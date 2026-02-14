"""
Core grant-matching rules engine.

This is the intellectual heart of GrantFinder Ireland. It evaluates a user
profile dict against every active grant's eligibility rules and returns a
ranked list of MatchResult objects.

Algorithm overview
──────────────────
1. Load all active grants together with their eligibility rules.
2. For each grant:
   a. Group rules by ``rule_group`` (rules in the same group are AND-ed).
   b. Evaluate every group against the user profile.
   c. If ANY group passes entirely → user is **eligible** (OR logic).
   d. Calculate a match score = best (max) percentage of mandatory rules
      passed across all groups.
3. Sort results: eligible → likely → possible, then by score descending.
4. Return matched grants with human-readable explanations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, List, Optional


# ── Match types ──────────────────────────────────────────────────────────────

class MatchType(str, Enum):
    ELIGIBLE = "eligible"           # All mandatory rules in ≥1 group pass
    LIKELY = "likely"               # ≥75 % of mandatory rules pass
    POSSIBLE = "possible"           # ≥50 % of mandatory rules pass
    NOT_ELIGIBLE = "not_eligible"   # < 50 %


# ── Result container ─────────────────────────────────────────────────────────

@dataclass
class MatchResult:
    grant_id: str
    grant_name: str
    match_type: MatchType
    match_score: float              # 0-100
    max_amount: Optional[float]
    amount_description: Optional[str]
    category: str
    source_organisation: str
    source_url: str
    application_url: Optional[str]
    short_description: str
    slug: str
    failed_rules: List[str] = field(default_factory=list)
    notes: str = ""


# ── Operator helpers ─────────────────────────────────────────────────────────

def _to_lower_list(val: str) -> list[str]:
    return [v.strip().lower() for v in val.split(",")]


def _op_eq(field_val: Any, rule_val: str) -> bool:
    return str(field_val).lower() == rule_val.lower()


def _op_neq(field_val: Any, rule_val: str) -> bool:
    return str(field_val).lower() != rule_val.lower()


def _op_gt(field_val: Any, rule_val: str) -> bool:
    return float(field_val) > float(rule_val)


def _op_gte(field_val: Any, rule_val: str) -> bool:
    return float(field_val) >= float(rule_val)


def _op_lt(field_val: Any, rule_val: str) -> bool:
    return float(field_val) < float(rule_val)


def _op_lte(field_val: Any, rule_val: str) -> bool:
    return float(field_val) <= float(rule_val)


def _op_in(field_val: Any, rule_val: str) -> bool:
    return str(field_val).lower() in _to_lower_list(rule_val)


def _op_not_in(field_val: Any, rule_val: str) -> bool:
    return str(field_val).lower() not in _to_lower_list(rule_val)


def _op_contains(field_val: Any, rule_val: str) -> bool:
    if isinstance(field_val, list):
        return rule_val.lower() in [v.lower() for v in field_val]
    return False


def _op_not_contains(field_val: Any, rule_val: str) -> bool:
    if isinstance(field_val, list):
        return rule_val.lower() not in [v.lower() for v in field_val]
    return True


def _op_is_true(field_val: Any, _rule_val: str) -> bool:
    return bool(field_val) is True


def _op_is_false(field_val: Any, _rule_val: str) -> bool:
    return bool(field_val) is False


def _op_exists(field_val: Any, _rule_val: str) -> bool:
    return field_val is not None and field_val != "" and field_val != []


def _op_between(field_val: Any, rule_val: str) -> bool:
    parts = rule_val.split(",")
    lo, hi = float(parts[0]), float(parts[1])
    return lo <= float(field_val) <= hi


OPERATORS: dict[str, Callable[[Any, str], bool]] = {
    "eq": _op_eq,
    "neq": _op_neq,
    "gt": _op_gt,
    "gte": _op_gte,
    "lt": _op_lt,
    "lte": _op_lte,
    "in": _op_in,
    "not_in": _op_not_in,
    "contains": _op_contains,
    "not_contains": _op_not_contains,
    "is_true": _op_is_true,
    "is_false": _op_is_false,
    "exists": _op_exists,
    "between": _op_between,
}


# ── Main engine ──────────────────────────────────────────────────────────────

_MATCH_TYPE_ORDER = {
    MatchType.ELIGIBLE: 0,
    MatchType.LIKELY: 1,
    MatchType.POSSIBLE: 2,
    MatchType.NOT_ELIGIBLE: 3,
}


class GrantMatcher:
    """Evaluate a user profile against all grants and return ranked matches."""

    def match(
        self,
        user_profile: dict[str, Any],
        grants_with_rules: list,
    ) -> list[MatchResult]:
        """
        Run the full matching algorithm.

        Parameters
        ----------
        user_profile : dict
            Keys correspond to ``EligibilityRule.field`` names.
        grants_with_rules : list
            Grant ORM objects (or grant-like dicts) with an
            ``eligibility_rules`` attribute/key.

        Returns
        -------
        list[MatchResult]
            Only grants where match_type != NOT_ELIGIBLE, sorted by
            relevance.
        """
        results: list[MatchResult] = []

        for grant in grants_with_rules:
            result = self._evaluate_grant(user_profile, grant)
            if result.match_type != MatchType.NOT_ELIGIBLE:
                results.append(result)

        results.sort(
            key=lambda r: (_MATCH_TYPE_ORDER.get(r.match_type, 3), -r.match_score)
        )
        return results

    # ── Per-grant evaluation ─────────────────────────────────────────────

    def _evaluate_grant(self, profile: dict[str, Any], grant) -> MatchResult:
        """Evaluate a single grant against the user profile."""

        # Support both ORM objects and plain dicts
        rules = (
            grant.eligibility_rules
            if hasattr(grant, "eligibility_rules")
            else grant.get("eligibility_rules", [])
        )
        grant_id = str(grant.id if hasattr(grant, "id") else grant["id"])
        grant_name = grant.name if hasattr(grant, "name") else grant["name"]
        slug = grant.slug if hasattr(grant, "slug") else grant.get("slug", "")
        category = grant.category if hasattr(grant, "category") else grant["category"]
        max_amount = (
            grant.max_amount if hasattr(grant, "max_amount") else grant.get("max_amount")
        )
        amount_desc = (
            grant.amount_description
            if hasattr(grant, "amount_description")
            else grant.get("amount_description", "")
        )
        source_org = (
            grant.source_organisation
            if hasattr(grant, "source_organisation")
            else grant.get("source_organisation", "")
        )
        source_url = (
            grant.source_url
            if hasattr(grant, "source_url")
            else grant.get("source_url", "")
        )
        application_url = (
            grant.application_url
            if hasattr(grant, "application_url")
            else grant.get("application_url")
        )
        short_desc = (
            grant.short_description
            if hasattr(grant, "short_description")
            else grant.get("short_description", "")
        )

        # No rules → universally available
        if not rules:
            return MatchResult(
                grant_id=grant_id,
                grant_name=grant_name,
                match_type=MatchType.ELIGIBLE,
                match_score=100.0,
                max_amount=float(max_amount) if max_amount else None,
                amount_description=amount_desc,
                category=category,
                source_organisation=source_org,
                source_url=source_url,
                application_url=application_url,
                short_description=short_desc,
                slug=slug,
                failed_rules=[],
                notes="No specific eligibility criteria — available to all.",
            )

        # Group rules by rule_group
        groups: dict[int, list] = {}
        for rule in rules:
            rg = rule.rule_group if hasattr(rule, "rule_group") else rule["rule_group"]
            groups.setdefault(rg, []).append(rule)

        best_score: float = 0
        best_failed: list[str] = []
        any_group_passed = False

        for _group_id, group_rules in groups.items():
            mandatory = [
                r
                for r in group_rules
                if (r.is_mandatory if hasattr(r, "is_mandatory") else r.get("is_mandatory", True))
            ]
            total = len(mandatory)
            passed = 0
            failed_descriptions: list[str] = []

            for rule in mandatory:
                r_field = rule.field if hasattr(rule, "field") else rule["field"]
                r_op = rule.operator if hasattr(rule, "operator") else rule["operator"]
                r_val = rule.value if hasattr(rule, "value") else rule["value"]
                r_desc = (
                    rule.description
                    if hasattr(rule, "description")
                    else rule.get("description")
                )

                field_value = profile.get(r_field)

                # Missing field → uncertain, not outright fail
                if field_value is None and r_op not in ("is_false", "exists"):
                    failed_descriptions.append(
                        r_desc or f"We need to know your '{r_field}'"
                    )
                    continue

                try:
                    evaluator = OPERATORS.get(r_op)
                    if evaluator and evaluator(field_value, r_val):
                        passed += 1
                    else:
                        failed_descriptions.append(
                            r_desc
                            or f"Requirement: {r_field} {r_op} {r_val}"
                        )
                except (ValueError, TypeError, IndexError):
                    failed_descriptions.append(
                        r_desc or f"Could not evaluate: {r_field}"
                    )

            group_score = (passed / total * 100) if total > 0 else 100.0

            if passed == total and total > 0:
                any_group_passed = True

            if group_score > best_score:
                best_score = group_score
                best_failed = failed_descriptions

        # Determine match type
        if any_group_passed:
            match_type = MatchType.ELIGIBLE
            best_score = 100.0
        elif best_score >= 75:
            match_type = MatchType.LIKELY
        elif best_score >= 50:
            match_type = MatchType.POSSIBLE
        else:
            match_type = MatchType.NOT_ELIGIBLE

        return MatchResult(
            grant_id=grant_id,
            grant_name=grant_name,
            match_type=match_type,
            match_score=best_score,
            max_amount=float(max_amount) if max_amount else None,
            amount_description=amount_desc,
            category=category,
            source_organisation=source_org,
            source_url=source_url,
            application_url=application_url,
            short_description=short_desc,
            slug=slug,
            failed_rules=best_failed,
            notes=self._generate_notes(match_type, best_failed),
        )

    # ── Note generation ──────────────────────────────────────────────────

    @staticmethod
    def _generate_notes(match_type: MatchType, failed_rules: list[str]) -> str:
        if match_type == MatchType.ELIGIBLE:
            return "You appear to meet all eligibility criteria for this grant."
        if match_type == MatchType.LIKELY:
            return (
                "You likely qualify, but should verify: "
                + "; ".join(failed_rules[:2])
            )
        if match_type == MatchType.POSSIBLE:
            return (
                "You may qualify — check these requirements: "
                + "; ".join(failed_rules[:3])
            )
        return ""

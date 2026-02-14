"""Unit tests for the grant-matching rules engine.

These tests validate the core GrantMatcher algorithm using dict-based grants
(no database needed).
"""

import pytest
from app.engine.matcher import GrantMatcher, MatchType


matcher = GrantMatcher()


# ── Helper: build a grant dict ───────────────────────────────────────────────

def _grant(name, slug, rules=None, max_amount=None, category="home_energy"):
    return {
        "id": slug,
        "name": name,
        "slug": slug,
        "short_description": f"Test grant: {name}",
        "category": category,
        "max_amount": max_amount,
        "amount_description": f"Up to €{max_amount}" if max_amount else None,
        "source_organisation": "Test",
        "source_url": "https://example.com",
        "application_url": None,
        "eligibility_rules": rules or [],
    }


def _rule(field, operator, value, group=0, description=None, mandatory=True):
    return {
        "rule_group": group,
        "field": field,
        "operator": operator,
        "value": value,
        "description": description or f"{field} {operator} {value}",
        "is_mandatory": mandatory,
    }


# ── SEAI Solar PV Grant ─────────────────────────────────────────────────────

solar_pv_grant = _grant("SEAI Solar PV Grant", "seai-solar-pv", max_amount=1800, rules=[
    _rule("home_status", "in", "owner,landlord"),
    _rule("home_year_built", "lt", "2021"),
    _rule("has_solar_pv", "is_false", "true"),
])


def test_solar_pv_eligible():
    """Homeowner with pre-2021 home, no existing solar should qualify."""
    profile = {
        "home_status": "owner",
        "home_year_built": 2005,
        "has_solar_pv": False,
        "county": "Dublin",
    }
    result = matcher.match(profile, [solar_pv_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.ELIGIBLE


def test_solar_pv_not_eligible_new_home():
    """Home built after 2021 fails 1 of 3 rules — returns 'possible' (66%)."""
    profile = {
        "home_status": "owner",
        "home_year_built": 2022,
        "has_solar_pv": False,
    }
    result = matcher.match(profile, [solar_pv_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.POSSIBLE


def test_solar_pv_not_eligible_renter():
    """Renter fails 1 of 3 rules — returns 'possible' (66%)."""
    profile = {
        "home_status": "renter",
        "home_year_built": 2000,
        "has_solar_pv": False,
    }
    result = matcher.match(profile, [solar_pv_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.POSSIBLE


def test_solar_pv_already_has_solar():
    """Owner who already has solar fails 1 of 3 rules — returns 'possible' (66%)."""
    profile = {
        "home_status": "owner",
        "home_year_built": 1990,
        "has_solar_pv": True,
    }
    result = matcher.match(profile, [solar_pv_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.POSSIBLE


# ── Warmer Homes Scheme (OR logic) ──────────────────────────────────────────

warmer_homes_grant = _grant("Warmer Homes Scheme", "warmer-homes", max_amount=None, rules=[
    # Group 0: owner + fuel_allowance
    _rule("home_status", "eq", "owner", group=0),
    _rule("welfare_payments", "contains", "fuel_allowance", group=0),
    # Group 1: owner + disability_allowance
    _rule("home_status", "eq", "owner", group=1),
    _rule("welfare_payments", "contains", "disability_allowance", group=1),
    # Group 2: owner + jobseekers + child under 7
    _rule("home_status", "eq", "owner", group=2),
    _rule("welfare_payments", "contains", "jobseekers_allowance", group=2),
    _rule("has_child_under_7", "is_true", "true", group=2),
])


def test_warmer_homes_fuel_allowance():
    """Owner on Fuel Allowance should qualify."""
    profile = {
        "home_status": "owner",
        "welfare_payments": ["fuel_allowance"],
    }
    result = matcher.match(profile, [warmer_homes_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.ELIGIBLE


def test_warmer_homes_disability_allowance():
    """Owner on Disability Allowance should qualify (group 1)."""
    profile = {
        "home_status": "owner",
        "welfare_payments": ["disability_allowance"],
    }
    result = matcher.match(profile, [warmer_homes_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.ELIGIBLE


def test_warmer_homes_jobseeker_with_child():
    """Owner on Jobseeker's with child under 7 should qualify (group 2)."""
    profile = {
        "home_status": "owner",
        "welfare_payments": ["jobseekers_allowance"],
        "has_child_under_7": True,
    }
    result = matcher.match(profile, [warmer_homes_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.ELIGIBLE


def test_warmer_homes_renter_not_eligible():
    """Renter on Fuel Allowance passes 1 of 2 rules per group — 'possible' (50%)."""
    profile = {
        "home_status": "renter",
        "welfare_payments": ["fuel_allowance"],
    }
    result = matcher.match(profile, [warmer_homes_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.POSSIBLE


# ── Help to Buy ──────────────────────────────────────────────────────────────

htb_grant = _grant("Help to Buy", "help-to-buy", max_amount=30000, category="housing", rules=[
    _rule("is_first_time_buyer", "is_true", "true"),
])


def test_help_to_buy_first_time_buyer():
    """First-time buyer should qualify."""
    profile = {"is_first_time_buyer": True}
    result = matcher.match(profile, [htb_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.ELIGIBLE


def test_help_to_buy_not_first_time():
    """Non first-time buyer should NOT qualify."""
    profile = {"is_first_time_buyer": False}
    result = matcher.match(profile, [htb_grant])
    assert len(result) == 0


# ── No rules = universal ────────────────────────────────────────────────────

child_benefit = _grant("Child Benefit", "child-benefit", max_amount=1680, category="family", rules=[
    _rule("has_children", "is_true", "true"),
])

universal_grant = _grant("Drug Payment Scheme", "drug-payment", category="health", rules=[])


def test_child_benefit_eligible():
    profile = {"has_children": True}
    result = matcher.match(profile, [child_benefit])
    assert len(result) == 1
    assert result[0].match_type == MatchType.ELIGIBLE


def test_child_benefit_no_children():
    profile = {"has_children": False}
    result = matcher.match(profile, [child_benefit])
    assert len(result) == 0


def test_universal_grant_everyone_qualifies():
    """A grant with no rules should match everyone."""
    result = matcher.match({}, [universal_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.ELIGIBLE
    assert result[0].match_score == 100.0


# ── Multiple grants ─────────────────────────────────────────────────────────

def test_multiple_grants_match():
    """A typical homeowner profile should match multiple grants."""
    profile = {
        "age": 45,
        "county": "Cork",
        "home_status": "owner",
        "home_year_built": 1995,
        "ber_rating": "D1",
        "has_solar_pv": False,
        "has_heat_pump": False,
        "employment_status": "employed",
        "income_bracket": "40-60k",
        "has_children": True,
        "welfare_payments": [],
        "is_first_time_buyer": False,
    }
    all_grants = [solar_pv_grant, warmer_homes_grant, htb_grant, child_benefit, universal_grant]
    results = matcher.match(profile, all_grants)

    # Should match: solar PV, child benefit, drug payment scheme
    # Should NOT match: warmer homes (no welfare), help to buy (not first-time)
    assert len(results) >= 3
    matched_names = [r.grant_name for r in results]
    assert "SEAI Solar PV Grant" in matched_names
    assert "Child Benefit" in matched_names
    assert "Drug Payment Scheme" in matched_names


def test_results_sorted_by_match_type():
    """Results should be sorted: eligible first, then likely, then possible."""
    profile = {
        "home_status": "owner",
        "home_year_built": 1995,
        "has_solar_pv": False,
        "has_children": True,
    }
    all_grants = [solar_pv_grant, child_benefit, universal_grant]
    results = matcher.match(profile, all_grants)

    types = [r.match_type for r in results]
    expected_order = sorted(types, key=lambda t: {
        MatchType.ELIGIBLE: 0, MatchType.LIKELY: 1, MatchType.POSSIBLE: 2
    }.get(t, 3))
    assert types == expected_order


# ── Missing fields handled gracefully ────────────────────────────────────────

def test_missing_fields_handled_gracefully():
    """Missing profile fields should result in 'likely' or 'possible', not crash."""
    profile = {
        "home_status": "owner",
        # home_year_built is missing, has_solar_pv is missing
    }
    result = matcher.match(profile, [solar_pv_grant])
    assert len(result) >= 1
    assert result[0].match_type in (MatchType.LIKELY, MatchType.POSSIBLE)


# ── between operator ─────────────────────────────────────────────────────────

age_grant = _grant("Age-Restricted Grant", "age-grant", rules=[
    _rule("age", "between", "18,66"),
])


def test_between_operator_in_range():
    profile = {"age": 35}
    result = matcher.match(profile, [age_grant])
    assert len(result) == 1
    assert result[0].match_type == MatchType.ELIGIBLE


def test_between_operator_out_of_range():
    profile = {"age": 70}
    result = matcher.match(profile, [age_grant])
    assert len(result) == 0

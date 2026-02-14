"""Scan endpoints: run grant matching, get results, history."""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User
from app.models.profile import UserProfile
from app.models.grant import Grant
from app.models.scan_result import ScanResult, ScanResultGrant
from app.engine.matcher import GrantMatcher, MatchResult
from app.engine.savings import calculate_savings
from app.engine.ai_summary import generate_ai_summary
from app.schemas.scan import (
    AnonymousScanRequest,
    ScanResponse,
    CategoryResult,
    GrantMatchResponse,
    ScanHistoryItem,
)
from app.utils.auth import get_current_user, get_optional_user
from app.utils.validators import GRANT_CATEGORIES
from app.engine.how_to_claim import HOW_TO_CLAIM

router = APIRouter(prefix="/api/v1/scan", tags=["Scan"])
matcher = GrantMatcher()

def _run_scan(profile_dict: dict, db: Session) -> list[MatchResult]:
    """Load active grants with rules and run the matcher."""
    grants = (
        db.query(Grant)
        .filter(Grant.is_active == True)  # noqa: E712
        .options(joinedload(Grant.eligibility_rules))
        .all()
    )
    return matcher.match(profile_dict, grants)


def _build_response(
    results: list[MatchResult],
    profile_dict: dict,
    scan_id: Optional[str] = None,
    include_ai_summary: bool = True,
) -> ScanResponse:
    """Convert MatchResult list into a ScanResponse grouped by category."""
    category_map = dict(GRANT_CATEGORIES)
    cat_buckets: dict[str, list[GrantMatchResponse]] = {}
    total_value = 0.0
    income_bracket = profile_dict.get("income_bracket")

    grant_dicts_for_ai = []

    for r in results:
        # Calculate precise savings
        savings = calculate_savings(
            slug=r.slug,
            max_amount=r.max_amount,
            amount_description=r.amount_description or "",
            income_bracket=income_bracket,
            profile=profile_dict,
        )

        grant_resp = GrantMatchResponse(
            grant_id=r.grant_id,
            name=r.grant_name,
            slug=r.slug,
            short_description=r.short_description,
            match_type=r.match_type.value,
            match_score=r.match_score,
            max_amount=r.max_amount,
            amount_description=r.amount_description or "",
            source_organisation=r.source_organisation,
            source_url=r.source_url,
            application_url=r.application_url,
            notes=r.notes,
            is_locked=False,
            category=r.category,
            estimated_annual_saving=savings["estimated_annual_saving"],
            estimated_backdated_saving=savings["estimated_backdated_saving"],
            savings_note=savings["savings_note"],
            how_to_claim=HOW_TO_CLAIM.get(r.slug, ""),
        )
        cat_buckets.setdefault(r.category, []).append(grant_resp)
        if r.max_amount:
            total_value += r.max_amount

        # For AI summary
        grant_dicts_for_ai.append({
            "name": r.grant_name,
            "match_type": r.match_type.value,
            "max_amount": r.max_amount,
            "amount_description": r.amount_description or "",
            "category": r.category,
            "savings_note": savings["savings_note"],
        })

    categories = [
        CategoryResult(
            category=cat,
            label=category_map.get(cat, cat),
            count=len(grants_list),
            total_value=sum(g.max_amount or 0 for g in grants_list),
            grants=grants_list,
        )
        for cat, grants_list in cat_buckets.items()
    ]
    categories.sort(key=lambda c: c.total_value, reverse=True)

    # Generate AI summary
    summary = ""
    if include_ai_summary:
        summary = generate_ai_summary(profile_dict, grant_dicts_for_ai, total_value)

    return ScanResponse(
        scan_id=scan_id,
        total_grants_found=len(results),
        total_potential_value=total_value,
        categories=categories,
        summary=summary,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.post("/anonymous", response_model=ScanResponse)
def anonymous_scan(body: AnonymousScanRequest, db: Session = Depends(get_db)):
    """Run a grant scan without an account (limited results)."""
    profile_dict = body.model_dump(exclude_unset=True)

    # Compute convenience flags
    age = profile_dict.get("age")
    if age is not None:
        profile_dict["is_over_65"] = age >= 65
        profile_dict["is_over_66"] = age >= 66
        profile_dict["is_over_70"] = age >= 70
    youngest = profile_dict.get("youngest_child_age")
    if youngest is not None:
        profile_dict["has_child_under_7"] = youngest < 7

    results = _run_scan(profile_dict, db)
    return _build_response(results, profile_dict)


@router.post("", response_model=ScanResponse)
def run_scan(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Run a full grant scan using the authenticated user's profile."""
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.id)
        .order_by(UserProfile.updated_at.desc())
        .first()
    )
    if not profile:
        raise HTTPException(400, "Please complete your profile first.")

    profile_dict = profile.to_dict()
    results = _run_scan(profile_dict, db)

    # Save scan result (before building response so we have scan_id)
    total_value = sum(r.max_amount or 0 for r in results)
    scan = ScanResult(
        user_id=user.id,
        profile_id=profile.id,
        total_grants=len(results),
        total_value=total_value,
    )
    db.add(scan)
    db.flush()

    for idx, r in enumerate(results):
        db.add(
            ScanResultGrant(
                scan_result_id=scan.id,
                grant_id=r.grant_id,
                match_score=r.match_score,
                match_type=r.match_type.value,
                notes=r.notes,
                sort_order=idx,
            )
        )

    user.last_scan_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(scan)

    return _build_response(results, profile_dict, scan_id=str(scan.id))


@router.get("/results", response_model=ScanResponse)
def get_latest_results(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the latest scan results for the authenticated user."""
    scan = (
        db.query(ScanResult)
        .filter(ScanResult.user_id == user.id)
        .order_by(ScanResult.created_at.desc())
        .first()
    )
    if not scan:
        raise HTTPException(404, "No scan results found. Run a scan first.")

    # Reload the matched grants with their grant details
    result_grants = (
        db.query(ScanResultGrant)
        .filter(ScanResultGrant.scan_result_id == scan.id)
        .options(joinedload(ScanResultGrant.grant))
        .order_by(ScanResultGrant.sort_order)
        .all()
    )

    category_map = dict(GRANT_CATEGORIES)
    cat_buckets: dict[str, list[GrantMatchResponse]] = {}

    for rg in result_grants:
        g = rg.grant

        resp = GrantMatchResponse(
            grant_id=str(g.id),
            name=g.name,
            slug=g.slug,
            short_description=g.short_description,
            match_type=rg.match_type,
            match_score=float(rg.match_score) if rg.match_score else 0,
            max_amount=float(g.max_amount) if g.max_amount else None,
            amount_description=g.amount_description or "",
            source_organisation=g.source_organisation,
            source_url=g.source_url,
            application_url=g.application_url,
            notes=rg.notes or "",
            is_locked=False,
            category=g.category,
        )
        cat_buckets.setdefault(g.category, []).append(resp)

    categories = [
        CategoryResult(
            category=cat,
            label=category_map.get(cat, cat),
            count=len(grants_list),
            total_value=sum(gl.max_amount or 0 for gl in grants_list),
            grants=grants_list,
        )
        for cat, grants_list in cat_buckets.items()
    ]
    categories.sort(key=lambda c: c.total_value, reverse=True)

    return ScanResponse(
        scan_id=str(scan.id),
        total_grants_found=scan.total_grants,
        total_potential_value=float(scan.total_value) if scan.total_value else 0,
        categories=categories,
        summary=scan.summary or "",
        generated_at=scan.created_at.isoformat(),
    )


@router.get("/history", response_model=list[ScanHistoryItem])
def get_scan_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all past scan results for the authenticated user."""
    scans = (
        db.query(ScanResult)
        .filter(ScanResult.user_id == user.id)
        .order_by(ScanResult.created_at.desc())
        .all()
    )
    return [
        ScanHistoryItem(
            id=str(s.id),
            total_grants=s.total_grants,
            total_value=float(s.total_value) if s.total_value else None,
            created_at=s.created_at.isoformat(),
        )
        for s in scans
    ]

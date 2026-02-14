"""Admin endpoints: CRUD for grants, rules, stats, import."""

import json
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from slugify import slugify

from app.database import get_db
from app.models.user import User
from app.models.grant import Grant, GrantDocument, GrantStep
from app.models.eligibility_rule import EligibilityRule
from app.models.scan_result import ScanResult
from app.models.audit import GrantAuditLog
from app.schemas.grant import (
    GrantCreate,
    GrantUpdate,
    GrantResponse,
    EligibilityRuleCreate,
    EligibilityRuleResponse,
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


# TODO: Add proper admin role checking
def _require_admin(user: User):
    """Placeholder admin check — replace with real role system."""
    pass  # For MVP, any authenticated user can access admin


@router.get("/grants")
def admin_list_grants(
    include_inactive: bool = True,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(user)
    query = db.query(Grant)
    if not include_inactive:
        query = query.filter(Grant.is_active == True)  # noqa: E712
    total = query.count()
    grants = query.order_by(Grant.category, Grant.name).offset((page - 1) * per_page).limit(per_page).all()

    return {
        "grants": [_grant_dict(g) for g in grants],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.post("/grants", status_code=201)
def admin_create_grant(
    body: GrantCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(user)

    grant = Grant(
        name=body.name,
        slug=body.slug or slugify(body.name),
        short_description=body.short_description,
        long_description=body.long_description,
        category=body.category,
        subcategory=body.subcategory,
        max_amount=body.max_amount,
        amount_description=body.amount_description,
        amount_type=body.amount_type,
        is_means_tested=body.is_means_tested,
        source_organisation=body.source_organisation,
        source_url=body.source_url,
        application_url=body.application_url,
        application_method=body.application_method,
        is_always_open=body.is_always_open,
        opening_date=body.opening_date,
        closing_date=body.closing_date,
        typical_processing=body.typical_processing,
        last_verified_at=datetime.utcnow(),
    )
    db.add(grant)
    db.flush()

    # Audit log
    db.add(GrantAuditLog(
        grant_id=grant.id,
        changed_by=user.email or str(user.id),
        change_type="created",
        new_values=body.model_dump(),
    ))
    db.commit()
    db.refresh(grant)

    return _grant_dict(grant)


@router.put("/grants/{grant_id}")
def admin_update_grant(
    grant_id: str,
    body: GrantUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(user)
    grant = db.query(Grant).filter(Grant.id == grant_id).first()
    if not grant:
        raise HTTPException(404, "Grant not found")

    old_values = _grant_dict(grant)
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(grant, field, value)
    grant.last_verified_at = datetime.utcnow()

    db.add(GrantAuditLog(
        grant_id=grant.id,
        changed_by=user.email or str(user.id),
        change_type="updated",
        old_values=old_values,
        new_values=update_data,
    ))
    db.commit()
    db.refresh(grant)
    return _grant_dict(grant)


@router.delete("/grants/{grant_id}")
def admin_delete_grant(
    grant_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Soft-delete a grant (set is_active=False)."""
    _require_admin(user)
    grant = db.query(Grant).filter(Grant.id == grant_id).first()
    if not grant:
        raise HTTPException(404, "Grant not found")
    grant.is_active = False
    db.add(GrantAuditLog(
        grant_id=grant.id,
        changed_by=user.email or str(user.id),
        change_type="deactivated",
    ))
    db.commit()
    return {"message": "Grant deactivated"}


# ── Rules ────────────────────────────────────────────────────────────────────

@router.post("/grants/{grant_id}/rules", status_code=201)
def admin_add_rule(
    grant_id: str,
    body: EligibilityRuleCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(user)
    grant = db.query(Grant).filter(Grant.id == grant_id).first()
    if not grant:
        raise HTTPException(404, "Grant not found")

    rule = EligibilityRule(
        grant_id=grant.id,
        rule_group=body.rule_group,
        field=body.field,
        operator=body.operator,
        value=body.value,
        description=body.description,
        is_mandatory=body.is_mandatory,
        sort_order=body.sort_order,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {
        "id": str(rule.id),
        "grant_id": str(rule.grant_id),
        **body.model_dump(),
    }


@router.put("/rules/{rule_id}")
def admin_update_rule(
    rule_id: str,
    body: EligibilityRuleCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(user)
    rule = db.query(EligibilityRule).filter(EligibilityRule.id == rule_id).first()
    if not rule:
        raise HTTPException(404, "Rule not found")
    for field, value in body.model_dump().items():
        setattr(rule, field, value)
    db.commit()
    return {"message": "Rule updated"}


@router.delete("/rules/{rule_id}", status_code=204)
def admin_delete_rule(
    rule_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(user)
    rule = db.query(EligibilityRule).filter(EligibilityRule.id == rule_id).first()
    if not rule:
        raise HTTPException(404, "Rule not found")
    db.delete(rule)
    db.commit()


# ── Stats ────────────────────────────────────────────────────────────────────

@router.get("/stats")
def admin_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_admin(user)
    from app.models.user import User as UserModel
    total_users = db.query(func.count(UserModel.id)).scalar()
    total_scans = db.query(func.count(ScanResult.id)).scalar()
    total_grants = db.query(func.count(Grant.id)).filter(Grant.is_active == True).scalar()  # noqa: E712
    paid_users = db.query(func.count(UserModel.id)).filter(UserModel.plan != "free").scalar()

    return {
        "total_users": total_users,
        "total_scans": total_scans,
        "total_grants": total_grants,
        "paid_users": paid_users,
        "conversion_rate": round(paid_users / max(total_users, 1) * 100, 2),
    }


# ── Bulk import ──────────────────────────────────────────────────────────────

@router.post("/grants/import")
async def admin_import_grants(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Bulk import grants from a JSON file."""
    _require_admin(user)
    content = await file.read()
    try:
        grants_data = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON file")

    imported = 0
    for g_data in grants_data:
        # Skip if slug already exists
        existing = db.query(Grant).filter(Grant.slug == g_data.get("slug")).first()
        if existing:
            continue

        grant = Grant(
            name=g_data["name"],
            slug=g_data.get("slug", slugify(g_data["name"])),
            short_description=g_data["short_description"],
            long_description=g_data.get("long_description"),
            category=g_data["category"],
            subcategory=g_data.get("subcategory"),
            max_amount=g_data.get("max_amount"),
            amount_description=g_data.get("amount_description"),
            amount_type=g_data.get("amount_type", "variable"),
            is_means_tested=g_data.get("is_means_tested", False),
            source_organisation=g_data["source_organisation"],
            source_url=g_data["source_url"],
            application_url=g_data.get("application_url"),
            application_method=g_data.get("application_method"),
            is_always_open=g_data.get("is_always_open", True),
            typical_processing=g_data.get("typical_processing"),
            last_verified_at=datetime.utcnow(),
        )
        db.add(grant)
        db.flush()

        # Import rules
        for rule_data in g_data.get("eligibility_rules", []):
            db.add(EligibilityRule(
                grant_id=grant.id,
                rule_group=rule_data.get("rule_group", 0),
                field=rule_data["field"],
                operator=rule_data["operator"],
                value=rule_data["value"],
                description=rule_data.get("description"),
                is_mandatory=rule_data.get("is_mandatory", True),
            ))

        # Import steps
        for step_data in g_data.get("steps", []):
            db.add(GrantStep(
                grant_id=grant.id,
                step_number=step_data["step_number"],
                title=step_data["title"],
                description=step_data["description"],
                url=step_data.get("url"),
            ))

        # Import documents
        for doc_data in g_data.get("documents", []):
            db.add(GrantDocument(
                grant_id=grant.id,
                document_name=doc_data["document_name"],
                description=doc_data.get("description"),
                is_required=doc_data.get("is_required", True),
            ))

        imported += 1

    db.commit()
    return {"imported": imported, "total_in_file": len(grants_data)}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _grant_dict(g: Grant) -> dict:
    return {
        "id": str(g.id),
        "name": g.name,
        "slug": g.slug,
        "category": g.category,
        "max_amount": float(g.max_amount) if g.max_amount else None,
        "amount_description": g.amount_description,
        "source_organisation": g.source_organisation,
        "is_active": g.is_active,
        "last_verified_at": g.last_verified_at.isoformat() if g.last_verified_at else None,
    }

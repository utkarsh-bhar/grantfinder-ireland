"""Grant browsing endpoints: list, search, detail, categories."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.grant import Grant, GrantDocument, GrantStep
from app.schemas.grant import (
    GrantResponse,
    GrantListResponse,
    GrantDocumentResponse,
    GrantStepResponse,
    CategoryCount,
)
from app.utils.validators import GRANT_CATEGORIES

router = APIRouter(prefix="/api/v1/grants", tags=["Grants"])


@router.get("", response_model=GrantListResponse)
def list_grants(
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all active grants, optionally filtered by category."""
    query = db.query(Grant).filter(Grant.is_active == True)  # noqa: E712

    if category:
        query = query.filter(Grant.category == category)

    total = query.count()
    grants = (
        query.order_by(Grant.category, Grant.name)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return GrantListResponse(
        grants=[_grant_to_response(g) for g in grants],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/categories", response_model=list[CategoryCount])
def list_categories(db: Session = Depends(get_db)):
    """List all grant categories with counts."""
    counts = (
        db.query(Grant.category, func.count(Grant.id))
        .filter(Grant.is_active == True)  # noqa: E712
        .group_by(Grant.category)
        .all()
    )
    category_map = dict(GRANT_CATEGORIES)
    return [
        CategoryCount(
            category=cat,
            label=category_map.get(cat, cat),
            count=count,
        )
        for cat, count in counts
    ]


@router.get("/search")
def search_grants(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    """Search grants by keyword (name + description)."""
    search = f"%{q.lower()}%"
    results = (
        db.query(Grant)
        .filter(
            Grant.is_active == True,  # noqa: E712
            (func.lower(Grant.name).like(search))
            | (func.lower(Grant.short_description).like(search)),
        )
        .order_by(Grant.name)
        .limit(50)
        .all()
    )
    return {"results": [_grant_to_response(g) for g in results], "total": len(results)}


@router.get("/new")
def new_grants(db: Session = Depends(get_db)):
    """Get grants added in the last 30 days."""
    from datetime import datetime, timedelta

    cutoff = datetime.utcnow() - timedelta(days=30)
    results = (
        db.query(Grant)
        .filter(Grant.is_active == True, Grant.created_at >= cutoff)  # noqa: E712
        .order_by(Grant.created_at.desc())
        .all()
    )
    return {"grants": [_grant_to_response(g) for g in results]}


@router.get("/{slug}", response_model=GrantResponse)
def get_grant(slug: str, db: Session = Depends(get_db)):
    """Get a single grant by its slug."""
    grant = db.query(Grant).filter(Grant.slug == slug, Grant.is_active == True).first()  # noqa: E712
    if not grant:
        raise HTTPException(404, "Grant not found")
    return _grant_to_response(grant)


@router.get("/{slug}/steps", response_model=list[GrantStepResponse])
def get_grant_steps(slug: str, db: Session = Depends(get_db)):
    """Get application steps for a grant."""
    grant = db.query(Grant).filter(Grant.slug == slug).first()
    if not grant:
        raise HTTPException(404, "Grant not found")
    steps = (
        db.query(GrantStep)
        .filter(GrantStep.grant_id == grant.id)
        .order_by(GrantStep.step_number)
        .all()
    )
    return [
        GrantStepResponse(
            id=str(s.id),
            step_number=s.step_number,
            title=s.title,
            description=s.description,
            url=s.url,
        )
        for s in steps
    ]


@router.get("/{slug}/documents", response_model=list[GrantDocumentResponse])
def get_grant_documents(slug: str, db: Session = Depends(get_db)):
    """Get required documents for a grant."""
    grant = db.query(Grant).filter(Grant.slug == slug).first()
    if not grant:
        raise HTTPException(404, "Grant not found")
    docs = (
        db.query(GrantDocument)
        .filter(GrantDocument.grant_id == grant.id)
        .order_by(GrantDocument.sort_order)
        .all()
    )
    return [
        GrantDocumentResponse(
            id=str(d.id),
            document_name=d.document_name,
            description=d.description,
            is_required=d.is_required,
            sort_order=d.sort_order,
        )
        for d in docs
    ]


def _grant_to_response(grant: Grant) -> GrantResponse:
    return GrantResponse(
        id=str(grant.id),
        name=grant.name,
        slug=grant.slug,
        short_description=grant.short_description,
        long_description=grant.long_description,
        category=grant.category,
        subcategory=grant.subcategory,
        max_amount=float(grant.max_amount) if grant.max_amount else None,
        amount_description=grant.amount_description,
        amount_type=grant.amount_type,
        is_means_tested=grant.is_means_tested,
        source_organisation=grant.source_organisation,
        source_url=grant.source_url,
        application_url=grant.application_url,
        application_method=grant.application_method,
        is_always_open=grant.is_always_open,
        opening_date=grant.opening_date,
        closing_date=grant.closing_date,
        typical_processing=grant.typical_processing,
        is_active=grant.is_active,
        last_verified_at=grant.last_verified_at,
        created_at=grant.created_at,
    )

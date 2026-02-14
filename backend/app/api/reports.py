"""PDF report generation and download endpoints — free for all users."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.grant import Grant
from app.engine.matcher import GrantMatcher
from app.reports.generator import generate_report_bytes
from app.schemas.scan import AnonymousScanRequest

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])
matcher = GrantMatcher()


@router.post("/download")
def download_pdf_report(
    body: AnonymousScanRequest,
    db: Session = Depends(get_db),
):
    """
    Generate and download a PDF report from scan profile data.
    No authentication required — completely free.
    """
    profile_dict = body.model_dump(exclude_unset=True)

    # Compute convenience flags (same as scan endpoint)
    age = profile_dict.get("age")
    if age is not None:
        profile_dict["is_over_65"] = age >= 65
        profile_dict["is_over_66"] = age >= 66
        profile_dict["is_over_70"] = age >= 70
    youngest = profile_dict.get("youngest_child_age")
    if youngest is not None:
        profile_dict["has_child_under_7"] = youngest < 7

    # Run the matcher
    grants = (
        db.query(Grant)
        .filter(Grant.is_active == True)  # noqa: E712
        .options(joinedload(Grant.eligibility_rules))
        .all()
    )
    results = matcher.match(profile_dict, grants)

    # Build grant dicts for the report template
    matched_grants = []
    for r in results:
        matched_grants.append({
            "name": r.grant_name,
            "slug": r.slug,
            "category": r.category,
            "match_type": r.match_type.value,
            "match_score": r.match_score,
            "max_amount": r.max_amount,
            "amount_description": r.amount_description or "",
            "short_description": r.short_description,
            "source_url": r.source_url,
            "application_url": r.application_url,
            "notes": r.notes,
        })

    # Generate the PDF
    pdf_bytes = generate_report_bytes(matched_grants)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"GrantFinder_Report_{timestamp}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )

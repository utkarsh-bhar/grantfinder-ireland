"""PDF report generation and download endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User
from app.models.scan_result import ScanResult, ScanResultGrant
from app.reports.generator import generate_report
from app.utils.auth import get_current_user
from app.utils.s3 import get_presigned_url

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.post("/generate")
def generate_pdf_report(
    scan_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate a full PDF report for the user's scan results."""
    if user.plan not in ("report", "premium"):
        raise HTTPException(403, "PDF reports require a paid plan")

    # Get the scan result
    if scan_id:
        scan = (
            db.query(ScanResult)
            .filter(ScanResult.id == scan_id, ScanResult.user_id == user.id)
            .first()
        )
    else:
        scan = (
            db.query(ScanResult)
            .filter(ScanResult.user_id == user.id)
            .order_by(ScanResult.created_at.desc())
            .first()
        )

    if not scan:
        raise HTTPException(404, "No scan results found")

    # Load matched grants
    result_grants = (
        db.query(ScanResultGrant)
        .filter(ScanResultGrant.scan_result_id == scan.id)
        .options(joinedload(ScanResultGrant.grant))
        .order_by(ScanResultGrant.sort_order)
        .all()
    )

    matched_grants = []
    for rg in result_grants:
        g = rg.grant
        matched_grants.append({
            "name": g.name,
            "category": g.category,
            "match_type": rg.match_type,
            "match_score": float(rg.match_score) if rg.match_score else 0,
            "max_amount": float(g.max_amount) if g.max_amount else None,
            "amount_description": g.amount_description or "",
            "short_description": g.short_description,
            "source_url": g.source_url,
            "application_url": g.application_url,
            "notes": rg.notes or "",
        })

    # Generate the PDF
    s3_key = generate_report(user, scan, matched_grants)
    scan.report_url = s3_key
    db.commit()

    return {"report_url": s3_key, "scan_id": str(scan.id)}


@router.get("/{report_id}/download")
def download_report(
    report_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download a PDF report via pre-signed S3 URL."""
    scan = (
        db.query(ScanResult)
        .filter(ScanResult.id == report_id, ScanResult.user_id == user.id)
        .first()
    )
    if not scan or not scan.report_url:
        raise HTTPException(404, "Report not found")

    url = get_presigned_url(scan.report_url)
    return RedirectResponse(url=url)

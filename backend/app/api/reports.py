"""PDF report generation, download, and email endpoints — free for all users."""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.grant import Grant
from app.engine.matcher import GrantMatcher
from app.engine.savings import calculate_savings
from app.engine.ai_summary import generate_ai_summary
from app.engine.how_to_claim import HOW_TO_CLAIM
from app.reports.generator import generate_report_bytes
from app.schemas.scan import AnonymousScanRequest

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])
matcher = GrantMatcher()


def _build_report_data(body: AnonymousScanRequest, db: Session) -> tuple[list[dict], dict, float]:
    """Run scan and build enriched grant data for the report."""
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

    # Run the matcher
    grants = (
        db.query(Grant)
        .filter(Grant.is_active == True)  # noqa: E712
        .options(joinedload(Grant.eligibility_rules))
        .all()
    )
    results = matcher.match(profile_dict, grants)
    income_bracket = profile_dict.get("income_bracket")

    # Build enriched grant dicts
    matched_grants = []
    for r in results:
        savings = calculate_savings(
            slug=r.slug,
            max_amount=r.max_amount,
            amount_description=r.amount_description or "",
            income_bracket=income_bracket,
            profile=profile_dict,
        )
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
            "estimated_annual_saving": savings["estimated_annual_saving"],
            "estimated_backdated_saving": savings["estimated_backdated_saving"],
            "savings_note": savings["savings_note"],
            "how_to_claim": HOW_TO_CLAIM.get(r.slug, ""),
        })

    total_value = sum(g.get("max_amount") or 0 for g in matched_grants)

    return matched_grants, profile_dict, total_value


@router.post("/download")
def download_pdf_report(
    body: AnonymousScanRequest,
    db: Session = Depends(get_db),
):
    """Generate and download a PDF report. No authentication required."""
    matched_grants, profile_dict, total_value = _build_report_data(body, db)

    # Generate AI summary for the PDF
    ai_summary = generate_ai_summary(profile_dict, matched_grants, total_value)

    # Generate the PDF
    pdf_bytes = generate_report_bytes(matched_grants, ai_summary=ai_summary)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"GrantFinder_Report_{timestamp}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


class EmailReportRequest(BaseModel):
    profile: AnonymousScanRequest
    email: EmailStr


@router.post("/email")
def email_pdf_report(
    body: EmailReportRequest,
    db: Session = Depends(get_db),
):
    """Generate a PDF report and email it to the user."""
    matched_grants, profile_dict, total_value = _build_report_data(body.profile, db)

    # Generate AI summary
    ai_summary = generate_ai_summary(profile_dict, matched_grants, total_value)

    # Generate the PDF
    pdf_bytes = generate_report_bytes(
        matched_grants,
        user_label=body.email,
        ai_summary=ai_summary,
    )

    # Send email
    try:
        _send_email(body.email, pdf_bytes, len(matched_grants), total_value)
    except Exception as e:
        raise HTTPException(500, f"Failed to send email: {str(e)}")

    return {"message": f"Report sent to {body.email}", "grants_found": len(matched_grants)}


def _send_email(to_email: str, pdf_bytes: bytes, grants_count: int, total_value: float):
    """Send the PDF report via email using Resend."""
    import base64
    from app.config import get_settings

    settings = get_settings()

    # Try Resend first (preferred - simpler API)
    resend_key = settings.RESEND_API_KEY if hasattr(settings, 'RESEND_API_KEY') else ""

    if resend_key:
        import resend
        resend.api_key = resend_key
        resend.Emails.send({
            "from": "GrantFinder <reports@grantfinder.ie>",
            "to": [to_email],
            "subject": f"Your GrantFinder Report — {grants_count} grants worth €{total_value:,.0f}",
            "html": _email_html(grants_count, total_value),
            "attachments": [{
                "filename": "GrantFinder_Report.pdf",
                "content": base64.b64encode(pdf_bytes).decode("utf-8"),
            }],
        })
        return

    # Fall back to SendGrid
    if settings.SENDGRID_API_KEY:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import (
            Mail, Attachment, FileContent, FileName, FileType, Disposition
        )
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=to_email,
            subject=f"Your GrantFinder Report — {grants_count} grants worth €{total_value:,.0f}",
            html_content=_email_html(grants_count, total_value),
        )
        encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        attachment = Attachment(
            FileContent(encoded_pdf),
            FileName("GrantFinder_Report.pdf"),
            FileType("application/pdf"),
            Disposition("attachment"),
        )
        message.attachment = attachment
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        return

    raise Exception(
        "Email service not configured. Please set RESEND_API_KEY or SENDGRID_API_KEY."
    )


def _email_html(grants_count: int, total_value: float) -> str:
    return f"""
    <div style="font-family: -apple-system, sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #16a34a; font-size: 24px; margin: 0;">GrantFinder.ie</h1>
            <p style="color: #64748b; margin-top: 8px;">Your Personalised Grant Report</p>
        </div>

        <div style="background: linear-gradient(135deg, #16a34a, #059669); border-radius: 16px; padding: 30px; text-align: center; color: white; margin-bottom: 30px;">
            <p style="font-size: 14px; opacity: 0.9; margin: 0;">You could be entitled to up to</p>
            <p style="font-size: 42px; font-weight: 800; margin: 10px 0;">€{total_value:,.0f}</p>
            <p style="font-size: 14px; opacity: 0.9; margin: 0;">across {grants_count} grants and schemes</p>
        </div>

        <p style="color: #334155; font-size: 15px; line-height: 1.6;">
            Your personalised PDF report is attached to this email. It includes:
        </p>
        <ul style="color: #475569; font-size: 14px; line-height: 1.8; padding-left: 20px;">
            <li>All {grants_count} grants and tax credits you may qualify for</li>
            <li>Estimated savings and backdated claim amounts</li>
            <li>Step-by-step Revenue myAccount claiming instructions</li>
            <li>Direct application links for each grant</li>
        </ul>

        <p style="color: #334155; font-size: 15px; line-height: 1.6; margin-top: 20px;">
            <strong>Tip:</strong> Many tax credits can be backdated up to 4 years.
            Check the report for grants you could have claimed previously — you may be owed a refund!
        </p>

        <div style="border-top: 1px solid #e2e8f0; margin-top: 30px; padding-top: 20px; text-align: center;">
            <p style="color: #94a3b8; font-size: 12px;">
                This email was sent by GrantFinder.ie. Information is for guidance only and does not
                constitute financial advice. Verify eligibility directly with the relevant organisation.
            </p>
        </div>
    </div>
    """

"""PDF report generation using WeasyPrint + Jinja2 templates."""

import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from app.utils.validators import GRANT_CATEGORIES

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def generate_report_bytes(
    matched_grants: list[dict],
    user_label: str = "GrantFinder User",
    ai_summary: str = "",
) -> bytes:
    """
    Generate a PDF report and return it as bytes.

    Parameters
    ----------
    matched_grants : list[dict]
        Each dict should have: name, category, match_type, match_score,
        max_amount, amount_description, short_description, source_url,
        application_url, notes, slug, estimated_annual_saving,
        estimated_backdated_saving, savings_note, how_to_claim.
    user_label : str
        Label to show on the cover page.
    ai_summary : str
        AI-generated personalised summary text.

    Returns
    -------
    bytes
        The PDF file content.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("grant_report.html")

    # Group grants by category
    category_map = dict(GRANT_CATEGORIES)
    categories: dict[str, list] = {}
    for g in matched_grants:
        cat = g.get("category", "other")
        categories.setdefault(cat, []).append(g)

    total_value = sum(g.get("max_amount") or 0 for g in matched_grants)

    # Calculate total backdated value
    total_annual_saving = sum(g.get("estimated_annual_saving") or 0 for g in matched_grants)
    total_backdated = sum(g.get("estimated_backdated_saving") or 0 for g in matched_grants)
    backdatable_grants = [g for g in matched_grants if g.get("estimated_backdated_saving")]
    claimable_grants = [g for g in matched_grants if g.get("how_to_claim")]

    html_content = template.render(
        user_email=user_label,
        generated_date=datetime.now().strftime("%d %B %Y"),
        total_grants=len(matched_grants),
        total_value=f"€{total_value:,.0f}",
        total_annual_saving=f"€{total_annual_saving:,.0f}" if total_annual_saving else None,
        total_backdated=f"€{total_backdated:,.0f}" if total_backdated else None,
        backdatable_count=len(backdatable_grants),
        categories=categories,
        category_labels=category_map,
        grants=matched_grants,
        ai_summary=ai_summary,
        claimable_grants=claimable_grants,
    )

    try:
        from weasyprint import HTML
        pdf_bytes = HTML(string=html_content).write_pdf()
    except ImportError:
        pdf_bytes = html_content.encode("utf-8")

    return pdf_bytes

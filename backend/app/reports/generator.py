"""PDF report generation using WeasyPrint + Jinja2 templates."""

import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from app.config import get_settings
from app.utils.s3 import upload_pdf
from app.utils.validators import GRANT_CATEGORIES

settings = get_settings()

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def generate_report(user, scan_result, matched_grants: list[dict]) -> str:
    """Generate a PDF report and upload to S3. Returns S3 key."""
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("grant_report.html")

    # Group grants by category
    category_map = dict(GRANT_CATEGORIES)
    categories: dict[str, list] = {}
    for g in matched_grants:
        cat = g.get("category", "other")
        categories.setdefault(cat, []).append(g)

    total_value = sum(g.get("max_amount") or 0 for g in matched_grants)

    html_content = template.render(
        user_email=user.email or "GrantFinder User",
        generated_date=datetime.now().strftime("%d %B %Y"),
        total_grants=len(matched_grants),
        total_value=f"€{total_value:,.0f}",
        categories=categories,
        category_labels=category_map,
        grants=matched_grants,
    )

    # Try WeasyPrint, fall back to returning HTML key
    try:
        from weasyprint import HTML

        pdf_bytes = HTML(string=html_content).write_pdf()
    except ImportError:
        # WeasyPrint not installed — save as HTML instead
        pdf_bytes = html_content.encode("utf-8")

    s3_key = f"reports/{user.id}/{scan_result.id}.pdf"

    if settings.AWS_ACCESS_KEY_ID:
        url = upload_pdf(s3_key, pdf_bytes)
        return s3_key
    else:
        # Local dev — write to disk
        local_path = os.path.join("data", "reports")
        os.makedirs(local_path, exist_ok=True)
        filepath = os.path.join(local_path, f"{scan_result.id}.pdf")
        with open(filepath, "wb") as f:
            f.write(pdf_bytes)
        return filepath

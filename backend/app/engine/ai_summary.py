"""
AI-powered personalized summary using Claude.

Generates a tailored narrative based on the user's profile and matched grants.
"""

from __future__ import annotations

import logging
from typing import Any

from app.config import get_settings

logger = logging.getLogger(__name__)


def generate_ai_summary(
    profile: dict[str, Any],
    matched_grants: list[dict],
    total_value: float,
) -> str:
    """
    Generate a personalised AI summary of the user's grant results.

    Falls back to a template-based summary if the API key is not configured
    or the API call fails.
    """
    settings = get_settings()

    if not settings.ANTHROPIC_API_KEY:
        return _fallback_summary(profile, matched_grants, total_value)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        # Build a concise profile description
        profile_desc = _describe_profile(profile)
        grants_desc = _describe_grants(matched_grants[:10])  # Top 10 only

        message = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=600,
            messages=[{
                "role": "user",
                "content": f"""You are a friendly Irish grants advisor. Write a personalised 3-4 paragraph summary for this person's grant results. Be warm, specific, and actionable.

PROFILE:
{profile_desc}

TOP MATCHED GRANTS/CREDITS:
{grants_desc}

TOTAL POTENTIAL VALUE: €{total_value:,.0f}

Write a personalised summary that:
1. Acknowledges their specific situation (age, family, employment, etc.)
2. Highlights the 3-4 most impactful grants/credits they should prioritise
3. Mentions any credits they might be able to backdate for up to 4 years
4. Ends with a clear first step they should take

Keep it under 200 words. Use plain language. Don't use bullet points — write flowing paragraphs. Don't mention GrantFinder by name. Address the reader as "you"."""
            }],
        )

        return message.content[0].text.strip()

    except Exception as e:
        logger.warning(f"AI summary generation failed: {e}")
        return _fallback_summary(profile, matched_grants, total_value)


def _describe_profile(profile: dict) -> str:
    """Build a readable profile description for the AI prompt."""
    parts = []
    if profile.get("age"):
        parts.append(f"Age: {profile['age']}")
    if profile.get("county"):
        parts.append(f"County: {profile['county']}")
    if profile.get("marital_status"):
        parts.append(f"Marital status: {profile['marital_status']}")
    if profile.get("employment_status"):
        parts.append(f"Employment: {profile['employment_status']}")
    if profile.get("income_bracket"):
        parts.append(f"Income bracket: {profile['income_bracket']}")
    if profile.get("home_status"):
        parts.append(f"Housing: {profile['home_status']}")
    if profile.get("has_children"):
        num = profile.get("num_children", "")
        parts.append(f"Has children: yes ({num} children)" if num else "Has children: yes")
    if profile.get("is_carer"):
        parts.append("Is a carer: yes")
    if profile.get("has_dependent_relatives"):
        parts.append(f"Has dependent relatives: yes ({profile.get('num_dependent_relatives', 1)})")
    if profile.get("works_from_home"):
        parts.append("Works from home: yes")
    if profile.get("has_medical_expenses"):
        parts.append("Has medical expenses: yes")
    if profile.get("has_mortgage"):
        parts.append("Has mortgage: yes")
    if profile.get("has_nursing_home_expenses"):
        parts.append("Paying nursing home fees: yes")
    if profile.get("is_student"):
        parts.append("Is a student: yes")
    return "\n".join(parts) if parts else "No detailed profile provided"


def _describe_grants(grants: list[dict]) -> str:
    """Build a readable grants list for the AI prompt."""
    lines = []
    for g in grants:
        amount = g.get("amount_description") or (f"€{g.get('max_amount', 0):,.0f}" if g.get("max_amount") else "Variable")
        lines.append(f"- {g['name']} ({g['match_type']}): {amount}")
        if g.get("savings_note"):
            lines.append(f"  Savings: {g['savings_note']}")
    return "\n".join(lines)


def _fallback_summary(
    profile: dict,
    matched_grants: list[dict],
    total_value: float,
) -> str:
    """Generate a template-based summary when AI is unavailable."""
    eligible_count = sum(1 for g in matched_grants if g.get("match_type") == "eligible")
    tax_credits = [g for g in matched_grants if g.get("category") == "tax_relief"]
    top_grants = sorted(matched_grants, key=lambda g: g.get("max_amount") or 0, reverse=True)[:3]

    parts = [
        f"Based on your profile, we found {len(matched_grants)} grants, schemes, and tax credits "
        f"you may be entitled to, with a combined potential value of up to €{total_value:,.0f}. "
        f"{eligible_count} of these are strong matches where you appear to meet all eligibility criteria."
    ]

    if tax_credits:
        parts.append(
            f" You qualify for {len(tax_credits)} tax credit{'s' if len(tax_credits) != 1 else ''} "
            f"that could save you money — many of these can be backdated up to 4 years, "
            f"so you may be owed money from previous years too."
        )

    if top_grants:
        top_names = ", ".join(g["name"] for g in top_grants[:3])
        parts.append(
            f" Your highest-value matches include {top_names}."
            f" We recommend starting with the grants marked as 'eligible' and working through them in order of value."
        )

    return "".join(parts)

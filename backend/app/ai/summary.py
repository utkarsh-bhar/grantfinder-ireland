"""AI-generated scan summary using Claude API."""

import anthropic
from app.config import get_settings

settings = get_settings()


def generate_scan_summary(user_profile: dict, matched_grants: list) -> str:
    """Generate a warm, personalised summary of grant scan results.

    Falls back to a templated summary if the Anthropic key is not configured
    or the API call fails.
    """
    # Build grant list text
    grants_text = "\n".join(
        f"- {g['name']} ({g['category']}): up to {g.get('amount_description', 'variable')} — {g['match_type']}"
        for g in matched_grants[:20]
    )

    if not settings.ANTHROPIC_API_KEY:
        return _fallback_summary(user_profile, matched_grants)

    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,
            system=(
                "You are an Irish grants advisor. Generate a warm, encouraging, "
                "plain-English summary of the grant scan results. Be specific about "
                "amounts and categories. Keep it to 3-4 sentences. Use Euro (€) symbol. "
                "Don't use marketing language or exclamation marks. Be factual but friendly. "
                "Address the user as 'you'. Write as if speaking to them directly."
            ),
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"User profile summary:\n"
                        f"- Age: {user_profile.get('age', 'unknown')}\n"
                        f"- County: {user_profile.get('county', 'unknown')}\n"
                        f"- Home status: {user_profile.get('home_status', 'unknown')}\n"
                        f"- Employment: {user_profile.get('employment_status', 'unknown')}\n"
                        f"\nMatched grants:\n{grants_text}\n\n"
                        "Generate a personalised summary paragraph."
                    ),
                }
            ],
        )
        return message.content[0].text
    except Exception:
        return _fallback_summary(user_profile, matched_grants)


def _fallback_summary(user_profile: dict, matched_grants: list) -> str:
    """Template-based summary when the AI is unavailable."""
    total = len(matched_grants)
    total_value = sum(g.get("max_amount") or 0 for g in matched_grants)
    eligible = [g for g in matched_grants if g.get("match_type") == "eligible"]

    county = user_profile.get("county", "your area")
    value_str = f"€{total_value:,.0f}" if total_value else "various amounts"

    return (
        f"Based on your profile, we found {total} grants and schemes you may be "
        f"entitled to, with a combined potential value of up to {value_str}. "
        f"Of these, {len(eligible)} appear to be a strong match based on your answers. "
        f"We recommend starting with the highest-value grants and working through "
        f"the application steps provided."
    )

"""AI Chat Q&A — lets users ask questions about grants using Claude."""

import anthropic
from app.config import get_settings

settings = get_settings()


def answer_grant_question(
    question: str, user_profile: dict, relevant_grants: list
) -> str:
    """Answer a user question about grants using their profile context."""
    grants_context = "\n".join(
        f"Grant: {g['name']}\n"
        f"Description: {g.get('long_description', g.get('short_description', ''))}\n"
        f"Max amount: {g.get('amount_description', 'variable')}\n"
        f"Eligibility: {g.get('notes', 'See official source')}\n"
        f"How to apply: {g.get('application_url', g.get('source_url', ''))}\n"
        for g in relevant_grants[:5]
    )

    if not settings.ANTHROPIC_API_KEY:
        return (
            "I'm sorry, the AI assistant is not available at the moment. "
            "Please check the individual grant pages for more information, "
            "or contact the relevant government body directly."
        )

    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=800,
            system=(
                "You are an Irish government grants advisor chatbot for GrantFinder.ie. "
                "You help users understand what grants they qualify for and how to apply.\n\n"
                "Rules:\n"
                "- Be accurate. Only reference grants you have data for.\n"
                "- If unsure, say \"I'd recommend checking [source] directly\" with the URL.\n"
                "- Use simple language, no jargon.\n"
                "- Be concise — aim for 2-3 short paragraphs max.\n"
                "- Always mention relevant amounts in Euro (€).\n"
                "- Never give tax or legal advice — suggest consulting an accountant/solicitor.\n"
                "- You are NOT a government representative. You help people find information."
            ),
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"User context:\n"
                        f"- County: {user_profile.get('county', 'unknown')}\n"
                        f"- Home status: {user_profile.get('home_status', 'unknown')}\n"
                        f"- Employment: {user_profile.get('employment_status', 'unknown')}\n"
                        f"\nRelevant grants in our database:\n{grants_context}\n"
                        f"User question: {question}"
                    ),
                }
            ],
        )
        return message.content[0].text
    except Exception as e:
        return (
            "I'm sorry, I couldn't process your question right now. "
            f"Please try again in a moment. (Error: {str(e)[:100]})"
        )

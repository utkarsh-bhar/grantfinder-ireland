"""AI Chat endpoint: ask questions about grants using Claude API."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.models.grant import Grant
from app.models.profile import UserProfile
from app.ai.chat import answer_grant_question
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    question: str
    grant_slug: str | None = None  # Optionally scope to a specific grant


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []  # Grant slugs used for context


@router.post("", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.plan != "premium":
        raise HTTPException(403, "AI Chat requires a Premium subscription")

    # Load user profile for context
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.id)
        .order_by(UserProfile.updated_at.desc())
        .first()
    )
    profile_dict = profile.to_dict() if profile else {}

    # Load relevant grants
    if body.grant_slug:
        grants = (
            db.query(Grant)
            .filter(Grant.slug == body.grant_slug, Grant.is_active == True)  # noqa: E712
            .all()
        )
    else:
        # Use the user's most recent scan results or top grants
        grants = (
            db.query(Grant)
            .filter(Grant.is_active == True)  # noqa: E712
            .limit(10)
            .all()
        )

    grants_data = [
        {
            "name": g.name,
            "slug": g.slug,
            "long_description": g.long_description or g.short_description,
            "amount_description": g.amount_description,
            "source_url": g.source_url,
            "application_url": g.application_url,
            "notes": "",
        }
        for g in grants
    ]

    answer = answer_grant_question(body.question, profile_dict, grants_data)

    return ChatResponse(
        answer=answer,
        sources=[g.slug for g in grants],
    )

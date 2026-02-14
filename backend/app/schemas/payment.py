"""Payment / Stripe schemas."""

from typing import Optional
from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    price_id: str  # Stripe price ID
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class SubscriptionStatus(BaseModel):
    plan: str
    is_active: bool
    expires_at: Optional[str] = None
    stripe_customer_id: Optional[str] = None

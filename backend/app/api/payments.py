"""Stripe payment endpoints: checkout, webhooks, status."""

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.user import User
from app.schemas.payment import CheckoutRequest, CheckoutResponse, SubscriptionStatus
from app.utils.auth import get_current_user

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])


@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout(
    body: CheckoutRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a Stripe Checkout session."""
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(503, "Payments are not configured")

    # Ensure user has a Stripe customer
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(email=user.email)
        user.stripe_customer_id = customer.id
        db.commit()

    success_url = body.success_url or f"{settings.APP_URL}/results?payment=success"
    cancel_url = body.cancel_url or f"{settings.APP_URL}/pricing?payment=cancelled"

    session = stripe.checkout.Session.create(
        customer=user.stripe_customer_id,
        payment_method_types=["card"],
        line_items=[{"price": body.price_id, "quantity": 1}],
        mode="subscription" if "monthly" in body.price_id or "annual" in body.price_id else "payment",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"user_id": str(user.id)},
    )

    return CheckoutResponse(checkout_url=session.url, session_id=session.id)


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(503, "Webhook secret not configured")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(400, "Invalid webhook signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("user_id")
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                # Determine plan from the session
                if session.get("mode") == "subscription":
                    user.plan = "premium"
                else:
                    user.plan = "report"
                db.commit()

    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        customer_id = sub.get("customer")
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.plan = "free"
            user.plan_expires_at = None
            db.commit()

    return {"status": "ok"}


@router.get("/status", response_model=SubscriptionStatus)
def payment_status(user: User = Depends(get_current_user)):
    """Get current subscription status."""
    return SubscriptionStatus(
        plan=user.plan,
        is_active=user.plan in ("report", "premium"),
        expires_at=user.plan_expires_at.isoformat() if user.plan_expires_at else None,
        stripe_customer_id=user.stripe_customer_id,
    )


@router.post("/cancel")
def cancel_subscription(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel a user's premium subscription."""
    if not user.stripe_customer_id:
        raise HTTPException(400, "No active subscription")

    # Cancel all active subscriptions for this customer
    subscriptions = stripe.Subscription.list(
        customer=user.stripe_customer_id, status="active"
    )
    for sub in subscriptions.auto_paging_iter():
        stripe.Subscription.cancel(sub.id)

    user.plan = "free"
    user.plan_expires_at = None
    db.commit()

    return {"message": "Subscription cancelled successfully"}

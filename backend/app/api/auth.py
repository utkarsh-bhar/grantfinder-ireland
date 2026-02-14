"""Authentication endpoints: register, login, refresh, OAuth."""

from collections import defaultdict
from datetime import datetime, timedelta
from threading import Lock

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# In-memory rate limiter: {ip: [timestamps]}
_rate_limit_store: dict[str, list[datetime]] = defaultdict(list)
_rate_limit_lock = Lock()
_RATE_LIMIT_MAX = 10
_RATE_LIMIT_WINDOW_SECONDS = 60


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit_auth(request: Request) -> None:
    ip = _get_client_ip(request)
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=_RATE_LIMIT_WINDOW_SECONDS)
    with _rate_limit_lock:
        timestamps = _rate_limit_store[ip]
        timestamps[:] = [t for t in timestamps if t > cutoff]
        if len(timestamps) >= _RATE_LIMIT_MAX:
            raise HTTPException(429, "Too many requests. Please try again later.")
        timestamps.append(now)


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(
    body: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    rate_limit_auth(request)
    if len(body.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")

    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(409, "An account with this email already exists")

    user = User(
        email=body.email,
        password_hash=hash_password(body.password),
        auth_provider="email",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    rate_limit_auth(request)
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not user.password_hash:
        raise HTTPException(401, "Invalid email or password")
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(401, "Invalid or expired refresh token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(401, "User not found")

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/forgot-password", status_code=200)
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # Always return 200 to prevent email enumeration
    _user = db.query(User).filter(User.email == body.email).first()
    # TODO: Send password reset email via SendGrid
    return {"message": "If an account with that email exists, a reset link has been sent."}


@router.post("/reset-password", status_code=200)
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(body.token)
        if payload.get("type") != "reset":
            raise HTTPException(400, "Invalid reset token")
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(400, "Invalid or expired reset token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(400, "Invalid token")

    if len(body.new_password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")

    user.password_hash = hash_password(body.new_password)
    db.commit()
    return {"message": "Password has been reset successfully."}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
        "plan": user.plan,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }

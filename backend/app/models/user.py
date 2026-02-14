"""User model — authentication and subscription data."""

import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str | None] = mapped_column(
        String(255), unique=True, index=True
    )
    password_hash: Mapped[str | None] = mapped_column(String(255))
    auth_provider: Mapped[str | None] = mapped_column(String(50))  # email, google, apple
    auth_provider_id: Mapped[str | None] = mapped_column(String(255))

    # Subscription
    plan: Mapped[str] = mapped_column(
        String(20), default="free"
    )  # free, report, premium
    plan_expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    last_scan_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Relationships
    profiles: Mapped[list["UserProfile"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
    scan_results: Mapped[list["ScanResult"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
    alerts: Mapped[list["GrantAlert"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"

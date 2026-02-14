"""Grant, GrantDocument, and GrantStep models."""

import uuid
from datetime import datetime, date
from sqlalchemy import (
    String,
    Text,
    Boolean,
    Integer,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Grant(Base):
    __tablename__ = "grants"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    short_description: Mapped[str] = mapped_column(Text, nullable=False)
    long_description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    subcategory: Mapped[str | None] = mapped_column(String(100))

    # Financial details
    max_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    amount_description: Mapped[str | None] = mapped_column(Text)
    amount_type: Mapped[str] = mapped_column(
        String(30), nullable=False
    )  # fixed, percentage, variable, free_service
    is_means_tested: Mapped[bool] = mapped_column(Boolean, default=False)

    # Source & application
    source_organisation: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    application_url: Mapped[str | None] = mapped_column(Text)
    application_method: Mapped[str | None] = mapped_column(String(50))

    # Timing
    is_always_open: Mapped[bool] = mapped_column(Boolean, default=True)
    opening_date: Mapped[date | None] = mapped_column(Date)
    closing_date: Mapped[date | None] = mapped_column(Date)
    typical_processing: Mapped[str | None] = mapped_column(String(100))

    # Metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    last_verified_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes: Mapped[str | None] = mapped_column(Text)

    # Relationships
    eligibility_rules: Mapped[list["EligibilityRule"]] = relationship(  # noqa: F821
        back_populates="grant", cascade="all, delete-orphan"
    )
    documents: Mapped[list["GrantDocument"]] = relationship(
        back_populates="grant", cascade="all, delete-orphan"
    )
    steps: Mapped[list["GrantStep"]] = relationship(
        back_populates="grant", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Grant {self.slug}>"


class GrantDocument(Base):
    __tablename__ = "grant_documents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    grant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("grants.id", ondelete="CASCADE")
    )
    document_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    grant: Mapped["Grant"] = relationship(back_populates="documents")


class GrantStep(Base):
    __tablename__ = "grant_steps"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    grant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("grants.id", ondelete="CASCADE")
    )
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    grant: Mapped["Grant"] = relationship(back_populates="steps")

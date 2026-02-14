"""ScanResult and ScanResultGrant models — saved grant matching outcomes."""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_profiles.id")
    )
    total_grants: Mapped[int] = mapped_column(Integer, nullable=False)
    total_value: Mapped[float | None] = mapped_column(Numeric(12, 2))
    report_url: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="scan_results")  # noqa: F821
    matched_grants: Mapped[list["ScanResultGrant"]] = relationship(
        back_populates="scan_result", cascade="all, delete-orphan"
    )


class ScanResultGrant(Base):
    __tablename__ = "scan_result_grants"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    scan_result_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scan_results.id", ondelete="CASCADE"), index=True
    )
    grant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("grants.id"))
    match_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    match_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # eligible, likely, possible, check
    notes: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    scan_result: Mapped["ScanResult"] = relationship(back_populates="matched_grants")
    grant: Mapped["Grant"] = relationship()  # noqa: F821

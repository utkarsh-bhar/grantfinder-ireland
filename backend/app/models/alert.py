"""GrantAlert model — user notification preferences."""

import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class GrantAlert(Base):
    __tablename__ = "grant_alerts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    grant_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("grants.id"), nullable=True
    )
    alert_type: Mapped[str] = mapped_column(
        String(30), nullable=False
    )  # new_grant, deadline, change, all
    channel: Mapped[str] = mapped_column(
        String(20), default="email"
    )  # email, push, both
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="alerts")  # noqa: F821
    grant: Mapped["Grant | None"] = relationship()  # noqa: F821

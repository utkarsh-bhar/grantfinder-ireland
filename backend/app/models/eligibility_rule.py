"""EligibilityRule model — conditions that determine grant eligibility."""

import uuid
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    grant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("grants.id", ondelete="CASCADE"), index=True
    )

    rule_group: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # Same group = AND, different groups = OR
    field: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    operator: Mapped[str] = mapped_column(String(20), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationship
    grant: Mapped["Grant"] = relationship(back_populates="eligibility_rules")  # noqa: F821

    def __repr__(self) -> str:
        return f"<EligibilityRule {self.field} {self.operator} {self.value}>"

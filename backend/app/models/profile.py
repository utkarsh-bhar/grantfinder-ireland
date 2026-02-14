"""UserProfile model — questionnaire answers stored per user."""

import json
import uuid
from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Numeric,
    DateTime,
    ForeignKey,
    Text,
    TypeDecorator,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class JSONEncodedList(TypeDecorator):
    """Store a Python list as a JSON-encoded TEXT column (works with SQLite)."""
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return []


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    # ── PERSONAL ──────────────────────────────────────────────
    age: Mapped[int | None] = mapped_column(Integer)
    county: Mapped[str | None] = mapped_column(String(50))
    marital_status: Mapped[str | None] = mapped_column(String(30))
    nationality: Mapped[str | None] = mapped_column(String(50))
    residency_status: Mapped[str | None] = mapped_column(String(50))

    # ── HOUSING ───────────────────────────────────────────────
    home_status: Mapped[str | None] = mapped_column(String(30))
    home_type: Mapped[str | None] = mapped_column(String(30))
    home_year_built: Mapped[int | None] = mapped_column(Integer)
    ber_rating: Mapped[str | None] = mapped_column(String(5))
    has_solar_pv: Mapped[bool] = mapped_column(Boolean, default=False)
    has_heat_pump: Mapped[bool] = mapped_column(Boolean, default=False)
    property_value: Mapped[float | None] = mapped_column(Numeric(12, 2))
    mortgage_status: Mapped[str | None] = mapped_column(String(30))
    is_first_time_buyer: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── FAMILY ────────────────────────────────────────────────
    has_children: Mapped[bool] = mapped_column(Boolean, default=False)
    num_children: Mapped[int] = mapped_column(Integer, default=0)
    youngest_child_age: Mapped[int | None] = mapped_column(Integer)
    oldest_child_age: Mapped[int | None] = mapped_column(Integer)
    is_lone_parent: Mapped[bool] = mapped_column(Boolean, default=False)
    has_child_under_7: Mapped[bool] = mapped_column(Boolean, default=False)
    is_carer: Mapped[bool] = mapped_column(Boolean, default=False)
    caring_for_relationship: Mapped[str | None] = mapped_column(String(50))

    # ── EMPLOYMENT & INCOME ───────────────────────────────────
    employment_status: Mapped[str | None] = mapped_column(String(30))
    is_freelancer: Mapped[bool] = mapped_column(Boolean, default=False)
    has_side_income: Mapped[bool] = mapped_column(Boolean, default=False)
    annual_income: Mapped[float | None] = mapped_column(Numeric(12, 2))
    income_bracket: Mapped[str | None] = mapped_column(String(20))

    # ── WELFARE ───────────────────────────────────────────────
    welfare_payments: Mapped[list[str] | None] = mapped_column(JSONEncodedList)
    has_medical_card: Mapped[bool] = mapped_column(Boolean, default=False)
    has_gp_visit_card: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── DISABILITY & HEALTH ───────────────────────────────────
    has_disability: Mapped[bool] = mapped_column(Boolean, default=False)
    disability_type: Mapped[str | None] = mapped_column(String(50))
    household_disability: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── EDUCATION ─────────────────────────────────────────────
    is_student: Mapped[bool] = mapped_column(Boolean, default=False)
    education_level: Mapped[str | None] = mapped_column(String(50))
    planning_education: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── BUSINESS ──────────────────────────────────────────────
    owns_business: Mapped[bool] = mapped_column(Boolean, default=False)
    business_type: Mapped[str | None] = mapped_column(String(50))
    business_age_months: Mapped[int | None] = mapped_column(Integer)
    num_employees: Mapped[int] = mapped_column(Integer, default=0)
    business_sector: Mapped[str | None] = mapped_column(String(100))
    planning_business: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── TRANSPORT ─────────────────────────────────────────────
    owns_vehicle: Mapped[bool] = mapped_column(Boolean, default=False)
    vehicle_type: Mapped[str | None] = mapped_column(String(30))
    planning_ev_purchase: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── FARMING ───────────────────────────────────────────────
    is_farmer: Mapped[bool] = mapped_column(Boolean, default=False)
    farm_size_hectares: Mapped[float | None] = mapped_column(Numeric(8, 2))
    farm_type: Mapped[str | None] = mapped_column(String(50))

    # ── LANDLORD ──────────────────────────────────────────────
    is_landlord: Mapped[bool] = mapped_column(Boolean, default=False)
    num_rental_properties: Mapped[int] = mapped_column(Integer, default=0)

    # ── COMPUTED FLAGS ────────────────────────────────────────
    is_over_66: Mapped[bool] = mapped_column(Boolean, default=False)
    is_over_70: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── TIMESTAMPS ────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="profiles")  # noqa: F821

    def to_dict(self) -> dict:
        """Convert profile to dict for the rules engine."""
        data = {}
        for col in self.__table__.columns:
            if col.name in ("id", "user_id", "created_at", "updated_at"):
                continue
            val = getattr(self, col.name)
            if val is not None:
                data[col.name] = val
        # Compute convenience flags
        if self.age is not None:
            data["is_over_66"] = self.age >= 66
            data["is_over_70"] = self.age >= 70
        if self.youngest_child_age is not None:
            data["has_child_under_7"] = self.youngest_child_age < 7
        return data

    def __repr__(self) -> str:
        return f"<UserProfile user_id={self.user_id} county={self.county}>"

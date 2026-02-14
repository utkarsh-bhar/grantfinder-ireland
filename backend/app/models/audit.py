"""GrantAuditLog model — tracks all changes to grants."""

import json
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class JSONEncodedDict(TypeDecorator):
    """Store a Python dict as a JSON-encoded TEXT column (works with SQLite)."""
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value, default=str)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None


class GrantAuditLog(Base):
    __tablename__ = "grant_audit_log"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    grant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("grants.id"), index=True
    )
    changed_by: Mapped[str] = mapped_column(String(100), nullable=False)
    change_type: Mapped[str] = mapped_column(
        String(30), nullable=False
    )  # created, updated, deactivated
    old_values: Mapped[dict | None] = mapped_column(JSONEncodedDict)
    new_values: Mapped[dict | None] = mapped_column(JSONEncodedDict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

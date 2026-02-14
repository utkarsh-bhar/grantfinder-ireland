"""SQLAlchemy engine, session factory, and base model."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import get_settings

settings = get_settings()

_connect_args = {}
_kwargs: dict = {"pool_pre_ping": True}

if settings.DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}
    # SQLite doesn't support pool_size / max_overflow
else:
    _kwargs["pool_size"] = 10
    _kwargs["max_overflow"] = 20

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    **_kwargs,
)

# Enable WAL mode for SQLite (better concurrency)
if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

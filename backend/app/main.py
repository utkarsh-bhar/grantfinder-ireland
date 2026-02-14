"""FastAPI application entry point for GrantFinder Ireland."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base
from app.api import auth, profile, grants, scan, reports, payments, alerts, chat, admin

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and seed data on startup."""
    # Create tables (safe to call even if they exist already)
    Base.metadata.create_all(bind=engine)
    # Auto-seed grants from JSON (idempotent — skips if data exists)
    from app.database import SessionLocal
    from app.seed import seed_grants
    db = SessionLocal()
    try:
        seed_grants(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="GrantFinder Ireland API",
    description="Discover every government grant, scheme, and entitlement you qualify for in Ireland.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(grants.router)
app.include_router(scan.router)
app.include_router(reports.router)
app.include_router(payments.router)
app.include_router(alerts.router)
app.include_router(chat.router)
app.include_router(admin.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "name": "GrantFinder Ireland API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

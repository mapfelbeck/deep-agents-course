"""FastAPI application: router registration, CORS, and table creation."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import Base, engine
from app.models_db import Interview, Job, Note  # noqa: F401 - register models
from app.routers import interviews, jobs, notes, roles

settings = get_settings()

# Create tables on startup. For Postgres, prefer Alembic migrations in prod;
# this keeps local/dev friction to zero and is idempotent.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview Sheet API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roles.router)
app.include_router(interviews.router)
app.include_router(jobs.router)
app.include_router(notes.router)


@app.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}

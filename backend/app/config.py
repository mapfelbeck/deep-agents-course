"""Application settings loaded from the environment (with sane local defaults)."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ directory (this file lives at backend/app/config.py).
BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database. Defaults to a local SQLite file so the app runs with zero setup;
    # point DATABASE_URL at Postgres (e.g. postgresql+psycopg://...) in prod.
    database_url: str = f"sqlite:///{BACKEND_DIR / 'app.db'}"

    # CORS: the frontend dev origin(s) allowed to call the API.
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Confluence guideline cache folder (relative to backend/ unless absolute).
    confluence_dir: str = "confluence"

    # Interview notes output template.
    template_path: str = "templates/interview_notes_template.md"

    # Where uploaded resumes are briefly staged before redaction.
    upload_dir: str = "uploads"

    # Max upload size in bytes (default 10 MiB).
    max_upload_bytes: int = 10 * 1024 * 1024

    def resolve(self, value: str) -> Path:
        """Resolve a possibly-relative path against the backend directory."""
        path = Path(value)
        return path if path.is_absolute() else BACKEND_DIR / path

    @property
    def confluence_path(self) -> Path:
        return self.resolve(self.confluence_dir)

    @property
    def template_file(self) -> Path:
        return self.resolve(self.template_path)

    @property
    def upload_path(self) -> Path:
        return self.resolve(self.upload_dir)


@lru_cache
def get_settings() -> Settings:
    return Settings()

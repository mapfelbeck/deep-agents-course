"""Artifact storage seam.

Generated sheet and redacted resume markdown currently live in Postgres ``text``
columns via the ORM. This module centralizes read/write so large artifacts can be
moved to object storage later without touching the API or routers.
"""

from sqlalchemy.orm import Session

from app.models_db import Interview


def save_artifacts(
    db: Session,
    interview: Interview,
    *,
    sheet_md: str,
    resume_md: str | None,
) -> None:
    interview.sheet_md = sheet_md
    interview.resume_md = resume_md
    db.add(interview)
    db.commit()

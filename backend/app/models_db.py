"""ORM models: Interview, Job, Note.

Types are kept database-agnostic (String UUIDs, JSON arrays) so the same models
run on local SQLite and on Postgres in production without change.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(255), default="default", index=True)
    role: Mapped[str] = mapped_column(String(512))
    jd_paths: Mapped[list[str]] = mapped_column(JSON, default=list)
    candidate: Mapped[str | None] = mapped_column(String(512), nullable=True)
    sheet_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    # queued | generating | ready | error
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    created_at: Mapped[datetime] = mapped_column(default=_now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=_now, onupdate=_now, server_default=func.now()
    )

    job: Mapped["Job"] = relationship(
        back_populates="interview", uselist=False, cascade="all, delete-orphan"
    )
    note: Mapped["Note"] = relationship(
        back_populates="interview", uselist=False, cascade="all, delete-orphan"
    )


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    interview_id: Mapped[str] = mapped_column(
        ForeignKey("interviews.id", ondelete="CASCADE"), index=True
    )
    # queued | running | done | error
    status: Mapped[str] = mapped_column(String(32), default="queued")
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=_now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=_now, onupdate=_now, server_default=func.now()
    )

    interview: Mapped["Interview"] = relationship(back_populates="job")


class Note(Base):
    __tablename__ = "notes"

    interview_id: Mapped[str] = mapped_column(
        ForeignKey("interviews.id", ondelete="CASCADE"), primary_key=True
    )
    notes_md: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(
        default=_now, onupdate=_now, server_default=func.now()
    )

    interview: Mapped["Interview"] = relationship(back_populates="note")

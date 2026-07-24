"""Interview creation, listing, and detail endpoints."""

import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agent.runner import run_generation
from app.config import get_settings
from app.db import get_db
from app.deps import User, get_current_user
from app.models_db import Interview, Job, Note
from app.schemas import InterviewCreated, InterviewDetail, InterviewSummary

router = APIRouter(prefix="/api/interviews", tags=["interviews"])

ALLOWED_SUFFIXES = {".pdf", ".md"}


def _stage_upload(resume: UploadFile) -> tuple[Path, str]:
    """Validate and save the upload to the staging dir. Returns (path, candidate)."""
    settings = get_settings()
    original = Path(resume.filename or "resume")
    suffix = original.suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail="Only .pdf or .md resume files are accepted.",
        )

    data = resume.file.read()
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="Resume file is too large.")
    if not data:
        raise HTTPException(status_code=400, detail="Resume file is empty.")

    settings.upload_path.mkdir(parents=True, exist_ok=True)
    dest = settings.upload_path / f"{uuid.uuid4().hex}{suffix}"
    dest.write_bytes(data)
    return dest, original.stem


@router.post("", response_model=InterviewCreated, status_code=201)
def create_interview(
    background: BackgroundTasks,
    role: str = Form(...),
    resume: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> InterviewCreated:
    if not role.strip():
        raise HTTPException(status_code=400, detail="A role is required.")

    resume_path: Path | None = None
    candidate: str | None = None
    if resume is not None and resume.filename:
        resume_path, candidate = _stage_upload(resume)

    interview = Interview(
        user_id=user.id,
        role=role.strip(),
        candidate=candidate,
        jd_paths=[],
        status="queued",
    )
    job = Job(status="queued", interview=interview)
    note = Note(notes_md="", interview=interview)
    db.add_all([interview, job, note])
    db.commit()

    background.add_task(
        run_generation,
        interview.id,
        job.id,
        interview.role,
        str(resume_path) if resume_path else None,
    )
    return InterviewCreated(interview_id=interview.id, job_id=job.id)


@router.get("", response_model=list[InterviewSummary])
def list_interviews(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Interview]:
    stmt = (
        select(Interview)
        .where(Interview.user_id == user.id)
        .order_by(Interview.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def _get_owned(db: Session, interview_id: str, user: User) -> Interview:
    interview = db.get(Interview, interview_id)
    if interview is None or interview.user_id != user.id:
        raise HTTPException(status_code=404, detail="Interview not found.")
    return interview


@router.get("/{interview_id}", response_model=InterviewDetail)
def get_interview(
    interview_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> InterviewDetail:
    interview = _get_owned(db, interview_id, user)
    notes_md = interview.note.notes_md if interview.note else ""
    return InterviewDetail(
        id=interview.id,
        role=interview.role,
        candidate=interview.candidate,
        status=interview.status,
        created_at=interview.created_at,
        updated_at=interview.updated_at,
        jd_paths=interview.jd_paths,
        sheet_md=interview.sheet_md,
        resume_md=interview.resume_md,
        notes_md=notes_md,
    )

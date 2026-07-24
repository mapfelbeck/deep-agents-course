"""GET /api/jobs/{job_id} — poll generation status."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import User, get_current_user
from app.models_db import Job
from app.schemas import JobStatus

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobStatus)
def get_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Job:
    job = db.get(Job, job_id)
    if job is None or job.interview.user_id != user.id:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job

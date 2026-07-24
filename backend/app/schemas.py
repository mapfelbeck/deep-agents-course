"""Pydantic request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Role(BaseModel):
    value: str
    label: str
    paths: list[str]


class InterviewCreated(BaseModel):
    interview_id: str
    job_id: str


class JobStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    interview_id: str
    status: str
    error: str | None = None


class InterviewSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    role: str
    candidate: str | None = None
    status: str
    created_at: datetime


class InterviewDetail(InterviewSummary):
    jd_paths: list[str]
    sheet_md: str | None = None
    resume_md: str | None = None
    notes_md: str = ""
    updated_at: datetime


class NotesIn(BaseModel):
    notes_md: str


class NotesOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    interview_id: str
    notes_md: str
    updated_at: datetime

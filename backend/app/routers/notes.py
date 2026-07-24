"""GET/PUT /api/interviews/{id}/notes — read and autosave interviewer notes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import User, get_current_user
from app.models_db import Interview, Note
from app.schemas import NotesIn, NotesOut

router = APIRouter(prefix="/api/interviews", tags=["notes"])


def _get_owned(db: Session, interview_id: str, user: User) -> Interview:
    interview = db.get(Interview, interview_id)
    if interview is None or interview.user_id != user.id:
        raise HTTPException(status_code=404, detail="Interview not found.")
    return interview


@router.get("/{interview_id}/notes", response_model=NotesOut)
def get_notes(
    interview_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Note:
    interview = _get_owned(db, interview_id, user)
    note = interview.note
    if note is None:
        note = Note(interview_id=interview.id, notes_md="")
        db.add(note)
        db.commit()
    return note


@router.put("/{interview_id}/notes", response_model=NotesOut)
def save_notes(
    interview_id: str,
    payload: NotesIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Note:
    interview = _get_owned(db, interview_id, user)
    note = interview.note
    if note is None:
        note = Note(interview_id=interview.id)
        db.add(note)
    note.notes_md = payload.notes_md
    db.commit()
    db.refresh(note)
    return note

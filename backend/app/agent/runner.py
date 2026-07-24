"""Background generation pipeline.

Wraps the existing ``interview_notes_agent`` logic so the FastAPI backend can run
a generation as a background task and persist the result. Enforces resume
redaction and temp-file cleanup.
"""

from pathlib import Path

from deepagents import create_deep_agent

from app.agent.shared import ensure_confluence_cache, resume_to_markdown
from app.config import get_settings
from app.db import SessionLocal
from app.models_db import Interview, Job
from confluence_tool import import_confluence
from interview_notes_agent import (
    SYSTEM_PROMPT,
    build_user_message,
    find_job_descriptions,
    load_criteria,
    match_role,
)
from models import openai
from pdf_tool import convert_pdf_to_markdown


def _cleanup(resume_path: str | None) -> None:
    """Delete the staged upload and any markdown produced by PDF conversion."""
    if not resume_path:
        return
    src = Path(resume_path)
    src.unlink(missing_ok=True)
    if src.suffix.lower() == ".pdf":
        src.with_suffix(".md").unlink(missing_ok=True)


def run_generation(
    interview_id: str,
    job_id: str,
    role: str,
    resume_path: str | None,
) -> None:
    """Generate the interview sheet and persist it. Runs in a background thread."""
    settings = get_settings()
    db = SessionLocal()
    try:
        job = db.get(Job, job_id)
        interview = db.get(Interview, interview_id)
        if job is None or interview is None:
            return
        job.status = "running"
        interview.status = "generating"
        db.commit()

        confluence_dir = settings.confluence_path
        ensure_confluence_cache(confluence_dir)

        job_descs = find_job_descriptions(confluence_dir)
        matched_jds, available = match_role(role, job_descs, confluence_dir)
        if not matched_jds:
            roles_list = ", ".join(available)
            raise RuntimeError(
                f"No job description matched role '{role}'. Available: {roles_list}"
            )

        template = settings.template_file.read_text(encoding="utf-8")
        resume_md = (
            resume_to_markdown(Path(resume_path)) if resume_path else None
        )
        criteria = load_criteria(confluence_dir, matched_jds)

        agent = create_deep_agent(
            model=openai,
            tools=[import_confluence, convert_pdf_to_markdown],
            system_prompt=SYSTEM_PROMPT,
        )
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": build_user_message(
                            role,
                            matched_jds,
                            confluence_dir,
                            resume_md,
                            criteria,
                            template,
                        ),
                    }
                ]
            }
        )
        sheet_md = result["messages"][-1].content

        interview.sheet_md = sheet_md
        interview.resume_md = resume_md
        interview.jd_paths = [
            str(p.relative_to(confluence_dir)) for p in matched_jds
        ]
        interview.status = "ready"
        job.status = "done"
        job.error = None
        db.commit()
    except Exception as exc:  # noqa: BLE001 - record failure, don't crash worker
        db.rollback()
        job = db.get(Job, job_id)
        interview = db.get(Interview, interview_id)
        if job is not None:
            job.status = "error"
            job.error = str(exc)
        if interview is not None:
            interview.status = "error"
        db.commit()
    finally:
        _cleanup(resume_path)
        db.close()

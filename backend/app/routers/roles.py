"""GET /api/roles — selectable roles from the Confluence Job Descriptions."""

from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas import Role

from interview_notes_agent import find_job_descriptions, role_label, slugify
from app.agent.shared import ensure_confluence_cache

router = APIRouter(prefix="/api", tags=["roles"])


@router.get("/roles", response_model=list[Role])
def list_roles() -> list[Role]:
    settings = get_settings()
    confluence_dir = settings.confluence_path

    try:
        ensure_confluence_cache(confluence_dir)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=503,
            detail=f"Confluence guidelines are unavailable: {exc}",
        ) from exc

    job_descs = find_job_descriptions(confluence_dir)

    # De-duplicate by label, collecting the matching file paths per role.
    by_label: dict[str, list[str]] = {}
    for path in job_descs:
        label = role_label(path, confluence_dir)
        rel = str(path.relative_to(confluence_dir))
        by_label.setdefault(label, []).append(rel)

    roles = [
        Role(value=slugify(label), label=label, paths=sorted(paths))
        for label, paths in sorted(by_label.items())
    ]
    return roles

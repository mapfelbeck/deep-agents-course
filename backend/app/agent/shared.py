"""Shared agent helpers used by both the CLI agents and the web backend.

Extracted (Phase 0 of the site plan) so the interview flow no longer depends on
``resume_agent`` as a module. No behavior change for the CLI: the helpers keep
the same names and semantics.
"""

import time
from pathlib import Path

from confluence_tool import import_confluence
from pdf_tool import convert_pdf_to_markdown
from pii_redact import redact as redact_text

# Confluence root page for the Slalom hiring/interview guidelines.
CONFLUENCE_ROOT_PAGE_ID = "56819899"

# Rough character budget for the concatenated criteria passed to the model.
CRITERIA_CHAR_BUDGET = 120_000

# How long the cached Confluence guidelines are considered fresh before they are
# re-imported. Defaults to 7 days.
CONFLUENCE_CACHE_TTL_SECONDS = 7 * 24 * 60 * 60


def _cache_age_seconds(confluence_dir: Path) -> float | None:
    """Return the age in seconds of the freshest cached Markdown file.

    Returns None when the cache is missing or contains no Markdown files.
    """
    if not confluence_dir.is_dir():
        return None
    mtimes = [p.stat().st_mtime for p in confluence_dir.rglob("*.md")]
    if not mtimes:
        return None
    return max(0.0, time.time() - max(mtimes))


def ensure_confluence_cache(
    confluence_dir: Path,
    ttl_seconds: int = CONFLUENCE_CACHE_TTL_SECONDS,
) -> None:
    """Ensure a local Confluence guideline cache exists and is reasonably fresh.

    - If the cache is missing/empty, import it (requires Confluence credentials).
    - If the cache exists but is older than ``ttl_seconds``, attempt a refresh but
      keep using the existing cache when the refresh fails (e.g. offline).
    """
    age = _cache_age_seconds(confluence_dir)
    if age is not None and age < ttl_seconds:
        return

    cache_present = age is not None
    try:
        result = import_confluence.invoke(
            {"page_id": CONFLUENCE_ROOT_PAGE_ID, "out": str(confluence_dir)}
        )
        print(f"[info] {result}")
    except Exception as exc:  # noqa: BLE001 - refresh is best-effort
        if not cache_present:
            raise RuntimeError(
                f"Confluence cache '{confluence_dir}' is missing and the import "
                f"failed: {exc}"
            ) from exc
        print(
            f"[warn] could not refresh Confluence cache '{confluence_dir}' "
            f"({exc}); using existing cached files."
        )


def resume_to_markdown(resume_path: Path) -> str:
    """Return the resume content as Markdown, converting from PDF when needed.

    In all cases the returned text is PII-redacted before it reaches the agent.
    """
    if not resume_path.is_file():
        raise FileNotFoundError(f"Resume file not found: {resume_path}")

    suffix = resume_path.suffix.lower()
    if suffix == ".md":
        # Read and redact in-memory; do NOT modify the source .md file.
        return redact_text(resume_path.read_text(encoding="utf-8"))
    elif suffix == ".pdf":
        print(f"[info] Converting PDF resume '{resume_path}' to Markdown (redacted)...")
        result = convert_pdf_to_markdown.invoke({"input_path": str(resume_path)})
        print(f"[info] {result}")
        md_path = resume_path.with_suffix(".md")
        if not md_path.is_file():
            raise RuntimeError(f"PDF conversion did not produce '{md_path}'.")
        # The converted .md is already redacted (redact defaults to True).
        return md_path.read_text(encoding="utf-8")
    else:
        raise ValueError(
            f"Unsupported resume type '{suffix}'. Provide a .md or .pdf file."
        )

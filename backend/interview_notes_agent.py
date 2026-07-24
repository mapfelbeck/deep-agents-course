### Netskope workaround ###
import truststore
truststore.inject_into_ssl()
###########################

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import argparse
import re
import sys
from pathlib import Path

from deepagents import create_deep_agent

from models import openai
from confluence_tool import import_confluence
from pdf_tool import convert_pdf_to_markdown
from app.agent.shared import (
    CONFLUENCE_ROOT_PAGE_ID,
    CRITERIA_CHAR_BUDGET,
    ensure_confluence_cache,
    resume_to_markdown,
)

# Folders (relative to confluence/) that carry the strongest question / rubric /
# interview-structure signal. The matched job description is always loaded first;
# these provide the surrounding question banks and guidance.
PRIORITY_DIR_KEYWORDS = (
    "Sample Questions and Scripts",
    "Interviewing Guidance",
    "Interview Process",
)

# Default template path (relative to this file's directory).
DEFAULT_TEMPLATE = "templates/interview_notes_template.md"

SYSTEM_PROMPT = (
    "You are an interview-prep assistant for a Slalom interviewer. You build a "
    "prep sheet of NOTES and QUESTIONS the interviewer takes into an interview.\n\n"
    "Use ONLY the provided Slalom guidelines, the matched job description, and the "
    "sample questions (all sourced from Confluence). Do not invent Slalom process "
    "or criteria.\n\n"
    "Inputs you receive:\n"
    "- The target ROLE and the matched job description's required skills.\n"
    "- Optionally the candidate RESUME (Markdown, PII-redacted). It may be absent.\n"
    "- Slalom sample questions / interviewing guidance.\n"
    "- An output TEMPLATE you must fill in.\n\n"
    "Rules for the questions:\n"
    "1. Group questions by technology / skill / subject as appropriate.\n"
    "2. Within each technology/skill section, order questions from EASIEST to "
    "HARDEST (increasing difficulty).\n"
    "3. Every question must serve one of two purposes, and you must label which:\n"
    "   - (verify resume skill): confirm a skill the candidate claims on the "
    "resume. Only use when a resume was provided.\n"
    "   - (confirm role skill): confirm a skill required by the job description.\n"
    "4. When a resume is provided, cross-reference the resume's skills against the "
    "role requirements: probe claimed strengths deeply and explore gaps.\n"
    "5. When NO resume is provided, produce a role-based question bank covering the "
    "job description's required skills, and note in the Candidate Snapshot section "
    "that no resume was provided.\n\n"
    "You have tools (import_confluence, convert_pdf_to_markdown) available if you "
    "need to refresh the cached guidelines or convert a PDF, but normally the role, "
    "resume, and criteria are already provided in the message.\n\n"
    "Fill in the provided output TEMPLATE exactly, preserving its structure and "
    "headings. Cite the Confluence source file paths you used in the Sources "
    "section."
)


def _norm(text: str) -> str:
    """Lowercase and collapse non-alphanumerics to single spaces for matching."""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def find_job_descriptions(confluence_dir: Path) -> list[Path]:
    """Return all Markdown files that live under a 'Job Descriptions' folder."""
    return sorted(
        p
        for p in confluence_dir.rglob("*.md")
        if any(
            "job descriptions" in part.lower()
            for part in p.relative_to(confluence_dir).parts[:-1]
        )
    )


def role_label(path: Path, confluence_dir: Path) -> str:
    """Human-friendly role label derived from a job-description file path.

    Uses the file stem, or the parent folder name when the stem is a generic
    container name like 'Job Descriptions'.
    """
    stem = path.stem
    if _norm(stem) in ("job descriptions",):
        return path.parent.name
    return stem


def match_role(role: str, job_descs: list[Path], confluence_dir: Path):
    """Find the best-matching job description(s) for the requested role.

    Returns (matched_paths, available_labels). matched_paths is empty when no
    reasonable match is found.
    """
    role_tokens = set(_norm(role).split())
    labels: list[tuple[Path, str]] = [
        (p, role_label(p, confluence_dir)) for p in job_descs
    ]

    scored: list[tuple[float, Path, str]] = []
    for path, label in labels:
        rel_norm = _norm(str(path.relative_to(confluence_dir)))
        label_norm = _norm(label)
        label_tokens = set(label_norm.split()) | set(rel_norm.split())

        if not role_tokens:
            score = 0.0
        elif _norm(role) == label_norm:
            score = 1.0
        elif _norm(role) in rel_norm:
            score = 0.9
        else:
            overlap = len(role_tokens & label_tokens)
            score = overlap / len(role_tokens)
        if score > 0:
            scored.append((score, path, label))

    scored.sort(key=lambda t: (-t[0], len(str(t[1]))))
    available = sorted({label for _, label in labels})

    if not scored or scored[0][0] < 0.5:
        return [], available

    best_score = scored[0][0]
    matched = [path for score, path, _ in scored if score == best_score]
    return matched, available


def load_criteria(
    confluence_dir: Path,
    matched_jds: list[Path],
    char_budget: int = CRITERIA_CHAR_BUDGET,
) -> str:
    """Concatenate the matched JD(s) first, then the highest-signal question /
    guidance Markdown files, within a character budget."""
    all_md = sorted(confluence_dir.rglob("*.md"))

    def is_priority(path: Path) -> bool:
        rel = str(path.relative_to(confluence_dir))
        return any(keyword in rel for keyword in PRIORITY_DIR_KEYWORDS)

    matched_set = set(matched_jds)
    priority = [p for p in all_md if p not in matched_set and is_priority(p)]
    others = [p for p in all_md if p not in matched_set and not is_priority(p)]
    ordered = list(matched_jds) + priority + others

    chunks: list[str] = []
    used = 0
    for path in ordered:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:  # noqa: BLE001 - skip unreadable files
            print(f"[warn] could not read '{path}' ({exc}); skipping")
            continue
        rel = path.relative_to(confluence_dir)
        header = f"\n\n===== FILE: {rel} =====\n\n"
        block = header + text
        if used + len(block) > char_budget:
            remaining = char_budget - used
            if remaining <= len(header):
                break
            chunks.append(block[:remaining])
            print("[warn] criteria char budget reached; remaining files truncated.")
            break
        chunks.append(block)
        used += len(block)

    return "".join(chunks)


def build_user_message(
    role: str,
    matched_jds: list[Path],
    confluence_dir: Path,
    resume_md: str | None,
    criteria: str,
    template: str,
) -> str:
    jd_paths = "\n".join(
        f"- {p.relative_to(confluence_dir)}" for p in matched_jds
    )
    if resume_md is not None:
        resume_section = (
            "===== CANDIDATE RESUME (Markdown, PII-redacted) =====\n\n"
            f"{resume_md}\n"
        )
    else:
        resume_section = (
            "===== CANDIDATE RESUME =====\n\n"
            "No resume was provided. Produce a role-based question bank covering "
            "the job description's required skills, and state in the Candidate "
            "Snapshot section that no resume was provided.\n"
        )

    return (
        "Prepare an interviewer prep sheet (notes + questions) for the following "
        "interview.\n\n"
        f"===== TARGET ROLE =====\n\n{role}\n\n"
        f"Matched Slalom job description file(s):\n{jd_paths}\n\n"
        f"{resume_section}\n"
        "===== SLALOM GUIDELINES, JOB DESCRIPTION & SAMPLE QUESTIONS (Markdown) =====\n\n"
        f"{criteria}\n\n"
        "===== OUTPUT TEMPLATE (fill this in, preserving structure) =====\n\n"
        f"{template}\n"
    )


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "role"


def write_notes(
    notes: str,
    resume_path: Path | None,
    role: str,
    interview_dir: Path,
) -> Path:
    interview_dir.mkdir(parents=True, exist_ok=True)
    if resume_path is not None:
        stem = resume_path.stem
    else:
        stem = slugify(role)
    dest = interview_dir / f"{stem}-interview-notes.md"
    dest.write_text(notes, encoding="utf-8")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an interviewer prep sheet (notes + questions) from Slalom's "
            "interview process, a target role, and optionally a candidate resume."
        )
    )
    parser.add_argument(
        "--role",
        required=True,
        help="The role the interview is for (must match a Confluence job description).",
    )
    parser.add_argument(
        "--resume",
        default=None,
        help="Optional path to the candidate resume (.md or .pdf).",
    )
    parser.add_argument(
        "--confluence-dir",
        default="confluence",
        help="Folder holding cached Confluence guideline markdown (default: confluence)",
    )
    parser.add_argument(
        "--output-dir",
        default="interviews",
        help="Folder to write the interview prep sheet into (default: interviews)",
    )
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE,
        help=f"Output template markdown file (default: {DEFAULT_TEMPLATE})",
    )
    args = parser.parse_args()

    confluence_dir = Path(args.confluence_dir)
    interview_dir = Path(args.output_dir)
    template_path = Path(args.template)
    resume_path = Path(args.resume) if args.resume else None

    try:
        ensure_confluence_cache(confluence_dir)

        job_descs = find_job_descriptions(confluence_dir)
        if not job_descs:
            raise RuntimeError(
                f"No job descriptions found under '{confluence_dir}'."
            )
        matched_jds, available = match_role(args.role, job_descs, confluence_dir)
        if not matched_jds:
            roles_list = "\n".join(f"  - {r}" for r in available)
            raise RuntimeError(
                f"No job description matched role '{args.role}'.\n"
                f"Available roles:\n{roles_list}"
            )
        print(
            "[info] Matched role to: "
            + ", ".join(str(p.relative_to(confluence_dir)) for p in matched_jds)
        )

        if not template_path.is_file():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        template = template_path.read_text(encoding="utf-8")

        resume_md = resume_to_markdown(resume_path) if resume_path else None

        criteria = load_criteria(confluence_dir, matched_jds)
    except Exception as exc:  # noqa: BLE001 - surface a clean CLI error
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    agent = create_deep_agent(
        model=openai,
        tools=[import_confluence, convert_pdf_to_markdown],
        system_prompt=SYSTEM_PROMPT,
    )

    print("[info] Generating interview prep sheet...")
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": build_user_message(
                        args.role,
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
    notes = result["messages"][-1].content

    print("\n" + "=" * 72 + "\n")
    print(notes)
    print("\n" + "=" * 72 + "\n")

    dest = write_notes(notes, resume_path, args.role, interview_dir)
    print(f"[info] Interview prep sheet written to '{dest}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

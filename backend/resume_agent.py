### Netskope workaround ###
import truststore
truststore.inject_into_ssl()
###########################

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import argparse
import sys
from pathlib import Path

from deepagents import create_deep_agent

from models import openai
from confluence_tool import import_confluence
from pdf_tool import convert_pdf_to_markdown
from pii_redact import redact as redact_text

# Confluence root page for the Slalom hiring/interview guidelines.
CONFLUENCE_ROOT_PAGE_ID = "56819899"

# Folders (relative to confluence/) that carry the strongest role / seniority /
# evaluation signal. Used to keep the criteria context within model limits.
PRIORITY_DIR_KEYWORDS = (
    "Job Descriptions",
    "Interviewing Guidance",
    "Interview Process",
    "Sample Questions and Scripts",
)

# Rough character budget for the concatenated criteria passed to the model.
CRITERIA_CHAR_BUDGET = 120_000

SYSTEM_PROMPT = (
    "You are a Slalom hiring evaluator. You assess a candidate resume STRICTLY "
    "against the provided Slalom interview guidelines and job descriptions "
    "(sourced from Confluence). Do not invent criteria that are not supported by "
    "the guidelines.\n\n"
    "Your tasks:\n"
    "1. Identify the Slalom discipline/role the resume best matches (e.g. Software "
    "Engineering, Data Engineering, Quality Engineering, Platform Engineering, "
    "Experience Design, Solution Ownership) using the Job Descriptions.\n"
    "2. Recommend a seniority level consistent with Slalom's descriptions "
    "(e.g. Consultant / Senior Consultant / Principal, as found in the docs).\n"
    "3. Justify the recommendation with concrete evidence from the resume mapped "
    "to specific guideline requirements.\n"
    "4. Flag notable gaps or missing signals.\n\n"
    "You have tools available (import_confluence, convert_pdf_to_markdown) if you "
    "need to refresh the cached guidelines or convert a PDF, but normally the "
    "resume and criteria are already provided in the message.\n\n"
    "Produce a SHORT, structured Markdown report in exactly this format:\n\n"
    "# Resume Evaluation — <candidate name or file>\n\n"
    "## Recommended Role\n<discipline / role>\n\n"
    "## Recommended Seniority\n<level>\n\n"
    "## Rationale\n- <evidence mapped to a guideline requirement>\n\n"
    "## Strengths\n- ...\n\n"
    "## Gaps / Risks\n- ...\n\n"
    "## Sources\n- <confluence file paths referenced>\n\n"
    "Keep the whole report to about one screen."
)


def ensure_confluence_cache(confluence_dir: Path) -> None:
    """Ensure the criteria cache exists; import it from Confluence if missing/empty."""
    has_markdown = confluence_dir.is_dir() and any(confluence_dir.rglob("*.md"))
    if has_markdown:
        print(f"[info] Using cached guidelines in '{confluence_dir}'.")
        return

    print(f"[info] '{confluence_dir}' missing or empty; importing from Confluence...")
    result = import_confluence.invoke(
        {"page_id": CONFLUENCE_ROOT_PAGE_ID, "out": str(confluence_dir)}
    )
    print(f"[info] {result}")

    if not (confluence_dir.is_dir() and any(confluence_dir.rglob("*.md"))):
        raise RuntimeError(
            f"Confluence import did not produce any Markdown in '{confluence_dir}'."
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


def load_criteria(confluence_dir: Path, char_budget: int = CRITERIA_CHAR_BUDGET) -> str:
    """Concatenate the highest-signal guideline Markdown files within a char budget."""
    all_md = sorted(confluence_dir.rglob("*.md"))

    def is_priority(path: Path) -> bool:
        rel = str(path.relative_to(confluence_dir))
        return any(keyword in rel for keyword in PRIORITY_DIR_KEYWORDS)

    priority = [p for p in all_md if is_priority(p)]
    others = [p for p in all_md if not is_priority(p)]
    ordered = priority + others

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
            used = char_budget
            print("[warn] criteria char budget reached; remaining files truncated.")
            break
        chunks.append(block)
        used += len(block)

    return "".join(chunks)


def build_user_message(resume_md: str, criteria: str) -> str:
    return (
        "Evaluate the following candidate resume against the Slalom interview "
        "guidelines and job descriptions provided below. Recommend the best-fit "
        "role and seniority, and produce the short structured report as instructed.\n\n"
        "===== RESUME (Markdown) =====\n\n"
        f"{resume_md}\n\n"
        "===== SLALOM GUIDELINES & JOB DESCRIPTIONS (Markdown) =====\n\n"
        f"{criteria}\n"
    )


def write_report(report: str, resume_path: Path, report_dir: Path) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    dest = report_dir / f"{resume_path.stem}-evaluation.md"
    dest.write_text(report, encoding="utf-8")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate a resume against Slalom interview guidelines."
    )
    parser.add_argument(
        "--resume", required=True, help="Path to the resume (.md or .pdf)"
    )
    parser.add_argument(
        "--confluence-dir",
        default="confluence",
        help="Folder holding cached Confluence guideline markdown (default: confluence)",
    )
    parser.add_argument(
        "--output-dir",
        default="reports",
        help="Folder to write the evaluation report into (default: reports)",
    )
    args = parser.parse_args()

    resume_path = Path(args.resume)
    confluence_dir = Path(args.confluence_dir)
    report_dir = Path(args.report_dir)

    try:
        ensure_confluence_cache(confluence_dir)
        resume_md = resume_to_markdown(resume_path)
        criteria = load_criteria(confluence_dir)
    except Exception as exc:  # noqa: BLE001 - surface a clean CLI error
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    agent = create_deep_agent(
        model=openai,
        tools=[import_confluence, convert_pdf_to_markdown],
        system_prompt=SYSTEM_PROMPT,
    )

    print("[info] Evaluating resume...")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": build_user_message(resume_md, criteria)}]}
    )
    report = result["messages"][-1].content

    print("\n" + "=" * 72 + "\n")
    print(report)
    print("\n" + "=" * 72 + "\n")

    dest = write_report(report, resume_path, report_dir)
    print(f"[info] Report written to '{dest}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

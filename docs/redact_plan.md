# PII Redaction Plan

This plan evolves the existing Presidio-based redaction helper into a reusable
building block, wires it into the PDF converter and the resume agent, and
exposes it as a LangChain tool.

Everything runs locally with `presidio-analyzer` / `presidio-anonymizer` and
spaCy (`en_core_web_lg`), already used by the current `pii_redact.py`. No
network or API keys are required.

## Files involved

| File | Current state | After this plan |
| --- | --- | --- |
| `backend/pii_redact.py` | `redact_with_mapping` (returns text + mapping), `unredact` | Adds `redact()` that returns only the redacted text |
| `backend/pii_tool.py` | Empty | LangChain `@tool` wrapping `redact()` for raw strings |
| `backend/pdf_converter.py` | `convert_pdf(input_path, output_path=None)` | Adds `redact: bool = True` arg; redacts Markdown before writing |
| `backend/pdf_tool.py` | `convert_pdf_to_markdown(input_path, output_path=None)` | Adds `redact: bool = True` param, passed through to `convert_pdf` |
| `backend/resume_agent.py` | Converts PDFs, reads `.md` resumes verbatim | Redacts PDF text on conversion and redacts `.md` resume text in-memory before evaluation |

## Design decisions (confirmed)

- New mapping-free function is named **`redact`**.
- New boolean arg on `convert_pdf` is named **`redact`**, defaulting to **`True`**.
- When `resume_agent` reads a `.md` resume, it redacts **in-memory only** and
  does **not** modify the `.md` file on disk.
- The LangChain `convert_pdf_to_markdown` tool **exposes** the `redact` flag
  (default `True`), passing it through to `convert_pdf`.
- The `pii_tool` LangChain tool takes a **raw text string** and returns the
  **redacted string** (no mapping, not reversible).

---

## Task 1 — Add `redact()` to `pii_redact.py`

Add a thin wrapper around the existing `redact_with_mapping` that discards the
mapping and returns only the redacted text. Keep `redact_with_mapping` and
`unredact` unchanged so reversible workflows still work.

Add this function after `redact_with_mapping` (and before `unredact`):

```python
def redact(text: str, language: str = "en", score_threshold: float = 0.35) -> str:
    """Redact PII in `text` and return only the redacted text (no mapping).

    This is a convenience wrapper over `redact_with_mapping` for callers that
    do not need to reverse the redaction.

    Args:
        text: The text to redact.
        language: Presidio language code (default "en").
        score_threshold: Minimum confidence score for a detection to be
            redacted (default 0.35).

    Returns:
        The redacted text.
    """
    redacted, _mapping = redact_with_mapping(
        text, language=language, score_threshold=score_threshold
    )
    return redacted
```

Notes:
- Reuses the exact same detection/threshold behavior as `redact_with_mapping`,
  so the two stay consistent.
- The tokens produced are deterministic (SHA1-based), so identical inputs yield
  identical redacted output.

---

## Task 2 — Make `pii_tool.py` a LangChain tool

Write the code below into `backend/pii_tool.py`. It mirrors the structure of
`backend/pdf_tool.py` and `backend/confluence_tool.py` (import a function, wrap
it with `@tool`, return a friendly string, catch exceptions).

```python
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_core.tools import tool

from pii_redact import redact


@tool
def redact_pii(text: str) -> str:
    """Redact personally identifiable information (PII) from a text string.

    Detects and replaces PII (names, emails, phone numbers, addresses,
    LinkedIn/GitHub/personal URLs, etc.) with deterministic placeholder
    tokens. The redaction is one-way (no mapping is returned).

    Args:
        text: The raw text to redact.

    Returns:
        The redacted text, or an error message if redaction fails.
    """
    try:
        return redact(text)
    except Exception as e:
        return f"Error redacting text: {e}"
```

Notes:
- Returns the redacted string directly (the common case for an LLM tool that
  wants sanitized text back).
- On failure it returns an error string rather than raising, matching the
  behavior of the other tools in this repo.

---

## Task 3 — Add a `redact` flag to `convert_pdf`

Update `backend/pdf_converter.py` so `convert_pdf` optionally redacts the
extracted Markdown before writing it to disk.

Changes:
- Add `redact: bool = True` as the third parameter.
- When `redact` is `True`, run the extracted Markdown through
  `pii_redact.redact()` before writing.
- Import `redact` lazily (inside the function) or at module top; a top-level
  import is fine since `pdf_converter.py` already lives alongside
  `pii_redact.py`.

Updated function:

```python
import argparse
from pathlib import Path

import pymupdf4llm  # helper built on top of PyMuPDF

from pii_redact import redact as redact_text


def convert_pdf(
    input_path: str,
    output_path: str | None = None,
    redact: bool = True,
) -> str:
    """Convert a single PDF file to Markdown.

    Args:
        input_path: Path to the source PDF file.
        output_path: Where to write the Markdown. If omitted, uses the input
            path with a ".md" extension.
        redact: When True (default), redact PII from the extracted Markdown
            before writing it to disk.

    Returns:
        The path to the written Markdown file (as a string).
    """
    src = Path(input_path)
    if not src.is_file():
        raise FileNotFoundError(f"Input PDF not found: {src}")

    dest = Path(output_path) if output_path else src.with_suffix(".md")

    markdown = pymupdf4llm.to_markdown(str(src))
    if redact:
        markdown = redact_text(markdown)
    dest.write_text(markdown, encoding="utf-8")
    return str(dest)
```

CLI:
- Add an opt-out flag so redaction can be disabled from the command line, e.g.
  `--no-redact` (using `argparse.BooleanOptionalAction` or a
  `store_false` dest), keeping the default behavior redacted:

```python
    parser.add_argument(
        "--no-redact",
        dest="redact",
        action="store_false",
        help="Disable PII redaction of the extracted Markdown (default: redact)",
    )
    parser.set_defaults(redact=True)
    ...
    dest = convert_pdf(args.input, args.output, redact=args.redact)
```

Note: `redact_text` is the imported alias for `pii_redact.redact` to avoid a
name clash with the `redact` parameter.

---

## Task 4 — Pass `redact` through `pdf_tool.py`

Expose the flag on the LangChain tool so callers (including the agent) can
control it, defaulting to redacted.

```python
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_core.tools import tool

from pdf_converter import convert_pdf


@tool
def convert_pdf_to_markdown(
    input_path: str,
    output_path: str | None = None,
    redact: bool = True,
) -> str:
    """Convert a single PDF file into a Markdown file on disk.

    Args:
        input_path: Path to the source PDF file to convert.
        output_path: Optional path for the Markdown output. If omitted, the
            output is written next to the source PDF using the same name with a
            ".md" extension.
        redact: When True (default), PII is redacted from the extracted text
            before the Markdown file is written.

    Returns:
        A summary describing where the Markdown file was written.
    """
    try:
        dest = convert_pdf(input_path, output_path, redact=redact)
        return f"Successfully converted '{input_path}' to Markdown at '{dest}'."
    except Exception as e:
        return f"Error converting PDF '{input_path}': {e}"
```

---

## Task 5 — Redact in `resume_agent.py`

Two paths feed resume text into the agent (`resume_to_markdown`):

1. **PDF resumes** — converted via `convert_pdf_to_markdown`, which now redacts
   by default (Task 3/4). The written `.md` is already redacted, and the text
   returned to the agent is redacted.
2. **`.md` resumes** — currently read verbatim. These must be redacted
   **in-memory** before evaluation, without modifying the file on disk.

Update `resume_to_markdown` to redact the `.md` branch:

```python
from pii_redact import redact as redact_text  # add to imports at top of file


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
```

Notes:
- The PDF branch relies on `convert_pdf_to_markdown`'s default `redact=True`, so
  the on-disk `.md` and the returned text are both redacted.
- The `.md` branch redacts only in memory, leaving the original file untouched
  per the confirmed decision.
- No changes are needed to `build_user_message` or the system prompt; the model
  simply receives already-sanitized resume text.

---

## Verification

1. **Unit-style check of `redact`:**
   ```bash
   cd backend
   python -c "from pii_redact import redact; print(redact('Email: john@example.com, GitHub: github.com/jpublic'))"
   ```
   Expect emails / URLs replaced with `[EMAIL_ADDRESS_xxxxxxxx]` /
   `[GITHUB_xxxxxxxx]`-style tokens.

2. **PII tool:**
   ```bash
   python -c "from pii_tool import redact_pii; print(redact_pii.invoke({'text': 'Call me at (555) 123-4567'}))"
   ```

3. **PDF conversion (redacted by default):** convert a sample resume PDF and
   confirm the resulting `.md` contains redaction tokens instead of real PII.
   Confirm `--no-redact` produces un-redacted output.

4. **Resume agent end-to-end:** run
   `python resume_agent.py --resume <sample>.md` and confirm the resume content
   embedded in the evaluation is redacted, while the original `.md` on disk is
   unchanged.

## Out of scope

- No reverse/unredaction step is added to the agent flow; `unredact` remains
  available for callers that use `redact_with_mapping` directly.
- No batch/directory redaction mode.
- No changes to Presidio recognizers or score thresholds beyond what already
  exists in `pii_redact.py`.

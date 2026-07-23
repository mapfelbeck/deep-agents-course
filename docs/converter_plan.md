# PDF → Markdown Converter Plan

This plan turns the existing PDF helper into (1) a command-line tool and (2) a
LangChain tool, then verifies both by converting the sample PDFs.

Everything runs locally with `pymupdf4llm` (already used in the current
`pdf_converter.py`). No network or API keys are required.

## Files involved

| File | Current state | After this plan |
| --- | --- | --- |
| `backend/pdf_converter.py` | Hardcoded script (`test.pdf` → `test.md`) | CLI tool with `--input` / `--output` |
| `backend/pdf_tool.py` | Empty | LangChain `@tool` wrapping the converter |
| `sample_data/*.pdf` | 4 sample PDFs | Used to verify conversion |

## Design decisions (already confirmed)

- Convert **one PDF file at a time** (no directory/batch mode).
- Verification output is written **next to the source PDFs** in `sample_data/`.
- The LangChain tool takes **just an input path** and auto-derives the `.md`
  output path (same name, `.md` extension). An optional output override is
  allowed but not required.

---

## Task 1 — Make `pdf_converter.py` a CLI tool

Replace the entire contents of `backend/pdf_converter.py` with the code below.

Requirements:
- Accept `--input` (required) and `--output` (optional).
- If `--output` is omitted, derive it from the input by swapping the extension
  to `.md` (e.g. `sample 1.pdf` → `sample 1.md`).
- Expose a reusable `convert_pdf(input_path, output_path=None) -> str` function
  so the LangChain tool (Task 2) can import and call it.
- Keep a `main()` + `if __name__ == "__main__":` block, matching the pattern in
  `confluence_import.py`.

```python
import argparse
from pathlib import Path

import pymupdf4llm  # helper built on top of PyMuPDF


def convert_pdf(input_path: str, output_path: str | None = None) -> str:
    """Convert a single PDF file to Markdown.

    Args:
        input_path: Path to the source PDF file.
        output_path: Where to write the Markdown. If omitted, uses the input
            path with a ".md" extension.

    Returns:
        The path to the written Markdown file (as a string).
    """
    src = Path(input_path)
    if not src.is_file():
        raise FileNotFoundError(f"Input PDF not found: {src}")

    dest = Path(output_path) if output_path else src.with_suffix(".md")

    markdown = pymupdf4llm.to_markdown(str(src))
    dest.write_text(markdown, encoding="utf-8")
    return str(dest)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to Markdown."
    )
    parser.add_argument("--input", required=True, help="Path to the source PDF file")
    parser.add_argument(
        "--output",
        default=None,
        help="Path to the output Markdown file (default: input name with .md)",
    )
    args = parser.parse_args()
    dest = convert_pdf(args.input, args.output)
    print(f"{dest} written")


if __name__ == "__main__":
    main()
```

### How to run it

```bash
cd backend
python pdf_converter.py --input sample.pdf --output sample.md
# or let the output name be derived automatically:
python pdf_converter.py --input sample.pdf
```

---

## Task 2 — Make `pdf_tool.py` a LangChain tool

Write the code below into `backend/pdf_tool.py`. It mirrors the structure of
`backend/confluence_tool.py` (import a function, wrap it with `@tool`, return a
friendly summary string, catch exceptions).

```python
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_core.tools import tool

from pdf_converter import convert_pdf


@tool
def convert_pdf_to_markdown(input_path: str, output_path: str | None = None) -> str:
    """Convert a single PDF file into a Markdown file on disk.

    Args:
        input_path: Path to the source PDF file to convert.
        output_path: Optional path for the Markdown output. If omitted, the
            output is written next to the source PDF using the same name with a
            ".md" extension.

    Returns:
        A summary describing where the Markdown file was written.
    """
    try:
        dest = convert_pdf(input_path, output_path)
        return f"Successfully converted '{input_path}' to Markdown at '{dest}'."
    except Exception as e:
        return f"Error converting PDF '{input_path}': {e}"
```

Notes for the implementer:
- The import is `from pdf_converter import convert_pdf` (same directory,
  matching how `confluence_tool.py` does `from confluence_import import
  run_export`).
- Do not re-implement conversion logic here; reuse `convert_pdf` from Task 1.

---

## Task 3 — Verify by converting the sample PDFs

The `sample_data/` folder contains: `sample 1.pdf`, `sample 2.pdf`,
`sample 3.pdf`, `sample 4.pdf`. Filenames contain spaces, so quote them.

### 3a. Verify the CLI

Run each conversion from the `backend/` directory, writing output next to the
source PDFs:

```bash
cd backend
python pdf_converter.py --input "../sample_data/sample 1.pdf"
python pdf_converter.py --input "../sample_data/sample 2.pdf"
python pdf_converter.py --input "../sample_data/sample 3.pdf"
python pdf_converter.py --input "../sample_data/sample 4.pdf"
```

Expected: `../sample_data/sample 1.md` … `sample 4.md` are created, and each
command prints `<path> written`.

### 3b. Verify the LangChain tool

Confirm the tool imports and runs. From `backend/`:

```bash
python -c "from pdf_tool import convert_pdf_to_markdown; print(convert_pdf_to_markdown.invoke({'input_path': '../sample_data/sample 1.pdf'}))"
```

Expected output (a success summary):

```
Successfully converted '../sample_data/sample 1.pdf' to Markdown at '../sample_data/sample 1.md'.
```

### 3c. Sanity-check the output

Confirm the generated Markdown files are non-empty and contain text:

```bash
ls -la ../sample_data/*.md
head -n 20 "../sample_data/sample 1.md"
```

Expected: `.md` files exist with a size greater than 0 and readable content.

---

## Acceptance checklist

- [ ] `python pdf_converter.py --input sample.pdf --output sample.md` works.
- [ ] Omitting `--output` derives the `.md` filename automatically.
- [ ] `convert_pdf()` is importable and returns the output path.
- [ ] `pdf_tool.py` exposes a `@tool` (`convert_pdf_to_markdown`) that reuses
      `convert_pdf` and returns a summary string, with errors caught.
- [ ] All four `sample_data/*.pdf` files convert to non-empty `.md` files.
- [ ] The LangChain tool runs via `.invoke({...})` and returns a success message.

## Dependencies

`pymupdf4llm` must be installed (it is already imported by the current
`pdf_converter.py`). If it is missing, install it:

```bash
pip install pymupdf4llm
```

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
    parser.add_argument(
        "--no-redact",
        dest="redact",
        action="store_false",
        help="Disable PII redaction of the extracted Markdown (default: redact)",
    )
    parser.set_defaults(redact=True)
    args = parser.parse_args()
    dest = convert_pdf(args.input, args.output, redact=args.redact)
    print(f"{dest} written")


if __name__ == "__main__":
    main()
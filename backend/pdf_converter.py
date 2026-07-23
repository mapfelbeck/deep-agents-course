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
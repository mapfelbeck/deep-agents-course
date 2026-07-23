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

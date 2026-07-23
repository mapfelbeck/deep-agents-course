import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_core.tools import tool

from confluence_import import run_export


@tool
def import_confluence(page_id: str = "56819899", out: str = "imported") -> str:
    """Import a Confluence page tree (the page and all its child pages) into a local
    folder as Markdown files.

    Args:
        page_id: The root Confluence page ID to import. Defaults to the standard page.
        out: The output directory to write the Markdown files into. Defaults to "imported".

    Returns:
        A summary of how many pages were imported and where they were written.
    """
    try:
        count = run_export(page_id, out)
        return f"Successfully imported {count} Confluence page(s) into '{out}'."
    except Exception as e:
        return f"Error importing Confluence page {page_id}: {e}"
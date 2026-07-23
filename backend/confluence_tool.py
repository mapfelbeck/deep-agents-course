import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from langchain_core.tools import tool

@tool
def import_confluence(doc_id: str) -> str:
    """Import a Confluence document by its ID."""
    try:
        return f"Successfully imported Confluence document with ID: {doc_id}"
    except Exception as e:
        return f"Error: {e}"
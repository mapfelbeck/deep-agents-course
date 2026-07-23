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

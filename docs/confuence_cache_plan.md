# Confluence Cache Plan — Wire Import into a LangChain Agent

## Purpose

Turn the existing Confluence exporter into three cooperating pieces:

1. **`confluence_import.py`** — stays a runnable CLI **and** exposes a reusable function.
2. **`confluence_tool.py`** — a LangChain `@tool` that calls that function directly.
3. **`langchain_test.py`** — a test script where a deep agent uses the tool to import Confluence data into the `imported` folder.

Keep every change small and mechanical. Do **not** rewrite working logic. Only refactor what these three tasks require.

---

## Design Decisions (already agreed — do not change)

- The tool calls a **Python function** inside `confluence_import.py` directly (no subprocess).
- The tool exposes two parameters: `page_id` and `out`, **each with a hardcoded default** (`page_id="56819899"`, `out="imported"`).
- The agent is only told *"import the confluence data"* — the defaults supply the actual values.
- On success the tool returns a **summary string**: number of pages exported + the output path.

---

## Task 1 — `backend/confluence_import.py`

### Goal
Add one reusable function `run_export(page_id, out)` that does exactly what `main()` does today, and returns the exported page count. Keep the CLI working unchanged.

### Steps

1. **Add a new function `run_export`** just above `main()`. It contains the body that `main()` currently runs, but takes arguments and **returns the count** instead of only printing:

   ```python
   def run_export(page_id: str, out: str = "output") -> int:
       """Export a Confluence page tree to Markdown. Returns number of pages exported."""
       conf = connect()
       count = [0]
       export_page(conf, page_id, Path(out), set(), set(), count)
       print(f"Done. Exported {count[0]} page(s).")
       return count[0]
   ```

2. **Simplify `main()`** so it just parses args and calls `run_export`:

   ```python
   def main():
       parser = argparse.ArgumentParser(
           description="Recursively export a Confluence page tree to local Markdown files."
       )
       parser.add_argument("--page-id", required=True, help="Root Confluence page ID to export")
       parser.add_argument("--out", default="output", help="Base output directory (default: output)")
       args = parser.parse_args()
       run_export(args.page_id, args.out)
   ```

3. **Leave everything else unchanged**, including:
   - The `truststore` block at the very top (keep it first).
   - `sanitize`, `connect`, `with_retries`, `get_all_children`, `html_to_markdown`, `write_text`, `unique_name`, `export_page`.
   - The `if __name__ == "__main__": main()` block at the bottom.

### Acceptance check for Task 1
The CLI still works exactly as before:

```bash
python confluence_import.py --page-id 56819899 --out output
```

---

## Task 2 — `backend/confluence_tool.py`

### Goal
Replace the placeholder tool with a real one that calls `run_export` and returns a summary string.

### Full replacement file contents

```python
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
```

### Notes for the implementer
- The `import_confluence` **function name stays the same** (already referenced elsewhere if needed).
- Defaults `page_id="56819899"` and `out="imported"` are intentional so the agent can call the tool with no arguments.
- Do **not** add a subprocess call — import and call `run_export` directly.

### Acceptance check for Task 2
This import must succeed without error from the `backend/` directory:

```bash
python -c "from confluence_tool import import_confluence; print(import_confluence.name)"
```
Expected output: `import_confluence`

---

## Task 3 — `backend/langchain_test.py`

### Goal
Make the agent use the tool to import the Confluence data into `imported`. The prompt only says *"import the confluence data"*; the tool defaults do the rest.

### Full replacement file contents

```python
### Netskope workaround ###
import truststore
truststore.inject_into_ssl()
##########################

from deepagents import create_deep_agent
from models import openai
from confluence_tool import import_confluence

agent = create_deep_agent(
    model=openai,
    tools=[import_confluence],
    system_prompt=(
        "You are a helpful assistant that imports Confluence documentation. "
        "When asked to import the confluence data, call the import_confluence tool."
    ),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Import the confluence data."}]}
)

print(result["messages"][-1].content)
```

### Notes for the implementer
- Keep the `truststore` block first, before any other imports.
- Pass the tool via `tools=[import_confluence]` — this is additive to the deep agent's built-in tools.
- Do not pass the page ID or the folder name in the prompt; the tool defaults handle them.

### Acceptance check for Task 3
Run from the `backend/` directory:

```bash
python langchain_test.py
```
Expected: the script runs, the agent calls the tool, an `imported/` folder is created with the exported Markdown tree, and the printed final message mentions the number of pages imported.

---

## Order of Implementation

1. Edit `confluence_import.py` (Task 1) and verify the CLI still works.
2. Replace `confluence_tool.py` (Task 2) and verify the import check.
3. Replace `langchain_test.py` (Task 3) and run the end-to-end test.

## Things NOT to change

- The `truststore` workaround blocks (must remain at the top of any file that has them).
- The Confluence connection logic and credentials handling (`connect()` reads from `.env`).
- Any of the export/markdown helper functions in `confluence_import.py`.
- `models.py` and `requirements.txt`.

## Prerequisites (already in place — just confirm)

- `.env` contains `CONFLUENCE_URL`, `ATLASSIAN_USER`, `ATLASSIAN_API_KEY`.
- Dependencies from `requirements.txt` are installed in the active environment.
- All three scripts are run from the `backend/` directory so that `from confluence_import import run_export`, `from confluence_tool import import_confluence`, and `from models import openai` resolve correctly.

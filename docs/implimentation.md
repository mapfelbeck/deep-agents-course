# Confluence → Local Markdown Exporter — Implementation Plan

## Goal

Build a Python tool that:

1. Connects to Confluence (Cloud) using API credentials.
2. Given a starting page ID, recursively downloads that page and **all descendant pages**.
3. Converts each page's storage-format (XHTML) body into Markdown.
4. Mirrors the Confluence page hierarchy as a local folder tree:
   - The **root folder** is named after the title of the starting page.
   - Each page produces a Markdown file inside its own folder, and the file is named the same as the page title.
   - Every child page repeats the same pattern (a folder named after the child title, containing a Markdown file named after the child title, and folders for its own children).

---

## 1. Environment & Dependencies

### Existing setup (already in the repo)

- `backend/read_confluence.py` — a working proof-of-concept that connects and fetches one page.
- `.env` file is loaded via `python-dotenv`. Required variables:
  - `CONFLUENCE_URL` — e.g. `https://your-domain.atlassian.net/wiki`
  - `ATLASSIAN_USER` — the account email.
  - `ATLASSIAN_API_KEY` — an Atlassian API token.
- `atlassian-python-api==4.0.7` is already installed and provides the `Confluence` client.
- `beautifulsoup4==4.15.0` is already installed.
- The file begins with a `truststore` block (corporate TLS interception workaround). **Keep this block verbatim at the very top of the new script**, before any network imports run.

### New dependency to add

Add a Markdown converter. Use **`markdownify`** (simple, HTML → Markdown, handles tables/lists well).

- Add to [backend/requirements.txt](../backend/requirements.txt):
  ```
  markdownify==0.13.1
  ```
- Install:
  ```bash
  pip install markdownify
  ```

> Note: Confluence "storage format" is XHTML with custom `<ac:...>` and `<ri:...>` macro tags. `markdownify` will strip unknown tags' wrappers but keep their text. This is acceptable for a first version. See "Known limitations" below.

---

## 2. File to Create

Create a new file: `backend/confluence_export.py`. Do **not** overwrite the existing `read_confluence.py`.

---

## 3. Confluence API — What to Call

Using the `Confluence` client from `atlassian.confluence`:

### 3.1 Connect

```python
confluence = Confluence(
    url=os.getenv("CONFLUENCE_URL"),
    username=os.getenv("ATLASSIAN_USER"),
    password=os.getenv("ATLASSIAN_API_KEY"),
)
```

### 3.2 Fetch a single page (title + body)

```python
page = confluence.get_page_by_id(page_id=page_id, expand="body.storage")
title = page["title"]
html_body = page["body"]["storage"]["value"]
```

### 3.3 Fetch child pages of a page

Use:

```python
children = confluence.get_page_child_by_type(
    page_id=page_id,
    type="page",
    start=0,
    limit=100,
)
```

- Returns a list of child page dicts; each has `"id"` and `"title"`.
- **Pagination:** if a page has more than 100 children, loop increasing `start` by `limit` until fewer than `limit` results are returned. Implement a helper `get_all_children(page_id)` that pages through everything and returns a combined list.

---

## 4. Core Algorithm (Recursive Traversal)

Depth-first recursion starting at the given root ID.

```
export_page(page_id, parent_dir):
    page   = get_page_by_id(page_id, expand="body.storage")
    title  = page["title"]
    html   = page["body"]["storage"]["value"]

    safe   = sanitize(title)
    page_dir = parent_dir / safe          # folder named after this page
    page_dir.mkdir(parents=True, exist_ok=True)

    md = html_to_markdown(html)
    md = f"# {title}\n\n" + md             # prepend title as H1 (optional but recommended)
    write_text(page_dir / f"{safe}.md", md)

    for child in get_all_children(page_id):
        export_page(child["id"], page_dir)   # recurse; children nest under page_dir
```

Entry point:

```
root_id = <the id passed in>
export_page(root_id, Path("output"))   # or a configurable base output dir
```

This yields exactly the required structure:

```
output/
└── <Root Title>/
    ├── <Root Title>.md
    ├── <Child A Title>/
    │   ├── <Child A Title>.md
    │   └── <Grandchild Title>/
    │       └── <Grandchild Title>.md
    └── <Child B Title>/
        └── <Child B Title>.md
```

> Design decision: the root folder lives under a top-level `output/` directory to keep the repo clean. If the user prefers the root folder created directly in the working directory, change the base dir to `Path(".")`.

---

## 5. Helper Functions to Implement

### 5.1 `sanitize(title: str) -> str`

Page titles can contain characters illegal in file/folder names (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) and leading/trailing whitespace or dots.

- Replace each illegal character with `_` (or a space).
- Strip leading/trailing whitespace and trailing dots.
- Collapse repeated whitespace to single spaces.
- If the result is empty, fall back to the page ID.
- Optionally truncate to a safe length (e.g. 150 chars) to avoid path-length issues.

Use a regex: `re.sub(r'[\\/:*?"<>|]', "_", title)`.

### 5.2 `html_to_markdown(html: str) -> str`

```python
from markdownify import markdownify as md
return md(html, heading_style="ATX")
```

- `heading_style="ATX"` produces `#`-style headings.
- Wrap in a try/except; on failure, fall back to writing the raw HTML so no content is silently lost, and log a warning.

### 5.3 `get_all_children(page_id: str) -> list[dict]`

Paginate through `get_page_child_by_type` (see 3.3), returning every child page dict.

### 5.4 `write_text(path: Path, text: str)`

Write UTF-8 encoded text: `path.write_text(text, encoding="utf-8")`.

---

## 6. Robustness Requirements

- **Cycle / duplicate protection:** Maintain a `visited: set[str]` of page IDs already exported. Skip any ID already in the set (Confluence trees are normally acyclic, but this guards against surprises and prevents infinite loops).
- **Duplicate sibling titles:** Two sibling pages could sanitize to the same folder name. Detect collisions within a parent directory and append ` (2)`, ` (3)`, etc. A simple approach: track used names per parent directory.
- **Error handling per page:** Wrap each page's fetch/convert/write in a try/except so one failing page doesn't abort the whole export. Log the failing page ID and title, then continue.
- **Rate limiting:** Confluence Cloud can throttle. Catch request exceptions; optionally add a small `time.sleep()` between calls or a retry with backoff on HTTP 429.
- **Progress logging:** Print each page as it is exported, e.g. `[export] <id> -> <relative path>`, plus a final count of pages exported.

---

## 7. CLI Interface

Make the root page ID configurable rather than hard-coded. Use `argparse`:

```bash
python backend/confluence_export.py --page-id 56819899 --out output
```

Arguments:

- `--page-id` (required): the starting Confluence page ID.
- `--out` (optional, default `output`): base output directory.

If you want a minimal first version, a hard-coded `ROOT_ID` constant is acceptable, but `argparse` is preferred and low-effort.

---

## 8. Suggested File Skeleton

```python
### Netskope nonsense...
import truststore
truststore.inject_into_ssl()
########################

import argparse
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from atlassian.confluence import Confluence
from markdownify import markdownify as md_convert

load_dotenv()

ILLEGAL = re.compile(r'[\\/:*?"<>|]')


def sanitize(title: str) -> str:
    name = ILLEGAL.sub("_", title).strip().rstrip(".")
    name = re.sub(r"\s+", " ", name)
    return name[:150] or "untitled"


def connect() -> Confluence:
    return Confluence(
        url=os.getenv("CONFLUENCE_URL"),
        username=os.getenv("ATLASSIAN_USER"),
        password=os.getenv("ATLASSIAN_API_KEY"),
    )


def get_all_children(conf: Confluence, page_id: str) -> list[dict]:
    children, start, limit = [], 0, 100
    while True:
        batch = conf.get_page_child_by_type(
            page_id=page_id, type="page", start=start, limit=limit
        )
        children.extend(batch)
        if len(batch) < limit:
            break
        start += limit
    return children


def html_to_markdown(html: str) -> str:
    try:
        return md_convert(html, heading_style="ATX")
    except Exception:
        return html  # fallback: keep raw content


def unique_name(base: str, used: set[str]) -> str:
    name, i = base, 2
    while name in used:
        name = f"{base} ({i})"
        i += 1
    used.add(name)
    return name


def export_page(conf, page_id, parent_dir, visited, used_in_parent):
    if page_id in visited:
        return
    visited.add(page_id)

    page = conf.get_page_by_id(page_id=page_id, expand="body.storage")
    title = page["title"]
    html = page["body"]["storage"]["value"]

    folder_name = unique_name(sanitize(title), used_in_parent)
    page_dir = parent_dir / folder_name
    page_dir.mkdir(parents=True, exist_ok=True)

    md = f"# {title}\n\n" + html_to_markdown(html)
    (page_dir / f"{sanitize(title)}.md").write_text(md, encoding="utf-8")
    print(f"[export] {page_id} -> {page_dir}")

    child_used: set[str] = set()
    for child in get_all_children(conf, page_id):
        export_page(conf, child["id"], page_dir, visited, child_used)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-id", required=True)
    parser.add_argument("--out", default="output")
    args = parser.parse_args()

    conf = connect()
    export_page(conf, args.page_id, Path(args.out), set(), set())
    print("Done.")


if __name__ == "__main__":
    main()
```

---

## 9. Testing / Verification Steps

1. Ensure `.env` has valid `CONFLUENCE_URL`, `ATLASSIAN_USER`, `ATLASSIAN_API_KEY`.
2. Install the new dependency: `pip install markdownify`.
3. Run against a small known page with a few children:
   ```bash
   python backend/confluence_export.py --page-id 56819899 --out output
   ```
4. Confirm the folder tree matches the Confluence hierarchy.
5. Confirm each folder contains a `.md` file named after the title, with readable Markdown.
6. Test edge cases: a page with a title containing `/` or `:`; a page with >100 children (pagination); a page with no children (leaf).

---

## 10. Known Limitations (document, don't necessarily fix in v1)

- **Confluence macros** (`<ac:structured-macro>`, info panels, code blocks, Jira links, etc.) are not fully translated; `markdownify` keeps inner text but drops macro semantics.
- **Attachments and images** are not downloaded. Image references become broken links. A future enhancement: use `confluence.get_attachments_from_content(page_id)` and download binaries into an `assets/` subfolder, rewriting image `src` paths.
- **Internal page links** remain as Confluence URLs, not relative links to the exported files.
- **Page order** is API-returned order, not necessarily the sidebar order.

These are acceptable for a first version whose goal is to mirror content and hierarchy as Markdown.

---

## 11. Implementation Checklist

- [ ] Add `markdownify` to [backend/requirements.txt](../backend/requirements.txt) and install it.
- [ ] Create `backend/confluence_export.py` with the `truststore` block at the top.
- [ ] Implement `sanitize`, `connect`, `get_all_children`, `html_to_markdown`, `unique_name`, `export_page`, `main`.
- [ ] Add `argparse` CLI (`--page-id`, `--out`).
- [ ] Add `visited` set (cycle protection) and per-parent name-collision handling.
- [ ] Add per-page try/except and progress logging.
- [ ] Run against a real page ID and verify folder/file structure.

### Netskope workaround ###
import truststore
truststore.inject_into_ssl()
###########################

import argparse
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from atlassian.confluence import Confluence
from markdownify import markdownify as md_convert
from requests.exceptions import HTTPError, RequestException

load_dotenv()

ILLEGAL = re.compile(r'[\\/:*?"<>|]')

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2
REQUEST_DELAY_SECONDS = 0.2


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


def with_retries(func, *args, **kwargs):
    """Call func with simple retry/backoff on HTTP 429 (rate limiting) or transient request errors."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return func(*args, **kwargs)
        except HTTPError as exc:
            status = getattr(exc.response, "status_code", None)
            if status == 429 and attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF_SECONDS * attempt
                print(f"[warn] rate limited (429); retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise
        except RequestException:
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF_SECONDS * attempt
                print(f"[warn] request failed; retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise


def get_all_children(conf: Confluence, page_id: str) -> list[dict]:
    children, start, limit = [], 0, 100
    while True:
        batch = with_retries(
            conf.get_page_child_by_type,
            page_id=page_id,
            type="page",
            start=start,
            limit=limit,
        )
        children.extend(batch)
        if len(batch) < limit:
            break
        start += limit
    return children


def html_to_markdown(html: str) -> str:
    try:
        return md_convert(html, heading_style="ATX")
    except Exception as exc:
        print(f"[warn] markdown conversion failed ({exc}); falling back to raw HTML")
        return html  # fallback: keep raw content


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def unique_name(base: str, used: set) -> str:
    name, i = base, 2
    while name in used:
        name = f"{base} ({i})"
        i += 1
    used.add(name)
    return name


def export_page(conf, page_id, parent_dir: Path, visited: set, used_in_parent: set, count: list) -> None:
    if page_id in visited:
        print(f"[skip] {page_id} already visited (cycle/duplicate guard)")
        return
    visited.add(page_id)

    try:
        page = with_retries(conf.get_page_by_id, page_id=page_id, expand="body.storage")
        title = page["title"]
        html = page["body"]["storage"]["value"]

        folder_name = unique_name(sanitize(title), used_in_parent)
        page_dir = parent_dir / folder_name
        page_dir.mkdir(parents=True, exist_ok=True)

        markdown = f"# {title}\n\n" + html_to_markdown(html)
        write_text(page_dir / f"{sanitize(title)}.md", markdown)
        count[0] += 1
        print(f"[export] {page_id} -> {page_dir}")
    except Exception as exc:
        print(f"[error] failed to export page {page_id} ({exc}); continuing")
        return

    time.sleep(REQUEST_DELAY_SECONDS)

    try:
        children = get_all_children(conf, page_id)
    except Exception as exc:
        print(f"[error] failed to list children of {page_id} ({exc}); skipping children")
        return

    child_used: set = set()
    for child in children:
        export_page(conf, child["id"], page_dir, visited, child_used, count)


def run_export(page_id: str, out: str = "output") -> int:
    """Export a Confluence page tree to Markdown. Returns number of pages exported."""
    conf = connect()
    count = [0]
    export_page(conf, page_id, Path(out), set(), set(), count)
    print(f"Done. Exported {count[0]} page(s).")
    return count[0]


def main():
    parser = argparse.ArgumentParser(
        description="Recursively export a Confluence page tree to local Markdown files."
    )
    parser.add_argument("--page-id", required=True, help="Root Confluence page ID to export")
    parser.add_argument("--out", default="output", help="Base output directory (default: output)")
    args = parser.parse_args()
    run_export(args.page_id, args.out)


if __name__ == "__main__":
    main()

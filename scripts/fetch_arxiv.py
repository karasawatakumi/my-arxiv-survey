#!/usr/bin/env python3
"""Fetch latest N arXiv papers matching a query and export as CSV.

Usage:
    python fetch_arxiv.py "co:cvpr" 10                   # default categories applied
    python fetch_arxiv.py "diffusion" 50
    python fetch_arxiv.py "ti:transformer" 20 --categories cs.CL,cs.LG
    python fetch_arxiv.py "co:neurips" 30 --categories ""   # disable category filter

The query is passed to arXiv's search_query, AND-combined with the category
filter (default: cs.CV, cs.RO, cs.AI, cs.LG). Field prefixes:
    ti  title       au  author       abs abstract     co  comment
    jr  journal     cat category     rn  report-no    all all of the above
A bare keyword (no prefix) is searched across all fields.

Constraints on N (per arXiv API guidelines):
    - 1 <= N <= 30000
    - Internally paginated at PAGE_SIZE=200 with a 3s delay between requests.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT_DIR = os.path.join(REPO_ROOT, "outputs")

API_URL = "http://export.arxiv.org/api/query"
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

PAGE_SIZE = 25           # per-request cap; arxiv rate-limits large max_results aggressively
MAX_TOTAL = 30000        # practical hard cap for a single search
REQUEST_DELAY = 10.0     # seconds between requests (3s is API minimum; 10s for safety)
MAX_RETRIES = 5
BACKOFF_BASE = 10.0      # seconds; multiplied by attempt index on retry

DEFAULT_CATEGORIES = ["cs.CV", "cs.RO", "cs.AI", "cs.LG"]

REPO_URL_RE = re.compile(
    r"https?://(?:www\.)?(?:github\.com|gitlab\.com|bitbucket\.org)/\S+",
    re.IGNORECASE,
)


def build_url(query: str, start: int, max_results: int) -> str:
    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return f"{API_URL}?{urllib.parse.urlencode(params)}"


def fetch(url: str) -> bytes:
    last_err: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "fetch_arxiv/1.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = e
            # 429 / 5xx: wait longer; 4xx else: don't retry
            if e.code == 429 or 500 <= e.code < 600:
                if attempt < MAX_RETRIES:
                    time.sleep(BACKOFF_BASE * attempt)
                    continue
            raise RuntimeError(f"HTTP {e.code} on {url}") from e
        except Exception as e:  # noqa: BLE001
            last_err = e
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF_BASE * attempt)
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def parse_entries(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    entries = []
    for e in root.findall("a:entry", NS):
        get = lambda tag: (e.findtext(f"a:{tag}", default="", namespaces=NS) or "").strip()
        authors = [
            (a.findtext("a:name", default="", namespaces=NS) or "").strip()
            for a in e.findall("a:author", NS)
        ]
        categories = [
            c.attrib.get("term", "") for c in e.findall("a:category", NS)
        ]
        primary = e.find("arxiv:primary_category", NS)
        primary_cat = primary.attrib.get("term", "") if primary is not None else ""
        comment_el = e.find("arxiv:comment", NS)
        comment = " ".join((comment_el.text or "").split()) if comment_el is not None else ""
        m = REPO_URL_RE.search(comment)
        repo_url = m.group(0).rstrip(".,;:)\"'") if m else ""
        pdf_url = ""
        for link in e.findall("a:link", NS):
            if link.attrib.get("title") == "pdf":
                pdf_url = link.attrib.get("href", "")
                break
        entries.append({
            "id": get("id"),
            "title": " ".join(get("title").split()),
            "authors": "; ".join(authors),
            "author_count": len(authors),
            "primary_category": primary_cat,
            "categories": "; ".join(categories),
            "comment": comment,
            "repo_url": repo_url,
            "published": get("published"),
            "updated": get("updated"),
            "summary": " ".join(get("summary").split()),
            "pdf_url": pdf_url,
        })
    return entries


CSV_FIELDS = [
    "id", "title", "authors", "author_count",
    "primary_category", "categories", "comment", "repo_url",
    "published", "updated", "summary", "pdf_url",
]


def iter_pages(keyword: str, n: int, primary_filter: list[str] | None = None):
    """Yield (batch, written_so_far_after_batch, raw_start) per page.

    Stops when n filtered rows accumulated, the API runs out, or MAX_TOTAL hit.
    """
    if not (1 <= n <= MAX_TOTAL):
        raise ValueError(f"n must be in [1, {MAX_TOTAL}], got {n}")
    written = 0
    start = 0
    while written < n and start < MAX_TOTAL:
        url = build_url(keyword, start, PAGE_SIZE)
        xml_bytes = fetch(url)
        entries = parse_entries(xml_bytes)
        if not entries:
            return  # no more results from API
        raw_count = len(entries)
        start += raw_count
        if primary_filter:
            entries = [e for e in entries if e["primary_category"] in primary_filter]
        # cap to remaining n
        remaining = n - written
        if len(entries) > remaining:
            entries = entries[:remaining]
        written += len(entries)
        yield entries, written, start
        if raw_count < PAGE_SIZE:
            return  # server has no more matches
        if written < n:
            time.sleep(REQUEST_DELAY)


def build_query(user_query: str, categories: list[str]) -> str:
    if not categories:
        return user_query
    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
    return f"({cat_clause}) AND ({user_query})"


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch latest N arXiv papers matching an arXiv search query.")
    p.add_argument("query", help='arXiv search_query expression, e.g. "diffusion" or "co:cvpr"')
    p.add_argument("n", type=int, help=f"number of papers to fetch (1..{MAX_TOTAL})")
    p.add_argument("-o", "--output", default=None, help="output CSV path (default: arxiv_<query>_<n>.csv)")
    p.add_argument(
        "--categories",
        default=",".join(DEFAULT_CATEGORIES),
        help=f'comma-separated arXiv categories AND-combined with query (default: {",".join(DEFAULT_CATEGORIES)}). Pass "" to disable.',
    )
    args = p.parse_args()

    categories = [c.strip() for c in args.categories.split(",") if c.strip()]
    full_query = build_query(args.query, categories)

    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", args.query).strip("_") or "query"
    out = args.output or os.path.join(DEFAULT_OUT_DIR, f"arxiv_{safe}_{args.n}.csv")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    total = 0
    try:
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CSV_FIELDS, quoting=csv.QUOTE_ALL)
            w.writeheader()
            f.flush()
            for batch, written, raw_start in iter_pages(
                full_query, args.n, primary_filter=categories or None
            ):
                w.writerows(batch)
                f.flush()
                total = written
                print(f"  page done: +{len(batch)} rows  (written={written}, raw_seen={raw_start})", flush=True)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print(f"\ninterrupted: kept {total} rows in {out}", file=sys.stderr)
        return 130
    print(f"wrote {total} rows to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

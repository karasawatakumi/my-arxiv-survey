#!/usr/bin/env python3
"""Write a sidecar meta.json describing a tasks CSV's coverage.

For a CSV at outputs/foo.csv, by default writes outputs/foo.meta.json with:
    {
      "query": "co:cvpr AND co:2026",
      "total_rows": 1657,
      "latest_published": "2026-05-08",
      "latest_updated":   "2026-05-08",
      "last_fetched_at":  "2026-05-11T22:30:00+09:00"
    }

`query` is taken from --query if given, otherwise preserved from the existing
meta.json if one is present. This lets `update.sh` call write_meta.py without
re-specifying the query every run.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import sys


def main() -> int:
    p = argparse.ArgumentParser(description="Write meta.json sidecar describing a tasks CSV.")
    p.add_argument("csv_path", help="path to the tasks CSV")
    p.add_argument("-o", "--output", default=None, help="output meta path (default: <csv>.replace('.csv','.meta.json'))")
    p.add_argument("--query", default=None, help="search query stored in meta (preserved from existing meta if omitted)")
    args = p.parse_args()

    if args.output:
        out = args.output
    elif args.csv_path.endswith(".csv"):
        out = args.csv_path[:-4] + ".meta.json"
    else:
        out = args.csv_path + ".meta.json"

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    pubs = [(r.get("published") or "")[:10] for r in rows]
    pubs = [p for p in pubs if p]
    ups = [(r.get("updated") or "")[:10] for r in rows]
    ups = [u for u in ups if u]

    query = args.query
    if not query and os.path.exists(out):
        try:
            with open(out, encoding="utf-8") as f:
                old = json.load(f)
            query = old.get("query")
        except (OSError, json.JSONDecodeError):
            pass

    meta = {
        "query": query,
        "total_rows": len(rows),
        "latest_published": max(pubs) if pubs else None,
        "latest_updated": max(ups) if ups else None,
        "last_fetched_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, out)

    print(f"wrote meta: {out}")
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

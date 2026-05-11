#!/usr/bin/env python3
"""Merge an update CSV into an existing _tasks CSV.

Behavior:
    * Rows in UPDATE_CSV whose normalized id matches an existing row REPLACE
      the existing row in-place (preserving its position).
    * Rows in UPDATE_CSV whose id is new are APPENDED at the end.
    * Output column set = existing CSV's columns. Update rows missing a column
      keep the existing value (i.e. partial-column updates are not supported —
      pass a fully enriched update CSV).

Designed to be the final step of `update.sh` after diff fetch + enrich.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import tempfile


def norm_id(s: str) -> str:
    return re.sub(r"v\d+$", "", (s or "").strip())


def main() -> int:
    p = argparse.ArgumentParser(description="Merge update CSV into existing _tasks CSV.")
    p.add_argument("existing", help="existing _tasks.csv (will NOT be modified in place)")
    p.add_argument("update", help="update CSV with the same columns")
    p.add_argument("-o", "--output", required=True, help="output CSV path (may equal `existing` to overwrite)")
    args = p.parse_args()

    with open(args.existing, newline="", encoding="utf-8") as f:
        existing_rows = list(csv.DictReader(f))
    with open(args.update, newline="", encoding="utf-8") as f:
        update_rows = list(csv.DictReader(f))

    if not existing_rows:
        print("error: existing CSV has no rows", file=sys.stderr)
        return 2
    fieldnames = list(existing_rows[0].keys())

    update_map: dict[str, dict] = {}
    for r in update_rows:
        k = norm_id(r.get("id", ""))
        if k:
            update_map[k] = r

    merged: list[dict] = []
    replaced_ids: set[str] = set()
    for r in existing_rows:
        k = norm_id(r.get("id", ""))
        if k in update_map:
            up = update_map[k]
            # only keep columns in `fieldnames`; missing keys -> empty string
            merged.append({col: up.get(col, "") for col in fieldnames})
            replaced_ids.add(k)
        else:
            merged.append(r)

    added = 0
    for r in update_rows:
        k = norm_id(r.get("id", ""))
        if k and k not in replaced_ids:
            merged.append({col: r.get(col, "") for col in fieldnames})
            added += 1

    # atomic write: tmpfile + rename
    out_dir = os.path.dirname(os.path.abspath(args.output)) or "."
    fd, tmp = tempfile.mkstemp(prefix=".merge_", suffix=".csv", dir=out_dir)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            w.writeheader()
            w.writerows(merged)
        os.replace(tmp, args.output)
    except Exception:
        try: os.unlink(tmp)
        except OSError: pass
        raise

    print(
        f"merged: replaced={len(replaced_ids)} revised, added={added} new, "
        f"total={len(merged)} -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Enrich an arXiv-survey CSV by extracting structured info from `comment` via GPT.

Reads a CSV produced by fetch_arxiv.py, sends each row's `comment` to OpenAI,
and writes a new CSV with these columns appended:
    is_cvpr2026  yes | no | unsure
    track        main | findings | workshop | other | unknown
    accepted     yes | no | unsure
    notes        short free-text (e.g. "Highlight", "oral", "")

Requires OPENAI_API_KEY in .env (or the environment).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT_DIR = os.path.join(REPO_ROOT, "outputs")

SCHEMA = {
    "name": "comment_analysis",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["is_cvpr2026", "track", "accepted", "notes"],
        "properties": {
            "is_cvpr2026": {
                "type": "string",
                "enum": ["yes", "no", "unsure"],
                "description": "yes = comment clearly indicates CVPR 2026 (main, findings, or workshop). no = different conference/year (e.g. CVPR 2025, ECCV, ICCV, NeurIPS). unsure = unclear or empty.",
            },
            "track": {
                "type": "string",
                "enum": ["main", "findings", "workshop", "other", "unknown"],
                "description": "main = main conference (Highlight/oral/poster all count). findings = Findings track. workshop = any CVPR workshop / affiliated event. other = clearly different category. unknown = cannot tell.",
            },
            "accepted": {
                "type": "string",
                "enum": ["yes", "no", "unsure"],
                "description": "yes = explicitly accepted/published. no = only submitted/under review. unsure = unclear.",
            },
            "notes": {
                "type": "string",
                "description": "Short note: 'Highlight', 'oral', 'poster', '', etc. Max ~30 chars.",
            },
        },
    },
}

SYSTEM_PROMPT = (
    "You classify arXiv paper `comment` fields about CVPR 2026. "
    "Return only the structured JSON. Be conservative: if a comment doesn't "
    "explicitly mention CVPR 2026 in some form, set is_cvpr2026=unsure or no. "
    "Workshop papers (e.g. 'CVPR Workshops', 'XAI4CV Workshop, CVPR') -> track=workshop. "
    "'Findings Track' / 'Findings of CVPR' -> track=findings. "
    "Plain 'Accepted to CVPR 2026' or 'CVPR 2026 (Highlight)' -> track=main."
)


def classify(client: OpenAI, model: str, comment: str) -> dict:
    if not comment.strip():
        return {"is_cvpr2026": "unsure", "track": "unknown", "accepted": "unsure", "notes": ""}
    last_err: Exception | None = None
    for attempt in range(1, 4):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"comment: {comment}"},
                ],
                response_format={"type": "json_schema", "json_schema": SCHEMA},
                temperature=0,
            )
            return json.loads(resp.choices[0].message.content)
        except OpenAIError as e:
            last_err = e
            if attempt < 3:
                time.sleep(2 * attempt)
    raise RuntimeError(f"OpenAI call failed: {last_err}")


def main() -> int:
    p = argparse.ArgumentParser(description="Enrich arxiv CSV with GPT-based comment classification.")
    p.add_argument("input_csv", help="path to CSV produced by fetch_arxiv.py")
    p.add_argument("-o", "--output", default=None, help="output CSV path (default: <input>_enriched.csv)")
    p.add_argument("--model", default="gpt-4o-mini", help="OpenAI model (default: gpt-4o-mini)")
    p.add_argument("--limit", type=int, default=None, help="only process first N rows (for testing)")
    p.add_argument("--workers", type=int, default=5, help="concurrent OpenAI requests (default: 5)")
    args = p.parse_args()

    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    if not os.getenv("OPENAI_API_KEY"):
        print("error: OPENAI_API_KEY not set (put it in .env)", file=sys.stderr)
        return 2

    if args.output:
        out_path = args.output
    else:
        base = os.path.basename(args.input_csv).replace(".csv", "_enriched.csv")
        out_path = os.path.join(DEFAULT_OUT_DIR, base)
    if os.path.abspath(out_path) == os.path.abspath(args.input_csv):
        out_path = args.input_csv + ".enriched.csv"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    with open(args.input_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if args.limit:
        rows = rows[: args.limit]

    client = OpenAI()
    new_fields = ["is_cvpr2026", "track", "accepted", "notes"]

    def process(row):
        try:
            cls = classify(client, args.model, row.get("comment", ""))
        except Exception as e:
            print(f"  ERROR on '{(row.get('title','') or '')[:50]}': {e}", file=sys.stderr)
            cls = {"is_cvpr2026": "unsure", "track": "unknown", "accepted": "unsure", "notes": f"err:{type(e).__name__}"}
        row.update(cls)
        return row

    errors = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = list(rows[0].keys()) + new_fields if rows else new_fields
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        w.writeheader()
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            for i, row in enumerate(ex.map(process, rows), 1):
                w.writerow(row)
                f.flush()
                if (row.get("notes") or "").startswith("err:"):
                    errors += 1
                if i % 25 == 0 or i == len(rows):
                    print(f"[{i}/{len(rows)}] cvpr2026={row['is_cvpr2026']:6s} track={row['track']:9s} | {row.get('title','')[:60]}")
    print(f"\nwrote {len(rows)} rows to {out_path}" + (f" ({errors} errors)" if errors else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

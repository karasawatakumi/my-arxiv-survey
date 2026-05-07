#!/usr/bin/env python3
"""Enrich an arXiv-survey CSV with task-category labels via GPT.

Reads a CSV that has `title` and `summary` columns, classifies each paper's
task using a fixed taxonomy + free-form keywords, and writes a new CSV.

New columns:
    task_primary     one from TASK_CATEGORIES
    task_secondary   "" or "tagA" or "tagA, tagB" (subset of TASK_CATEGORIES, excludes primary)
    task_keywords    "kwA, kwB, ..." (free-form, 1-5 items)
    modality         image | video | 3d | point-cloud | multimodal | sensor | other
    task_summary     one-line (<=100 chars)

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

TASK_CATEGORIES = [
    "classification", "detection", "segmentation", "pose-estimation",
    "human-mesh", "depth-estimation", "tracking", "action-video",
    "image-generation", "video-generation", "3d-generation", "editing",
    "3d-reconstruction", "novel-view-synthesis", "vlm", "self-supervised",
    "foundation-model", "domain-adaptation", "continual-learning",
    "test-time-adaptation", "federated-learning", "ood-robustness",
    "adversarial-robustness", "efficiency-compression", "medical-imaging",
    "autonomous-driving", "robotics-vla", "face-avatar", "low-level",
    "benchmark-dataset", "other",
]

MODALITIES = ["image", "video", "3d", "point-cloud", "multimodal", "sensor", "other"]

SCHEMA = {
    "name": "task_classification",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["task_primary", "task_secondary", "task_keywords", "modality", "task_summary"],
        "properties": {
            "task_primary": {
                "type": "string",
                "enum": TASK_CATEGORIES,
                "description": "Most central task of the paper. Pick exactly one.",
            },
            "task_secondary": {
                "type": "array",
                "items": {"type": "string", "enum": TASK_CATEGORIES},
                "description": "0-2 additional categories that meaningfully apply (must differ from task_primary). Empty array if nothing else applies.",
            },
            "task_keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": "3-5 short free-form keywords (specific methods, sub-domains, or concepts), e.g. '3d gaussian splatting', 'CLIP', 'urban driving', 'hyperspectral'. Lowercase, concise.",
            },
            "modality": {
                "type": "string",
                "enum": MODALITIES,
                "description": "Primary input modality. Use 'multimodal' if vision+language is core. '3d' for meshes/NeRF/3DGS scenes. 'point-cloud' for LiDAR/PCD inputs.",
            },
            "task_summary": {
                "type": "string",
                "description": "One-line plain English summary of what the paper does (<=100 chars).",
            },
        },
    },
}

SYSTEM_PROMPT = (
    "You categorize computer vision / ML papers from their title and abstract.\n"
    "\n"
    "Rules:\n"
    "1. task_primary is the SINGLE most central task. Prefer domain-specific categories "
    "(medical-imaging, autonomous-driving, robotics-vla, face-avatar) over technique-only "
    "categories (vlm, foundation-model, self-supervised) when the paper's main contribution "
    "is *in* that domain. Example: a VLA model for robotic manipulation -> robotics-vla, "
    "not vlm.\n"
    "2. If no category clearly fits the central task, use 'other' for task_primary without "
    "hesitation. Examples that should be 'other': visual localization, SLAM, optical flow, "
    "stereo matching, scene flow.\n"
    "3. task_secondary: include ONLY tasks the paper explicitly performs, evaluates on, or "
    "directly contributes to. Do NOT fill slots to be 'thorough' — empty array is fine and "
    "often correct. Most papers have 0 or 1 secondary, not 2.\n"
    "4. task_keywords are free-form, specific, lowercase. Use them for things the taxonomy "
    "misses (e.g. 'visual localization', '3d gaussian splatting', 'hyperspectral'). "
    "Do not repeat category names there.\n"
    "5. task_summary: concrete one-liner — what is the input, what is produced, the key idea."
)


def classify(client: OpenAI, model: str, title: str, abstract: str) -> dict:
    user = f"title: {title}\n\nabstract: {abstract}"
    last_err: Exception | None = None
    for attempt in range(1, 4):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_schema", "json_schema": SCHEMA},
                temperature=0,
            )
            data = json.loads(resp.choices[0].message.content)
            # Normalize secondary: drop primary if echoed, dedupe, clamp to 2
            sec = [s for s in data.get("task_secondary", []) if s != data["task_primary"]]
            seen, ordered = set(), []
            for s in sec:
                if s not in seen:
                    seen.add(s)
                    ordered.append(s)
            data["task_secondary"] = ordered[:2]
            data["task_keywords"] = data.get("task_keywords", [])[:5]
            return data
        except OpenAIError as e:
            last_err = e
            if attempt < 3:
                time.sleep(2 * attempt)
    raise RuntimeError(f"OpenAI call failed: {last_err}")


def main() -> int:
    p = argparse.ArgumentParser(description="Enrich arxiv CSV with task categories via GPT.")
    p.add_argument("input_csv", help="path to CSV with title/summary columns")
    p.add_argument("-o", "--output", default=None, help="output CSV path (default: <input>_tasks.csv)")
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
        base = os.path.basename(args.input_csv).replace(".csv", "_tasks.csv")
        out_path = os.path.join(DEFAULT_OUT_DIR, base)
    if os.path.abspath(out_path) == os.path.abspath(args.input_csv):
        out_path = args.input_csv + ".tasks.csv"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    with open(args.input_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if args.limit:
        rows = rows[: args.limit]

    if rows and ("title" not in rows[0] or "summary" not in rows[0]):
        print("error: input CSV must have 'title' and 'summary' columns", file=sys.stderr)
        return 2

    client = OpenAI()
    new_fields = ["task_primary", "task_secondary", "task_keywords", "modality", "task_summary"]

    def process(row):
        try:
            cls = classify(client, args.model, row.get("title", ""), row.get("summary", ""))
            row["task_primary"] = cls["task_primary"]
            row["task_secondary"] = ", ".join(cls["task_secondary"])
            row["task_keywords"] = ", ".join(cls["task_keywords"])
            row["modality"] = cls["modality"]
            row["task_summary"] = cls["task_summary"]
        except Exception as e:
            print(f"  ERROR on '{(row.get('title','') or '')[:50]}': {e}", file=sys.stderr)
            row["task_primary"] = "other"
            row["task_secondary"] = ""
            row["task_keywords"] = ""
            row["modality"] = "other"
            row["task_summary"] = f"err:{type(e).__name__}"
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
                if row["task_summary"].startswith("err:"):
                    errors += 1
                if i % 25 == 0 or i == len(rows):
                    sec_str = f" (+{row['task_secondary']})" if row["task_secondary"] else ""
                    print(f"[{i}/{len(rows)}] {row['task_primary']}{sec_str} | {row.get('title','')[:60]}")
    print(f"\nwrote {len(rows)} rows to {out_path}" + (f" ({errors} errors)" if errors else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

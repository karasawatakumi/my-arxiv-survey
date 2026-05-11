#!/usr/bin/env bash
# Incremental update for the arXiv survey pipeline.
#
# Usage:
#   scripts/update.sh                                          # cvpr2026 defaults
#   scripts/update.sh outputs/cvpr2026_tasks.csv               # explicit target
#   QUERY="co:cvpr AND co:2026" scripts/update.sh              # override query
#   CAP=8000 scripts/update.sh                                 # raise upper cap
#
# Steps:
#   1. diff fetch: only entries with `updated` > max(existing.updated)
#   2. enrich_comments + enrich_tasks on the diff
#   3. merge into existing _tasks.csv (revised rows replaced, new rows appended)
#   4. update meta.json
#
# Safe to re-run: produces zero rows if there's nothing new and just refreshes
# meta.json.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

EXISTING="${1:-outputs/cvpr2026_tasks.csv}"
QUERY="${QUERY:-co:cvpr AND co:2026}"
CAP="${CAP:-5000}"

if [ ! -f "$EXISTING" ]; then
  echo "error: existing CSV not found: $EXISTING" >&2
  echo "  run a full fetch first (see README.md)." >&2
  exit 2
fi

STAMP="$(date +%Y%m%d_%H%M%S)"
TMP_RAW="outputs/.update_${STAMP}_raw.csv"
TMP_ENRICHED="outputs/.update_${STAMP}_enriched.csv"
TMP_TASKS="outputs/.update_${STAMP}_tasks.csv"
BACKUP="${EXISTING%.csv}.bak.${STAMP}.csv"

cleanup() {
  rm -f "$TMP_RAW" "$TMP_ENRICHED" "$TMP_TASKS"
}
trap cleanup EXIT

echo "==> [1/4] diff fetch  (query='$QUERY', cap=$CAP, boundary=max(updated) in $EXISTING)"
uv run scripts/fetch_arxiv.py "$QUERY" "$CAP" --update "$EXISTING" -o "$TMP_RAW"

DIFF_ROWS=$(($(wc -l < "$TMP_RAW") - 1))
if [ "$DIFF_ROWS" -le 0 ]; then
  echo "==> no new or revised entries — refreshing meta only"
  uv run scripts/write_meta.py "$EXISTING" --query "$QUERY"
  exit 0
fi
echo "==> $DIFF_ROWS rows to enrich"

echo "==> [2/4] enrich_comments"
uv run scripts/enrich_comments.py "$TMP_RAW" -o "$TMP_ENRICHED"

echo "==> [3/4] enrich_tasks"
uv run scripts/enrich_tasks.py "$TMP_ENRICHED" -o "$TMP_TASKS"

echo "==> backing up $EXISTING -> $BACKUP"
cp "$EXISTING" "$BACKUP"

echo "==> [4/4] merge into $EXISTING"
uv run scripts/merge_update.py "$EXISTING" "$TMP_TASKS" -o "$EXISTING"

echo "==> write meta"
uv run scripts/write_meta.py "$EXISTING" --query "$QUERY"

echo "==> done. backup kept at $BACKUP"

#!/usr/bin/env python3
"""Trend analysis for CVPR 2026 papers — bypasses the fixed task taxonomy.

Two complementary views, both ignoring task_primary / task_secondary / modality
(those are constrained to a 31-cat tax and can't reveal emergent topics):

  1. Embedding clustering: embed (title + task_keywords + abstract head),
     KMeans cluster, GPT-label each cluster's centroid neighborhood.
  2. LLM narrative: feed a condensed (title + task_keywords) view of all
     papers to a single GPT call and ask for emergent themes.

Output: outputs/cvpr2026_trends.md (Japanese, structured).

Usage:
    uv run scripts/analyze_trends.py
    uv run scripts/analyze_trends.py --n-clusters 40 --model gpt-5-mini
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import os
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV = os.path.join(REPO_ROOT, "outputs", "cvpr2026_tasks.csv")
DEFAULT_OUT = os.path.join(REPO_ROOT, "outputs", "cvpr2026_trends.md")

EMBED_MODEL = "text-embedding-3-small"
DEFAULT_LLM = "gpt-5-mini"
DEFAULT_K = 35

# Per-cluster label schema. Strict to keep parsing trivial.
CLUSTER_SCHEMA = {
    "name": "cluster_label",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["label", "what_is_distinctive"],
        "properties": {
            "label": {
                "type": "string",
                "description": (
                    "4〜8語の英語ラベル。手法名・タスク名・術語は英語のまま (e.g. "
                    "'3D Gaussian Splatting Editing', 'Vision-Language Robotic Policy'). "
                    "カタカナ訳禁止。"
                ),
            },
            "what_is_distinctive": {
                "type": "string",
                "description": (
                    "このクラスタの何がユニークか・どんなテクニカルなテーマか "
                    "を 1〜2文の日本語で。固有名詞・術語は英語のまま。"
                ),
            },
        },
    },
}

NARRATIVE_SCHEMA = {
    "name": "trend_narrative",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "emerging_themes",
            "hot_subfields",
            "methodological_trends",
            "novel_applications",
            "surprises",
        ],
        "properties": {
            "emerging_themes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["theme", "description", "example_titles"],
                    "properties": {
                        "theme": {"type": "string"},
                        "description": {"type": "string"},
                        "example_titles": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
                "description": "新興テーマ 5〜8個。固有名詞・術語は英語のまま。",
            },
            "hot_subfields": {
                "type": "array",
                "items": {"type": "string"},
                "description": "提出数が際立って多そうな細分野 5〜10個 (英語名+短い日本語コメント)。",
            },
            "methodological_trends": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "横断的に観測される手法トレンド 4〜8個 (e.g. "
                    "'diffusion models が画像生成以外のタスクに広がる', "
                    "'VLM をプランナーとして使う pattern が定着' 等)。"
                    "固有名詞・術語は英語のまま。"
                ),
            },
            "novel_applications": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "新しい応用領域・問題設定 3〜6個 (e.g. "
                    "'humanoid manipulation の評価ベンチ', 'VLM-based medical reasoning')。"
                    "術語英語のまま。"
                ),
            },
            "surprises": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "意外だった観測 2〜5個 (薄いと思った領域に多い/期待ほど無い 等)。"
                    "術語英語のまま。"
                ),
            },
        },
    },
}

CLUSTER_PROMPT_SYS = (
    "あなたはコンピュータビジョン/機械学習の研究者です。"
    "与えられた論文タイトル群と頻出キーワード群は同じクラスタに属します。"
    "このクラスタを表す簡潔な英語ラベルと、何がユニークかの日本語1〜2文を返してください。"
    "技術用語・手法名・タスク名は **英語のまま** 書きカタカナ化してはいけません。"
)

NARRATIVE_PROMPT_SYS = (
    "あなたはコンピュータビジョン/機械学習の研究者として、"
    "学会の論文タイトル+著者付与の自由記述キーワードリストを俯瞰し、"
    "事前定義カテゴリに頼らずに **その学会で今起きている現場のトレンド** を抽出する役割です。"
    "出力は指定された JSON スキーマに従ってください。\n\n"
    "厳守事項:\n"
    "- 手法名/モデル名/タスク名/データセット名/概念名は **英語のまま** 書く "
    "(e.g. Transformer, NeRF, 3D Gaussian Splatting, VLM, semantic segmentation, "
    "diffusion model, fine-tuning, scaling, distillation, retrieval)。\n"
    "- カタカナ化禁止 (ディフュージョン, トランスフォーマー, セグメンテーション 等)。\n"
    "- 推測ではなく、与えられたタイトル+キーワードに観測される実際のパターンを書く。\n"
    "- 件数感を込める (e.g. '〜系が目立つ', '〜が散見される', '〜は少ない')。\n"
    "- 過去学会との比較データは無いので、過去比は書かない。'CVPR 2026 で観測される' というスタンス。"
)


def load_papers(csv_path: str, cvpr_only: bool = True) -> list[dict]:
    rows: list[dict] = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if cvpr_only and r.get("is_cvpr2026") != "yes":
                continue
            rows.append(r)
    return rows


def build_doc(r: dict, *, abstract_chars: int = 800) -> str:
    parts = [r.get("title", "").strip()]
    kw = (r.get("task_keywords") or "").strip()
    if kw:
        parts.append(f"keywords: {kw}")
    summary = (r.get("summary") or "").strip().replace("\n", " ")
    if summary:
        parts.append(summary[:abstract_chars])
    return "\n\n".join(parts)


def build_condensed(r: dict) -> str:
    """Single-line view for the LLM narrative pass — keep token cost low."""
    kw = (r.get("task_keywords") or "").strip()
    track = (r.get("track") or "").strip()
    title = (r.get("title") or "").strip()
    bits = [title]
    if kw:
        bits.append(f"kws: {kw}")
    if track and track != "unknown":
        bits.append(f"track:{track}")
    return " | ".join(bits)


def embed_all(client: OpenAI, docs: list[str], batch_size: int = 512) -> np.ndarray:
    out: list[list[float]] = []
    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        print(f"  embedding batch {i // batch_size + 1} ({len(batch)} docs)...", flush=True)
        resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
        out.extend([d.embedding for d in resp.data])
    return np.array(out, dtype=np.float32)


def label_cluster(
    client: OpenAI,
    model: str,
    cluster_id: int,
    titles: list[str],
    top_keywords: list[tuple[str, int]],
) -> dict:
    kw_lines = "\n".join(f"  - {kw} (×{n})" for kw, n in top_keywords)
    title_lines = "\n".join(f"  - {t}" for t in titles[:10])
    user = (
        f"# Cluster {cluster_id}\n\n"
        f"## 頻出キーワード (free-form, 著者ではなく分類GPTが付与)\n{kw_lines}\n\n"
        f"## 代表論文タイトル (centroidに近い順)\n{title_lines}\n"
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CLUSTER_PROMPT_SYS},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_schema", "json_schema": CLUSTER_SCHEMA},
    )
    return json.loads(resp.choices[0].message.content)


def run_narrative(client: OpenAI, model: str, lines: list[str]) -> dict:
    user = (
        f"対象: CVPR 2026 で is_cvpr2026=yes と判定された {len(lines)} 件の論文。\n"
        f"各行は `title | kws: <task_keywords> | track:<track>` 形式。\n\n"
        "以下のリストを俯瞰して、指定スキーマで現場トレンドを抽出してください。\n\n"
        + "\n".join(lines)
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": NARRATIVE_PROMPT_SYS},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_schema", "json_schema": NARRATIVE_SCHEMA},
    )
    return json.loads(resp.choices[0].message.content)


def cluster_papers(embs: np.ndarray, n_clusters: int) -> tuple[np.ndarray, np.ndarray]:
    """Return (labels, centroids)."""
    # L2-normalize so euclidean ≈ cosine.
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    x = embs / norms
    km = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    labels = km.fit_predict(x)
    return labels, km.cluster_centers_


def closest_to_centroid(
    embs_norm: np.ndarray, labels: np.ndarray, centroids: np.ndarray, k: int = 10
) -> dict[int, list[int]]:
    out: dict[int, list[int]] = {}
    for c in range(centroids.shape[0]):
        idx = np.where(labels == c)[0]
        if len(idx) == 0:
            out[c] = []
            continue
        sims = cosine_similarity(embs_norm[idx], centroids[c : c + 1]).ravel()
        order = idx[np.argsort(-sims)]
        out[c] = order[:k].tolist()
    return out


def top_keywords_per_cluster(
    rows: list[dict], labels: np.ndarray, top_n: int = 8
) -> dict[int, list[tuple[str, int]]]:
    out: dict[int, list[tuple[str, int]]] = {}
    by_cluster: dict[int, Counter] = {}
    for r, c in zip(rows, labels):
        kw = (r.get("task_keywords") or "").strip()
        if not kw:
            continue
        counter = by_cluster.setdefault(int(c), Counter())
        for token in [t.strip() for t in kw.split(",") if t.strip()]:
            counter[token.lower()] += 1
    for c in range(int(labels.max()) + 1):
        out[c] = by_cluster.get(c, Counter()).most_common(top_n)
    return out


def overall_top_keywords(rows: list[dict], top_n: int = 50) -> list[tuple[str, int]]:
    c: Counter = Counter()
    for r in rows:
        kw = (r.get("task_keywords") or "").strip()
        if not kw:
            continue
        for token in [t.strip() for t in kw.split(",") if t.strip()]:
            c[token.lower()] += 1
    return c.most_common(top_n)


def render_markdown(
    rows: list[dict],
    labels: np.ndarray,
    cluster_papers_idx: dict[int, list[int]],
    cluster_labels: dict[int, dict],
    cluster_kws: dict[int, list[tuple[str, int]]],
    top_kws: list[tuple[str, int]],
    narrative: dict,
    *,
    llm_model: str,
) -> str:
    now = _dt.datetime.now(_dt.timezone.utc).astimezone()
    n = len(rows)
    track_c = Counter((r.get("track") or "unknown") for r in rows)
    repo_n = sum(1 for r in rows if (r.get("repo_url") or "").strip())

    lines: list[str] = []
    lines.append("# CVPR 2026 Trends — Free-form Analysis")
    lines.append("")
    lines.append(
        f"_generated: {now.strftime('%Y-%m-%d %H:%M %Z')} · "
        f"embedding: `{EMBED_MODEL}` · labeling+narrative: `{llm_model}` · "
        f"papers: {n} (is_cvpr2026=yes)_"
    )
    lines.append("")
    lines.append(
        "> このレポートは 31種固定タスクタクソノミ (task_primary / task_secondary / "
        "modality) を **使わず**、自由記述の `task_keywords` と embedding を素材に生成しています。"
    )
    lines.append("")

    # --- Section 1: stats ---
    lines.append("## 1. ベース統計")
    lines.append("")
    lines.append(f"- **N = {n}** papers (is_cvpr2026=yes)")
    lines.append(f"- with repo URL: **{repo_n}** ({repo_n / n * 100:.1f}%)")
    track_bits = ", ".join(f"{k}={v}" for k, v in track_c.most_common())
    lines.append(f"- track 内訳: {track_bits}")
    lines.append("")

    # --- Section 2: top free-form keywords ---
    lines.append("## 2. 自由記述キーワード Top 50 (頻度集計のみ)")
    lines.append("")
    lines.append("| rank | keyword | count |")
    lines.append("|---:|---|---:|")
    for i, (kw, c) in enumerate(top_kws, 1):
        lines.append(f"| {i} | `{kw}` | {c} |")
    lines.append("")

    # --- Section 3: emergent clusters ---
    n_clusters = int(labels.max()) + 1
    sizes = Counter(labels.tolist())
    order = [c for c, _ in sizes.most_common()]
    lines.append(f"## 3. 出現クラスタ ({n_clusters} clusters, size desc)")
    lines.append("")
    lines.append(
        "embedding (= title + task_keywords + abstract head) を `text-embedding-3-small` で取り、"
        f"KMeans({n_clusters}) でクラスタリング後、各クラスタの centroid 近傍と頻出キーワードを "
        f"`{llm_model}` にラベル付けさせています。"
    )
    lines.append("")
    for c in order:
        size = sizes[c]
        meta = cluster_labels.get(c, {})
        label = meta.get("label") or f"cluster-{c}"
        distinct = meta.get("what_is_distinctive") or ""
        kws = cluster_kws.get(c, [])
        rep = cluster_papers_idx.get(c, [])
        lines.append(f"### {label}  _(N={size})_")
        lines.append("")
        if distinct:
            lines.append(distinct)
            lines.append("")
        if kws:
            kw_inline = ", ".join(f"`{k}`×{n}" for k, n in kws)
            lines.append(f"- **top keywords**: {kw_inline}")
        if rep:
            lines.append("- **representative**:")
            for idx in rep[:8]:
                r = rows[idx]
                title = (r.get("title") or "").strip()
                arxiv_id = (r.get("id") or "").strip()
                if arxiv_id.startswith("http"):
                    lines.append(f"  - [{title}]({arxiv_id})")
                else:
                    lines.append(f"  - {title}")
        lines.append("")

    # --- Section 4: LLM narrative ---
    lines.append("## 4. LLM 俯瞰分析")
    lines.append("")
    lines.append(
        f"以下は条件付けカテゴリを使わず、`{llm_model}` に title + task_keywords + track の"
        "全件リストを渡して「現場のトレンド」を抽出させた結果。"
    )
    lines.append("")

    et = narrative.get("emerging_themes", []) or []
    lines.append("### 4.1 新興テーマ")
    lines.append("")
    for item in et:
        lines.append(f"**{item.get('theme', '?')}**")
        lines.append("")
        lines.append(item.get("description", ""))
        ex = item.get("example_titles") or []
        if ex:
            lines.append("")
            lines.append("代表的なタイトル:")
            for t in ex[:5]:
                lines.append(f"- {t}")
        lines.append("")

    lines.append("### 4.2 ホットな細分野")
    lines.append("")
    for x in narrative.get("hot_subfields", []) or []:
        lines.append(f"- {x}")
    lines.append("")

    lines.append("### 4.3 横断的な手法トレンド")
    lines.append("")
    for x in narrative.get("methodological_trends", []) or []:
        lines.append(f"- {x}")
    lines.append("")

    lines.append("### 4.4 新しい応用領域")
    lines.append("")
    for x in narrative.get("novel_applications", []) or []:
        lines.append(f"- {x}")
    lines.append("")

    lines.append("### 4.5 意外な観測")
    lines.append("")
    for x in narrative.get("surprises", []) or []:
        lines.append(f"- {x}")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv", default=DEFAULT_CSV)
    p.add_argument("-o", "--output", default=DEFAULT_OUT)
    p.add_argument("--n-clusters", type=int, default=DEFAULT_K)
    p.add_argument("--model", default=DEFAULT_LLM, help=f"LLM for labeling/narrative (default: {DEFAULT_LLM})")
    p.add_argument("--label-workers", type=int, default=6)
    p.add_argument("--no-cvpr-filter", action="store_true", help="include is_cvpr2026=no/unsure")
    args = p.parse_args()

    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    if not os.getenv("OPENAI_API_KEY"):
        print("error: OPENAI_API_KEY is not set", file=sys.stderr)
        return 1

    print(f"==> loading {args.csv}")
    rows = load_papers(args.csv, cvpr_only=not args.no_cvpr_filter)
    print(f"    {len(rows)} papers")
    if not rows:
        print("error: nothing to analyze", file=sys.stderr)
        return 1

    client = OpenAI()

    print(f"==> [1/4] embedding {len(rows)} docs with {EMBED_MODEL}")
    docs = [build_doc(r) for r in rows]
    embs = embed_all(client, docs)
    print(f"    embedding matrix: {embs.shape}")

    print(f"==> [2/4] KMeans({args.n_clusters})")
    labels, centroids = cluster_papers(embs, args.n_clusters)
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    embs_norm = embs / np.where(norms == 0, 1.0, norms)
    rep_idx = closest_to_centroid(embs_norm, labels, centroids, k=10)
    cluster_kws = top_keywords_per_cluster(rows, labels, top_n=8)

    print(f"==> [3/4] labeling clusters via {args.model} ({args.label_workers} workers)")
    cluster_labels: dict[int, dict] = {}

    def _label(c: int) -> tuple[int, dict]:
        titles = [rows[i].get("title", "") for i in rep_idx.get(c, [])]
        kws = cluster_kws.get(c, [])
        try:
            return c, label_cluster(client, args.model, c, titles, kws)
        except Exception as e:
            return c, {"label": f"cluster-{c}", "what_is_distinctive": f"(label failed: {e})"}

    with ThreadPoolExecutor(max_workers=args.label_workers) as ex:
        futures = [ex.submit(_label, c) for c in range(args.n_clusters)]
        for fut in as_completed(futures):
            c, meta = fut.result()
            cluster_labels[c] = meta
            print(f"    cluster {c}: {meta.get('label', '?')}")

    print(f"==> [4/4] LLM narrative via {args.model} (single call, full list)")
    lines = [build_condensed(r) for r in rows]
    try:
        narrative = run_narrative(client, args.model, lines)
    except Exception as e:
        print(f"warning: narrative call failed: {e}", file=sys.stderr)
        narrative = {
            "emerging_themes": [],
            "hot_subfields": [f"(narrative failed: {e})"],
            "methodological_trends": [],
            "novel_applications": [],
            "surprises": [],
        }

    top_kws = overall_top_keywords(rows, top_n=50)

    md = render_markdown(
        rows,
        labels,
        rep_idx,
        cluster_labels,
        cluster_kws,
        top_kws,
        narrative,
        llm_model=args.model,
    )
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"==> wrote {args.output} ({len(md):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

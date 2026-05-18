#!/usr/bin/env python3
"""Deep-read an arXiv paper with GPT and emit a Japanese structured summary.

Downloads the PDF, uploads it to OpenAI Files, and asks gpt-4o-mini to fill
a fixed JSON schema (Standard format). The result is written to
``outputs/deep_reads/<arxiv_id>.json`` and returned to the caller.

Used as a library by ``scripts/server.py`` (FastAPI endpoint) and as a CLI
for one-off runs.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from typing import Any

import httpx
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEEP_READ_DIR = os.path.join(REPO_ROOT, "outputs", "deep_reads")

DEFAULT_MODEL = "gpt-5-mini"
ALLOWED_MODELS = ("gpt-5-nano", "gpt-5-mini", "gpt-5.4-mini")
MAX_PDF_MB = 20  # Reject huge PDFs before they hit the OpenAI Files API.

SCHEMA = {
    "name": "deep_read_standard_ja",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "tldr",
            "problem_motivation",
            "proposed_method",
            "key_results",
            "strengths_weaknesses",
            "related_work_diff",
        ],
        "properties": {
            "tldr": {
                "type": "string",
                "description": "論文の要点を1〜2文の日本語で。具体的な手法名・タスク名を含めること。",
            },
            "problem_motivation": {
                "type": "string",
                "description": "解こうとしている課題と、なぜそれが重要か (3〜5文の日本語)。既存研究の限界も短く触れる。",
            },
            "proposed_method": {
                "type": "string",
                "description": "提案手法を構造的に。入力→処理→出力の流れ、モジュール構成、損失/学習設定、推論手順を箇条書きまたは段落で具体的に (5〜10文程度の日本語)。",
            },
            "key_results": {
                "type": "array",
                "items": {"type": "string"},
                "description": "主要な定量・定性結果を3〜6個の短い箇条書き (日本語)。ベンチマーク名・指標・対比対象・改善幅を必ず数値で示す。",
            },
            "strengths_weaknesses": {
                "type": "object",
                "additionalProperties": False,
                "required": ["strengths", "weaknesses"],
                "properties": {
                    "strengths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "強み・新規性のポイント (日本語) 2〜4個。",
                    },
                    "weaknesses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "限界・批判点・未検証の論点 (日本語) 1〜4個。論文本体で著者が述べる限界に加え、評価設定の弱点があれば指摘する。",
                    },
                },
            },
            "related_work_diff": {
                "type": "string",
                "description": "最も近い既存研究との差分を具体名 (論文名や手法名) を挙げて2〜4文の日本語で。何が新しく、なぜそれが効くのか。",
            },
        },
    },
}

SYSTEM_PROMPT = (
    "あなたはコンピュータビジョン/機械学習の研究者向けに論文を精読して日本語で要約するアシスタントです。"
    "添付されたPDFを精読し、指定された JSON スキーマに厳密に従って構造化サマリーを返してください。\n\n"
    "厳守事項:\n\n"
    "## 1. 表記ルール (最重要)\n"
    "助詞・動詞・接続詞・一般的な説明文は日本語で書く。ただし以下は **必ず英語のまま** 書き、"
    "カタカナに置き換えない:\n"
    "  - 手法名・モデル名・アーキテクチャ名 (e.g. Transformer, ResNet, NeRF, CLIP, ViT)\n"
    "  - タスク名・問題設定 (e.g. semantic segmentation, person re-identification, "
    "lifelong learning, domain adaptation)\n"
    "  - 概念・技術用語 (e.g. attention, fine-tuning, distillation, embedding, backbone, "
    "self-supervised, semantic drift, catastrophic forgetting, downstream)\n"
    "  - データセット名・指標名 (e.g. ImageNet, COCO, mAP, IoU, FID, dataset, benchmark)\n"
    "  - 一般的な ML 用語 (e.g. model, task, parameter, epoch, batch, class, pixel, feature)\n\n"
    "**悪い例 (カタカナ化禁止)**: セマンティックドリフト, カタストロフィックフォゲッティング, "
    "ライフロング, アテンション, トランスフォーマー, ファインチューニング, ダウンストリーム, "
    "バックボーン, ディスティレーション, ロバストネス, ジェネラリゼーション, データセット, "
    "ベンチマーク, モデル, タスク, パラメータ, エポック, バッチ, クラス, ピクセル, フィーチャ。\n\n"
    "**良い例 (英語のまま)**: semantic drift, catastrophic forgetting, lifelong, attention, "
    "Transformer, fine-tuning, downstream, backbone, distillation, robustness, generalization, "
    "dataset, benchmark, model, task, parameter, epoch, batch, class, pixel, feature。\n\n"
    "初出時に短い日本語訳を () で添えるのは可: 'lifelong learning (継続学習)'。冗長にしない。\n\n"
    "## 2. 内容ルール\n"
    "  - 推測ではなく論文本体の記述にもとづいて書く。値や指標は論文に書かれている数値をそのまま使う。\n"
    "  - 'key_results' は必ず数値や具体的なベンチマーク名を含める "
    "(例: 'ScanNet で IoU +2.3pt 改善', 'A100で 1.7x 高速化')。\n"
    "  - 'related_work_diff' は具体的な比較対象 (論文名・手法名) を最低1つ挙げる。"
    "論文内に明示されている比較を優先する。\n"
    "  - 不明な点は無理に補完しない。論文に書かれていない場合は 'weaknesses' に "
    "'〜は評価されていない' のように書く。\n"
    "  - 冗長な前置きや結びは入れない。スキーマで指定された情報だけを返す。"
)


@dataclass
class DeepReadResult:
    id: str
    generated_at: str
    model: str
    sections: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "generated_at": self.generated_at,
            "model": self.model,
            "sections": self.sections,
        }


def norm_id(raw: str) -> str:
    """Normalize an arXiv id or URL to a bare id (e.g. ``2605.05328``).

    Accepts: ``2605.05328``, ``2605.05328v2``, ``arXiv:2605.05328``,
    ``https://arxiv.org/abs/2605.05328v1``, ``http://arxiv.org/pdf/...``.
    """
    s = raw.strip()
    s = re.sub(r"^https?://arxiv\.org/(abs|pdf)/", "", s)
    s = re.sub(r"^arXiv:", "", s, flags=re.IGNORECASE)
    s = s.removesuffix(".pdf")
    s = re.sub(r"v\d+$", "", s)
    if not re.match(r"^\d{4}\.\d{4,5}$", s) and not re.match(r"^[a-z\-]+/\d+$", s):
        raise ValueError(f"not a recognizable arxiv id: {raw!r}")
    return s


def result_path(arxiv_id: str) -> str:
    return os.path.join(DEEP_READ_DIR, f"{arxiv_id}.json")


INDEX_PATH = os.path.join(DEEP_READ_DIR, "index.json")


def rebuild_index() -> dict[str, dict[str, str]]:
    """Scan outputs/deep_reads/*.json and rewrite index.json.

    Index format: {"<arxiv_id>": {"model": "...", "generated_at": "..."}}.
    The frontend reads it once at load to show a 🤖 indicator on rows that
    already have a cached deep-read, without N HEAD requests.
    """
    if not os.path.isdir(DEEP_READ_DIR):
        return {}
    entries: dict[str, dict[str, str]] = {}
    for name in os.listdir(DEEP_READ_DIR):
        if not name.endswith(".json") or name == "index.json":
            continue
        path = os.path.join(DEEP_READ_DIR, name)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        arxiv_id = data.get("id") or name.removesuffix(".json")
        entries[arxiv_id] = {
            "model": data.get("model", ""),
            "generated_at": data.get("generated_at", ""),
        }
    # Atomic write so concurrent generation threads can't read a half-written index.
    tmp = INDEX_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, sort_keys=True, indent=2)
    os.replace(tmp, INDEX_PATH)
    return entries


def load_cached(arxiv_id: str) -> dict[str, Any] | None:
    p = result_path(arxiv_id)
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


class PdfTooLargeError(RuntimeError):
    """Raised when an arXiv PDF exceeds MAX_PDF_MB. Caught and surfaced to the UI."""


class PdfTooLargeError(RuntimeError):
    """Raised when an arXiv PDF exceeds MAX_PDF_MB and the caller did not pass
    ``force_size=True``. Carries ``size_mb`` so the API can surface it to the UI."""

    def __init__(self, message: str, size_mb: float) -> None:
        super().__init__(message)
        self.size_mb = size_mb


def head_pdf_size_mb(arxiv_id: str, timeout: float = 15.0) -> float | None:
    """Return PDF size in MB via HEAD request, or None if size can't be determined.

    Used by the API layer to check size before kicking off a worker thread, so
    that callers can decide to bypass the limit before paying the OpenAI call.
    """
    arxiv_id = norm_id(arxiv_id)
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as cli:
            h = cli.head(url)
            if h.status_code == 200:
                cl = h.headers.get("content-length")
                if cl:
                    return int(cl) / 1024 / 1024
    except httpx.HTTPError:
        pass
    return None


def _download_pdf(
    arxiv_id: str, dest_path: str, timeout: float = 90.0, force_size: bool = False
) -> None:
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    max_bytes = MAX_PDF_MB * 1024 * 1024
    with httpx.Client(timeout=timeout, follow_redirects=True) as cli:
        # HEAD first to fail fast on huge PDFs without wasting bandwidth.
        if not force_size:
            try:
                h = cli.head(url)
                if h.status_code == 200:
                    cl = h.headers.get("content-length")
                    if cl and int(cl) > max_bytes:
                        size_mb = int(cl) / 1024 / 1024
                        raise PdfTooLargeError(
                            f"PDF is {size_mb:.1f}MB, exceeds {MAX_PDF_MB}MB limit "
                            f"(arxiv:{arxiv_id})",
                            size_mb=size_mb,
                        )
            except PdfTooLargeError:
                raise
            except httpx.HTTPError:
                pass  # HEAD failed — fall through to GET, where we re-check after download.

        r = cli.get(url)
        r.raise_for_status()
        ct = r.headers.get("content-type", "")
        if "pdf" not in ct.lower() and not r.content[:4] == b"%PDF":
            raise RuntimeError(f"unexpected content-type for {url}: {ct!r}")
        # Defensive: re-check after download in case HEAD didn't return content-length.
        if not force_size and len(r.content) > max_bytes:
            size_mb = len(r.content) / 1024 / 1024
            raise PdfTooLargeError(
                f"PDF is {size_mb:.1f}MB, exceeds {MAX_PDF_MB}MB limit "
                f"(arxiv:{arxiv_id})",
                size_mb=size_mb,
            )
        with open(dest_path, "wb") as f:
            f.write(r.content)


def deep_read(
    arxiv_id: str,
    *,
    model: str = DEFAULT_MODEL,
    overwrite: bool = False,
    force_size: bool = False,
    client: OpenAI | None = None,
) -> DeepReadResult:
    """Run the full deep-read pipeline for one arxiv id and persist the result.

    If ``outputs/deep_reads/<id>.json`` already exists and ``overwrite`` is False,
    returns the cached result without any API calls. ``force_size=True`` bypasses
    the MAX_PDF_MB safety check (caller has confirmed they want to run anyway).
    """
    if model not in ALLOWED_MODELS:
        raise ValueError(f"model {model!r} not in {ALLOWED_MODELS}")
    arxiv_id = norm_id(arxiv_id)
    os.makedirs(DEEP_READ_DIR, exist_ok=True)

    if not overwrite:
        cached = load_cached(arxiv_id)
        if cached is not None:
            return DeepReadResult(
                id=cached["id"],
                generated_at=cached["generated_at"],
                model=cached["model"],
                sections=cached["sections"],
            )

    if client is None:
        load_dotenv(os.path.join(REPO_ROOT, ".env"))
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set (put it in .env)")
        client = OpenAI()

    tmp_pdf = os.path.join(DEEP_READ_DIR, f".{arxiv_id}.tmp.pdf")
    file_id: str | None = None
    try:
        _download_pdf(arxiv_id, tmp_pdf, force_size=force_size)

        with open(tmp_pdf, "rb") as fh:
            uploaded = client.files.create(file=fh, purpose="user_data")
        file_id = uploaded.id

        last_err: Exception | None = None
        for attempt in range(1, 4):
            try:
                # Note: GPT-5 family only allows temperature=1 (default), so we don't pass it.
                # Structured outputs via json_schema guarantee the format regardless.
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "file",
                                    "file": {"file_id": file_id},
                                },
                                {
                                    "type": "text",
                                    "text": (
                                        f"arXiv:{arxiv_id} を精読し、指定スキーマに従って日本語で構造化サマリーを返してください。"
                                    ),
                                },
                            ],
                        },
                    ],
                    response_format={"type": "json_schema", "json_schema": SCHEMA},
                )
                sections = json.loads(resp.choices[0].message.content)
                break
            except OpenAIError as e:
                last_err = e
                if attempt < 3:
                    time.sleep(2 * attempt)
        else:
            raise RuntimeError(f"OpenAI call failed after retries: {last_err}")

        result = DeepReadResult(
            id=arxiv_id,
            generated_at=_dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
            model=model,
            sections=sections,
        )
        with open(result_path(arxiv_id), "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        try:
            rebuild_index()
        except OSError:
            pass
        return result
    finally:
        if file_id is not None:
            try:
                client.files.delete(file_id)
            except Exception:
                pass
        if os.path.exists(tmp_pdf):
            try:
                os.remove(tmp_pdf)
            except OSError:
                pass


def main() -> int:
    p = argparse.ArgumentParser(description="Deep-read an arXiv paper with GPT.")
    p.add_argument("arxiv_id", nargs="?", help="arXiv id (e.g. 2605.05328) or abs/pdf URL")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenAI model (default: {DEFAULT_MODEL})")
    p.add_argument("--overwrite", action="store_true", help="re-run even if a cached result exists")
    p.add_argument("--force-size", action="store_true", help=f"bypass {MAX_PDF_MB}MB PDF size limit")
    p.add_argument(
        "--rebuild-index",
        action="store_true",
        help="rescan outputs/deep_reads/ and rewrite index.json, then exit",
    )
    args = p.parse_args()

    if args.rebuild_index:
        entries = rebuild_index()
        print(f"wrote {INDEX_PATH} ({len(entries)} entries)")
        return 0

    if not args.arxiv_id:
        p.error("arxiv_id is required unless --rebuild-index is given")

    try:
        result = deep_read(
            args.arxiv_id,
            model=args.model,
            overwrite=args.overwrite,
            force_size=args.force_size,
        )
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"wrote {result_path(result.id)}")
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

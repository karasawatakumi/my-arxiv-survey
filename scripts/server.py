#!/usr/bin/env python3
"""Local server: static viewer + deep-read API.

Replaces ``python -m http.server`` for development. Serves ``index.html``,
``outputs/`` files, and exposes:

    POST /api/deep-read/{arxiv_id}        kick off (or short-circuit if cached)
    GET  /api/deep-read/{arxiv_id}        poll job status / fetch result
    GET  /api/health                      liveness probe used by the frontend

Bind: ``127.0.0.1:8765`` only. Do NOT expose to LAN — the deep-read endpoint
spends OpenAI credits.

Run:
    uv run scripts/server.py
"""

from __future__ import annotations

import os
import sys
import threading
import traceback
from dataclasses import dataclass, field
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deep_read import (  # noqa: E402
    ALLOWED_MODELS,
    DEFAULT_MODEL,
    MAX_PDF_MB,
    deep_read,
    head_pdf_size_mb,
    load_cached,
    norm_id,
    rebuild_index,
    result_path,
)

JobStatus = Literal["running", "done", "error"]


@dataclass
class Job:
    status: JobStatus = "running"
    error: str | None = None
    started_at: float = field(default_factory=lambda: __import__("time").time())


_jobs: dict[str, Job] = {}
_jobs_lock = threading.Lock()

app = FastAPI(title="arxiv-survey local")


def _run_job(arxiv_id: str, model: str, overwrite: bool, force_size: bool) -> None:
    try:
        deep_read(arxiv_id, model=model, overwrite=overwrite, force_size=force_size)
        with _jobs_lock:
            _jobs[arxiv_id] = Job(status="done")
    except Exception as e:
        traceback.print_exc()
        with _jobs_lock:
            _jobs[arxiv_id] = Job(status="error", error=f"{type(e).__name__}: {e}")


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "default_model": DEFAULT_MODEL, "allowed_models": list(ALLOWED_MODELS)}


@app.post("/api/deep-read/{arxiv_id:path}")
def start_deep_read(
    arxiv_id: str,
    overwrite: bool = False,
    model: str = DEFAULT_MODEL,
    force: bool = False,
) -> JSONResponse:
    try:
        nid = norm_id(arxiv_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if model not in ALLOWED_MODELS:
        raise HTTPException(
            status_code=400, detail=f"model {model!r} not in {list(ALLOWED_MODELS)}"
        )

    cached = load_cached(nid)
    if cached is not None and not overwrite:
        return JSONResponse({"id": nid, "status": "done", "result": cached})

    # Pre-flight PDF size check so the UI can prompt the user before any OpenAI
    # spend. ``force=true`` bypasses (user has confirmed they want to run anyway).
    if not force:
        size_mb = head_pdf_size_mb(nid)
        if size_mb is not None and size_mb > MAX_PDF_MB:
            return JSONResponse(
                {
                    "id": nid,
                    "status": "too_large",
                    "size_mb": round(size_mb, 1),
                    "limit_mb": MAX_PDF_MB,
                    "detail": (
                        f"PDF is {size_mb:.1f}MB, exceeds {MAX_PDF_MB}MB limit. "
                        f"Re-POST with force=true to run anyway."
                    ),
                },
                status_code=413,
            )

    with _jobs_lock:
        existing = _jobs.get(nid)
        if existing and existing.status == "running":
            return JSONResponse({"id": nid, "status": "running"})
        _jobs[nid] = Job(status="running")

    print(
        f"[deep-read] start {nid} model={model} overwrite={overwrite} force={force}",
        flush=True,
    )
    threading.Thread(
        target=_run_job, args=(nid, model, overwrite, force), daemon=True
    ).start()
    return JSONResponse({"id": nid, "status": "running"}, status_code=202)


@app.get("/api/deep-read/{arxiv_id:path}")
def get_deep_read(arxiv_id: str) -> JSONResponse:
    try:
        nid = norm_id(arxiv_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    with _jobs_lock:
        job = _jobs.get(nid)

    if job and job.status == "running":
        return JSONResponse({"id": nid, "status": "running"})

    # If the most recent attempt errored, surface that first — otherwise a stale
    # cached file would mask the failure as a successful (but unchanged) result.
    if job and job.status == "error":
        return JSONResponse(
            {"id": nid, "status": "error", "error": job.error}, status_code=500
        )

    cached = load_cached(nid)
    if cached is not None:
        return JSONResponse({"id": nid, "status": "done", "result": cached})

    return JSONResponse({"id": nid, "status": "not_started"}, status_code=404)


app.mount("/", StaticFiles(directory=REPO_ROOT, html=True), name="static")


def main() -> int:
    import uvicorn

    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    if not os.getenv("OPENAI_API_KEY"):
        print(
            "warning: OPENAI_API_KEY is not set — static serving will work but /api/deep-read will fail.",
            file=sys.stderr,
        )
    print("note: deep-read result file is outputs/deep_reads/<id>.json — git-tracked.")
    try:
        n = len(rebuild_index())
        print(f"note: rebuilt deep-read index ({n} entries).")
    except OSError as e:
        print(f"warning: could not rebuild deep-read index: {e}", file=sys.stderr)
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="info")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Worker startup script for the Stockfish analysis pipeline.

Requires RUNPOD_ENDPOINT_ID and RUNPOD_API_KEY to be set.

Optional env vars forwarded to the RunPod worker:
    ANALYSIS_DEPTH     — Stockfish search depth (default: 20)
    ANALYSIS_THREADS   — Threads per analysis (default: 8)
    ANALYSIS_HASH_MB   — Hash table size in MB (default: 2048)
    SF_POLL_INTERVAL   — Seconds between submission sweeps (default: 60)
"""
from __future__ import annotations

import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("start_workers")


def main() -> None:
    if not os.environ.get("RUNPOD_ENDPOINT_ID"):
        log.error("RUNPOD_ENDPOINT_ID is not set. This service requires a RunPod endpoint.")
        sys.exit(1)

    if not os.environ.get("RUNPOD_API_KEY"):
        log.error("RUNPOD_API_KEY is not set. This service requires a RunPod API key.")
        sys.exit(1)

    log.info("Starting RunPod job submitter")
    from stockfish_pipeline.ingest.job_submitter import run_submitter_loop
    run_submitter_loop()


if __name__ == "__main__":
    main()

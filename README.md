# woodland-chess-pipeline

Standalone ingest and analysis code extracted from Woodland Chess.

This repository contains:
- Chess.com ingest pipeline
- Analysis job queueing and worker execution
- Stockfish move-by-move analysis services
- SQLAlchemy models and DB bootstrap/migrations required for ingest/analysis
- Lichess opening-book TSV data for opening labeling

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Configure `.env` with at least:
- `CHESS_COM_USERNAMES` (comma-separated)
- `DATABASE_URL` (optional; defaults to local SQLite)
- `STOCKFISH_PATH` (optional; auto-detected if available on PATH)

## Sync games from Chess.com

```bash
python -m woodland_pipeline.ingest.run_sync
```

Options:
- `--usernames alice,bob` to override env usernames

## Queue analysis jobs

```bash
python -m woodland_pipeline.ingest.run_analysis_worker --enqueue-only
```

## Run Stockfish worker

```bash
python -m woodland_pipeline.ingest.run_analysis_worker --no-poll
```

Useful flags:
- `--stockfish /path/to/stockfish`
- `--depth 20`
- `--threads 1`
- `--limit 100`
- `--status`

## Combined enqueue + analyze

```bash
python -m woodland_pipeline.ingest.run_analysis_worker --enqueue --no-poll
```

## Notes

- The pipeline defaults to SQLite (`woodland_chess.db`) when `DATABASE_URL` is not set.
- PostgreSQL is recommended for concurrent workers.
- Queue claiming uses `FOR UPDATE SKIP LOCKED` on PostgreSQL.

## Deploy to Railway (polling analysis processor)

This repo is configured for Railway Config-as-Code + Docker build so Stockfish is available at runtime.

Included deployment files:
- `railway.toml` (builder + start command)
- `Dockerfile` (installs Python deps and Stockfish)
- `.dockerignore`

### 1. Create Railway services

- Create a new Railway project from this GitHub repo.
- Add a **PostgreSQL** service in Railway.
- Keep this worker as a **private service** (no public domain required).

### 2. Set environment variables

Set these on the worker service:
- `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
- `CHESS_COM_USERNAMES` = `alice,bob` (or your username list)
- `ANALYSIS_DEPTH` = `20` (optional)
- `ANALYSIS_THREADS` = `1` (optional)

Optional overrides:
- `STOCKFISH_PATH=/usr/games/stockfish`
- `CHESS_COM_USER_AGENT=woodland-chess-pipeline/0.1`

### 3. Deploy

Push to `main` (or trigger a manual deploy).

This service starts with:

```bash
python -m woodland_pipeline.ingest.run_analysis_worker
```

That command runs in polling mode by default, continuously checking the queue for new pending jobs.

### 4. Enqueue jobs

This worker only processes queued jobs. Enqueue jobs using one of these patterns:

- one-off local/CLI run:

```bash
python -m woodland_pipeline.ingest.run_analysis_worker --enqueue-only
```

- separate Railway service or cron job that runs enqueue logic.

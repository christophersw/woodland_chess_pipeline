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

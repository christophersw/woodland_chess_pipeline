FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STOCKFISH_PATH=/usr/local/bin/stockfish

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        tar \
    && rm -rf /var/lib/apt/lists/*

# Install CPU-optimized Stockfish sf_18 (avx2 — safe for all x86_64 hosts from ~2013+,
# significantly faster than the unoptimized Debian package).
RUN curl -fsSL "https://github.com/official-stockfish/Stockfish/releases/download/sf_18/stockfish-ubuntu-x86-64-avx2.tar" \
        -o /tmp/stockfish.tar \
    && tar -xf /tmp/stockfish.tar -C /tmp \
    && find /tmp -name "stockfish*" -type f -perm /111 | head -1 | xargs -I{} mv {} /usr/local/bin/stockfish \
    && chmod +x /usr/local/bin/stockfish \
    && rm -f /tmp/stockfish.tar

COPY pyproject.toml README.md ./
COPY woodland_pipeline ./woodland_pipeline
COPY start_workers.py ./

RUN pip install --no-cache-dir .

CMD ["python", "start_workers.py"]

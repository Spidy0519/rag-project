FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync --frozen

COPY . .

ENV PYTHONUNBUFFERED=1
ENV HF_HUB_DISABLE_TELEMETRY=1

EXPOSE ${PORT:-5000}

CMD ["uv", "run", "python", "app.py"]

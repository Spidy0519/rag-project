FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV HF_HUB_DISABLE_TELEMETRY=1
ENV CHROMA_MODE=memory

EXPOSE 7860

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]

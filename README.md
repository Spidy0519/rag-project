---
title: RAG Assistant
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.44.1
app_file: app.py
pinned: false
---

# RAG Assistant

Hybrid RAG system for programming questions (Python, Java, C) with document upload support.

## Tech Stack

| Layer | Tool |
|---|---|
| Backend | FastAPI + Uvicorn |
| Vector DB | Pinecone (serverless, free tier) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Google Gemini API (gemini-3.5-flash-lite) |
| Web scraping | requests + BeautifulSoup4 |
| Document parsing | pypdf, python-docx, pandas |
| Frontend | Gradio (HF Spaces) / HTML+CSS+JS (Render) |

## Setup (Local)

```bash
pip install -r requirements-prod.txt
cp .env.example .env
```

Add your API keys to `.env`:
```
GEMINI_API_KEY=your_gemini_key
PINECONE_API_KEY=your_pinecone_key
```

## Run (Local)

```bash
python app.py
```

## Deploy

### Hugging Face Spaces (Free)
1. Create Space → SDK: **Gradio**
2. Add Secrets: `GEMINI_API_KEY`, `PINECONE_API_KEY`
3. Push code — builds automatically

### Render (Docker)
1. Create Web Service → Runtime: **Docker**
2. Add env vars: `GEMINI_API_KEY`, `PINECONE_API_KEY`
3. Uses `main.py` (FastAPI) via Dockerfile

## Features

- **Chat** — Ask programming questions, get answers with source citations
- **Upload** — Drag-drop PDF, DOCX, CSV, XLSX, TXT, MD files
- **Scrape** — Scrape Python/Java/C docs or add custom URLs

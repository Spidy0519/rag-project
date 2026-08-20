---
title: RAG Assistant
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# RAG Assistant

Hybrid RAG system for programming questions (Python, Java, C) with document upload support.

## Tech Stack

| Layer | Tool |
|---|---|
| Package manager | pip |
| Backend | Flask + Gunicorn |
| Web scraping | requests + BeautifulSoup4 |
| Document parsing | pypdf, python-docx, pandas |
| Chunking | Custom recursive splitter (500 chars, 100 overlap) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB (in-memory) |
| LLM | Google Gemini API (gemini-3.5-flash-lite) |
| Frontend | HTML + CSS + vanilla JS |

## Setup (Local)

```bash
pip install -r requirements.txt
cp .env.example .env
```

Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_key_here
```

Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).

## Run (Local)

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

## Deploy to Hugging Face Spaces

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose **Docker** as the SDK
3. Push this code to the Space repo
4. Add **Secret** in Space Settings:
   - `GEMINI_API_KEY` = your API key
5. Build starts automatically — live at `https://your-username.github.io/space-name`

> **Note:** In-memory ChromaDB — data resets on restart. Re-upload or re-scrape as needed.

## Features

- **Chat** — Ask programming questions, get answers with source citations
- **Upload** — Drag-drop PDF, DOCX, CSV, XLSX, TXT, MD files
- **Scrape** — Scrape Python/Java/C docs or add custom URLs

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/` | Chat UI |
| POST | `/upload` | Upload document |
| POST | `/scrape` | Scrape URLs |
| POST | `/ask` | Ask a question |
| GET | `/stats` | Vector store stats |

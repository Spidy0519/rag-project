# RAG Assistant

Hybrid RAG system for programming questions (Python, Java, C) with document upload support.

## Tech Stack

| Layer | Tool |
|---|---|
| Package manager | uv |
| Backend | Flask |
| Web scraping | requests + BeautifulSoup4 |
| Document parsing | pypdf, python-docx, pandas |
| Chunking | Custom recursive splitter (500 chars, 100 overlap) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB |
| LLM | Google Gemini API (gemini-3.5-flash-lite) |
| Frontend | HTML + CSS + vanilla JS |

## Setup

```bash
uv sync
cp .env.example .env
```

Add your Gemini API key to `.env`:

```
GEMINI_API_KEY=your_key_here
```

Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).

## Run

```bash
uv run python app.py
```

Open [http://localhost:5000](http://localhost:5000).

## Features

- **Chat** — Ask programming questions, get answers with source citations
- **Upload** — Drag-drop PDF, DOCX, CSV, XLSX, TXT, MD files
- **Scrape** — Scrape Python/Java/C docs or add custom URLs

## Project Structure

```
rag-project/
├── app.py                  # Flask entry point
├── config.py               # Configuration
├── scraper/
│   └── scrape_docs.py      # Web scraper
├── ingestion/
│   ├── document_parser.py  # Multi-format parser
│   └── chunker.py          # Text chunker
├── rag/
│   ├── embeddings.py       # Sentence-transformers
│   ├── vectorstore.py      # ChromaDB
│   └── generator.py        # Gemini RAG generation
├── static/
│   ├── css/style.css
│   └── js/main.js
├── templates/
│   └── index.html
├── uploads/
└── chroma_db/
```

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/` | Chat UI |
| POST | `/upload` | Upload document |
| POST | `/scrape` | Scrape URLs |
| POST | `/ask` | Ask a question |
| GET | `/stats` | Vector store stats |

## Deploy to Render

1. Push code to GitHub

2. Go to [render.com](https://render.com) → New → **Web Service**

3. Connect your GitHub repo

4. Render auto-detects `render.yaml`. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120`

5. Add env var:
   ```
   GEMINI_API_KEY = your_key_here
   ```

6. Add **Persistent Disk** (Settings → Disks):
   - Mount Path: `/app/chroma_db`
   - Size: 1 GB

7. Deploy — your app will be live at `https://your-app.onrender.com`

> **Note:** First deploy takes ~5 min (installing torch + sentence-transformers). Free tier spins down after 15 min of inactivity — first request after idle may take 30-60s to wake up.

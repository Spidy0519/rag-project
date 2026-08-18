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

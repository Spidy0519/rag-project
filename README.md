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
| Frontend | HTML + CSS + vanilla JS |

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

- Get Gemini key at [Google AI Studio](https://aistudio.google.com/apikey)
- Get Pinecone key at [pinecone.io](https://www.pinecone.io/) (free tier: 100K vectors)

## Run (Local)

```bash
python app.py
```

Open [http://localhost:7860](http://localhost:7860).

## Deploy to Render

1. Create a new **Web Service** at [render.com](https://render.com)
2. Connect your GitHub repository
3. Set environment: **Docker**
4. Add **Environment Variables**:
   - `GEMINI_API_KEY` = your Gemini API key
   - `PINECONE_API_KEY` = your Pinecone API key
5. Deploy

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

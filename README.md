# RAG Assistant

A Hybrid Retrieval-Augmented Generation (RAG) system for answering programming questions using Pinecone vector database and Google Gemini LLM.

## Live Demo

- **Hugging Face Spaces:** [https://huggingface.co/spaces/Rahuman0519/rag-chatbot](https://huggingface.co/spaces/Rahuman0519/rag-chatbot)

## Features

- **Chat** — Ask programming questions (Python, Java, C) and get answers with source citations
- **Upload** — Upload documents (PDF, DOCX, CSV, XLSX, TXT, MD) for knowledge base
- **Scrape** — Scrape programming documentation from official sources

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| Frontend | Gradio (Hugging Face Spaces) |
| Vector Database | Pinecone (Serverless, Cloud) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Google Gemini API (gemini-3.5-flash-lite) |
| Document Parsing | pypdf, python-docx, pandas |
| Web Scraping | requests + BeautifulSoup4 |
| Language | Python 3.12 |

## Architecture

```
User Query
    │
    ▼
┌─────────────┐
│  Embedding   │  sentence-transformers (all-MiniLM-L6-v2)
│  Model       │  384-dimensional vectors
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Pinecone    │  Cosine similarity search (Top-K=3)
│  Vector DB   │  Serverless cloud database
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Gemini LLM  │  Context-aware answer generation
│              │  Temperature=0.3, Max tokens=1024
└──────┬──────┘
       │
       ▼
  Answer + Sources
```

## Project Structure

```
rag-project/
├── app.py                    # Gradio UI entry point
├── config.py                 # Configuration & environment variables
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── pyproject.toml            # Project metadata
├── .env.example              # Environment variable template
├── ingestion/
│   ├── document_parser.py    # PDF/DOCX/CSV/XLSX/TXT parsing
│   └── chunker.py            # Text chunking (500 chars, 100 overlap)
├── rag/
│   ├── embeddings.py         # Embedding generation
│   ├── vectorstore.py        # Pinecone vector operations
│   └── generator.py          # Gemini LLM answer generation
├── scraper/
│   └── scrape_docs.py        # Web scraping for programming docs
├── static/
│   ├── css/style.css         # UI stylesheet
│   └── js/main.js            # Frontend JavaScript
├── templates/
│   └── index.html            # HTML template
└── uploads/                  # Temporary file storage
```

## Setup

### Prerequisites

- Python 3.10+
- Pinecone account (free tier: 100K vectors)
- Google Gemini API key

### Installation

```bash
pip install -r requirements.txt
cp .env.example .env
```

### Environment Variables

Add your API keys to `.env`:

```
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=rag-assistant
```

### Run Locally

```bash
python app.py
```

Open [http://localhost:7860](http://localhost:7860)

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Chat UI |
| POST | `/ask` | Ask a question |
| POST | `/upload` | Upload document |
| POST | `/scrape` | Scrape URLs |
| GET | `/stats` | Vector store stats |

## Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Chunk Size | 500 | Characters per chunk |
| Chunk Overlap | 100 | Overlap between chunks |
| Embedding Model | all-MiniLM-L6-v2 | 384-dimensional vectors |
| Similarity Metric | Cosine | Vector similarity search |
| Top-K | 3 | Number of retrieved chunks |
| LLM Temperature | 0.3 | Response creativity |
| Max Tokens | 1024 | Maximum response length |

## Deployment

### Hugging Face Spaces (Free)

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Select **Gradio** as the SDK
3. Add Secrets: `GEMINI_API_KEY`, `PINECONE_API_KEY`
4. Push code — builds automatically

## Acknowledgements

- [Pinecone](https://www.pinecone.io/) — Vector database
- [Google Gemini](https://aistudio.google.com/) — Large language model
- [sentence-transformers](https://www.sbert.net/) — Embedding model
- [Hugging Face Spaces](https://huggingface.co/spaces) — Deployment platform

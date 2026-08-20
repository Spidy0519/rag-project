# Project Report: RAG Assistant

## Hybrid Retrieval-Augmented Generation System for Programming Questions

---

## 1. Abstract

This project implements a Hybrid Retrieval-Augmented Generation (RAG) system that combines document retrieval with large language model (LLM) generation to answer programming questions. The system uses Pinecone as a cloud-based vector database for storing and retrieving document embeddings, sentence-transformers for generating embeddings, and Google Gemini for generating context-aware answers. The application supports document upload, web scraping of programming documentation, and interactive chat through a web-based interface.

---

## 2. Introduction

### 2.1 Problem Statement

Programming learners and developers often need to search through extensive documentation to find specific answers. Traditional keyword-based search methods may not capture semantic meaning, leading to irrelevant results. This project addresses this challenge by implementing a RAG system that understands the context of queries and retrieves semantically relevant information.

### 2.2 Objectives

- Build a RAG system that combines retrieval and generation for accurate programming Q&A
- Implement document ingestion pipeline for PDF, DOCX, CSV, XLSX, and TXT files
- Integrate web scraping to automatically ingest programming documentation
- Provide a user-friendly chat interface with source citations
- Deploy the application as a free cloud service

---

## 3. Literature Review

### 3.1 Retrieval-Augmented Generation (RAG)

RAG is a technique that enhances LLM responses by retrieving relevant documents from a knowledge base before generating answers. This approach reduces hallucinations and provides factual, source-backed responses.

### 3.2 Vector Embeddings

Vector embeddings represent text as dense numerical vectors in high-dimensional space. Similar texts produce similar vectors, enabling semantic search. The all-MiniLM-L6-v2 model generates 384-dimensional embeddings optimized for semantic similarity tasks.

### 3.3 Vector Databases

Vector databases like Pinecone store embeddings and support efficient similarity search using algorithms like approximate nearest neighbor (ANN). Pinecone provides a serverless, managed solution with cosine similarity metric.

---

## 4. System Architecture

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                    User Interface                    │
│                   (Gradio / Web)                     │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  Application Layer                   │
│                   (FastAPI)                          │
├──────────────────┬───────────────┬──────────────────┤
│   Ingestion      │   Retrieval   │   Generation     │
│   Pipeline       │   Pipeline    │   Pipeline       │
├──────────────────┼───────────────┼──────────────────┤
│ - Document Parser│ - Embed Query │ - Gemini LLM     │
│ - Chunker        │ - Pinecone    │ - Prompt Builder  │
│ - Embedder       │   Similarity  │ - Response        │
│                  │   Search      │   Formatter       │
└──────────────────┴───────┬───────┴──────────────────┘
                           │
              ┌────────────▼────────────┐
              │    Pinecone (Cloud)      │
              │    Vector Database       │
              └─────────────────────────┘
```

### 4.2 Data Flow

**Ingestion Flow:**
1. User uploads document or triggers web scraping
2. Document is parsed to extract raw text
3. Text is chunked into 500-character segments with 100-character overlap
4. Each chunk is embedded using sentence-transformers (384-dim)
5. Embeddings are upserted to Pinecone with metadata

**Query Flow:**
1. User sends a question through the chat interface
2. Question is embedded using the same embedding model
3. Top-3 most similar chunks are retrieved from Pinecone
4. Retrieved chunks are formatted as context for Gemini
5. Gemini generates a concise answer with source citations

---

## 5. Implementation

### 5.1 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Backend | FastAPI | 0.115.12 | REST API framework |
| Vector DB | Pinecone | 9.1.0 | Cloud vector database |
| Embeddings | sentence-transformers | 6.0.0 | Text embedding model |
| LLM | Google Gemini | 2.18.1 | Answer generation |
| Scraping | BeautifulSoup4 | 4.15.0 | HTML parsing |
| PDF Parsing | pypdf | 6.16.1 | PDF text extraction |
| Frontend | Gradio | 5.x | Web interface |

### 5.2 Document Parsing

The system supports multiple file formats through a unified parsing interface:

- **PDF:** Extracts text page-by-page using pypdf
- **DOCX:** Extracts paragraphs using python-docx
- **CSV/XLSX:** Converts spreadsheet data to text using pandas
- **TXT/MD:** Reads plain text with encoding detection (UTF-8, Latin-1, CP1252)

### 5.3 Text Chunking

Documents are split into overlapping chunks for optimal retrieval:

- **Chunk Size:** 500 characters
- **Overlap:** 100 characters (ensures context continuity)
- **Metadata:** Each chunk retains source information and filename

### 5.4 Embedding Generation

The all-MiniLM-L6-v2 model generates 384-dimensional dense vectors:

- **Model:** all-MiniLM-L6-v2 (90.9 MB)
- **Dimensions:** 384
- **Batch Size:** 32
- **Device:** CPU

### 5.5 Vector Storage (Pinecone)

- **Index Name:** rag-assistant
- **Dimension:** 384
- **Metric:** Cosine similarity
- **Cloud:** AWS us-east-1
- **Free Tier:** 100,000 vectors

### 5.6 Answer Generation (Gemini)

- **Model:** gemini-3.5-flash-lite
- **Temperature:** 0.3 (conservative)
- **Max Tokens:** 1024
- **Retries:** 3 with exponential backoff for rate limiting
- **Prompt:** Context-based with retrieved chunks as source material

### 5.7 Web Scraping

Pre-configured sources for programming documentation:

| Source | URL |
|--------|-----|
| Python Basics | docs.python.org/3/tutorial/introduction.html |
| Python Data Structures | docs.python.org/3/tutorial/datastructures.html |
| Python Classes | docs.python.org/3/tutorial/classes.html |
| Python Errors | docs.python.org/3/tutorial/errors.html |
| Java Tutorial | dev.java/tutorial/ |
| Java Basics | dev.java/tutorial/basics/ |
| C Tutorial | learn-c.org/ |

---

## 6. User Interface

### 6.1 Chat Interface

- Real-time question answering
- Markdown-formatted responses with code block support
- Source citation chips linking to original documentation
- Typing indicator during processing
- 30-second request timeout with graceful error handling

### 6.2 Document Upload

- Drag-and-drop file upload
- Support for PDF, DOCX, CSV, XLSX, TXT, MD
- Real-time processing status
- Chunk count and character count feedback

### 6.3 Web Scraper

- One-click scraping of default documentation sources
- Custom URL scraping with optional label
- Per-source success/failure status reporting

---

## 7. Deployment

### 7.1 Platform: Hugging Face Spaces (Free)

- **SDK:** Gradio
- **Compute:** 2 vCPU, 16GB RAM
- **Storage:** Persistent file storage
- **URL:** https://huggingface.co/spaces/Rahuman0519/rag-chatbot

### 7.2 Environment Variables

| Variable | Description |
|----------|-------------|
| GEMINI_API_KEY | Google Gemini API authentication |
| PINECONE_API_KEY | Pinecone database authentication |
| PINECONE_INDEX_NAME | Pinecone index name (default: rag-assistant) |

---

## 8. Testing

### 8.1 Test Cases

| Test | Input | Expected Output | Status |
|------|-------|----------------|--------|
| Chat Query | "What are Python data structures?" | Answer with sources (lists, dicts, sets) | Pass |
| Chat Query | "Explain Java exception handling" | Answer with try-catch-finally explanation | Pass |
| Chat Query | "How does pointer work in C?" | Answer about memory addresses and dereferencing | Pass |
| File Upload | Python_Programs.pdf | Indexed with chunk count | Pass |
| Scrape Default | Click "Scrape Default Sources" | 7 sources scraped and indexed | Pass |
| Scrape URL | Custom URL input | Single URL scraped and indexed | Pass |
| Empty Query | Submit empty message | "No query provided" error | Pass |
| Invalid File | Empty file upload | "Could not extract text" message | Pass |

### 8.2 Performance Metrics

| Metric | Value |
|--------|-------|
| Embedding Time (per chunk) | ~5ms |
| Pinecone Query Time | ~20ms |
| Gemini Response Time | ~2-5s |
| Model Load Time (first run) | ~30s |
| Model Load Time (cached) | ~3s |

---

## 9. Limitations

1. **Free Tier Constraints:** Pinecone free tier limited to 100K vectors
2. **No GPU:** Embedding model runs on CPU for free deployment
3. **Rate Limits:** Gemini API has rate limits on free tier
4. **Static Scraping:** Web scraper cannot handle JavaScript-rendered pages
5. **No Authentication:** No user authentication system implemented
6. **Ephemeral Uploads:** Uploaded files are processed and deleted immediately

---

## 10. Future Enhancements

1. **User Authentication:** Add login system for personalized experience
2. **Chat History:** Store conversation history for context continuity
3. **Multi-language Support:** Extend beyond Python, Java, C documentation
4. **Hybrid Search:** Combine semantic search with keyword-based BM25
5. **Fine-tuned Embeddings:** Train domain-specific embedding model
6. **Streaming Responses:** Implement streaming Gemini responses
7. **Document Versioning:** Track document updates and re-index automatically

---

## 11. Conclusion

The RAG Assistant successfully demonstrates the integration of retrieval-augmented generation for programming Q&A. The system effectively combines Pinecone vector search with Gemini LLM to provide accurate, source-backed answers. The web scraping feature enables automatic knowledge base expansion from official documentation. The application is deployed as a free cloud service on Hugging Face Spaces, making it accessible to all users.

---

## 12. References

1. Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS.
2. Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." EMNLP.
3. Pinecone Documentation. "Vector Database." https://docs.pinecone.io/
4. Google AI Studio. "Gemini API." https://aistudio.google.com/
5. Hugging Face. "sentence-transformers." https://www.sbert.net/
6. Gradio Documentation. "Quickstart." https://www.gradio.app/docs/

---

## 13. Appendices

### Appendix A: Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with API keys

# Run application
python app.py
```

### Appendix B: API Reference

| Endpoint | Method | Body | Response |
|----------|--------|------|----------|
| `/ask` | POST | `{"query": "string"}` | `{"answer": "string", "sources": [...]}` |
| `/upload` | POST | `file: binary` | `{"message": "string", "chunks": int, "chars": int}` |
| `/scrape` | POST | `{"url": "string", "name": "string"}` | `{"status": "string", "chunks": int}` |
| `/stats` | GET | — | `{"total_chunks": int}` |

### Appendix C: Configuration Parameters

| Parameter | Value | File |
|-----------|-------|------|
| CHUNK_SIZE | 500 | config.py |
| CHUNK_OVERLAP | 100 | config.py |
| TOP_K | 3 | config.py |
| EMBEDDING_MODEL | all-MiniLM-L6-v2 | config.py |
| GEMINI_MODEL | gemini-3.5-flash-lite | rag/generator.py |
| TEMPERATURE | 0.3 | rag/generator.py |
| MAX_OUTPUT_TOKENS | 1024 | rag/generator.py |

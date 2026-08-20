---
title: RAG Assistant
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
---

# RAG Assistant

Hybrid RAG system for programming questions (Python, Java, C) with document upload support.

## Setup

Add **Secrets** in Space Settings:
- `GEMINI_API_KEY` — get at [Google AI Studio](https://aistudio.google.com/apikey)
- `PINECONE_API_KEY` — get at [pinecone.io](https://www.pinecone.io/) (free tier)

## Features

- **Chat** — Ask programming questions, get answers with source citations
- **Upload** — Drag-drop PDF, DOCX, CSV, XLSX, TXT, MD files
- **Scrape** — Scrape Python/Java/C docs or add custom URLs

## Tech Stack

| Layer | Tool |
|---|---|
| Backend | FastAPI + Uvicorn |
| Vector DB | Pinecone (serverless) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Google Gemini (gemini-3.5-flash-lite) |
| Frontend | Gradio |

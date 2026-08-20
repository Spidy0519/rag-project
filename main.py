import os
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from config import UPLOAD_DIR
from ingestion.document_parser import parse_file
from ingestion.chunker import chunk_text
from rag.embeddings import embed_texts, get_model
from rag.vectorstore import add_documents, get_stats
from rag.generator import generate_answer
from scraper.scrape_docs import scrape_all, scrape_single


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    get_model()
    yield


app = FastAPI(title="RAG Assistant", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class AskRequest(BaseModel):
    query: str


@app.post("/ask")
async def ask(req: AskRequest):
    if not req.query.strip():
        return JSONResponse({"error": "No query provided"}, status_code=400)
    return generate_answer(req.query.strip())


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = file.filename or "unknown"
    filepath = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{filename}")
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    try:
        text = parse_file(filepath)
        if not text.strip():
            return JSONResponse({"error": "Could not extract text from file"}, status_code=400)
        chunks = chunk_text(text, source=filename, extra_meta={"filename": filename})
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [c["id"] for c in chunks]
        embeddings = embed_texts(texts)
        add_documents(texts, embeddings, metadatas, ids)
        return {
            "message": f"Uploaded and indexed '{filename}'",
            "chunks": len(chunks),
            "chars": len(text),
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


class ScrapeRequest(BaseModel):
    url: str | None = None
    name: str = "custom"


@app.post("/scrape")
async def scrape(req: ScrapeRequest):
    if req.url:
        return scrape_single(req.url, req.name)
    results = scrape_all()
    return {"message": "Scraping complete", "results": results}


@app.get("/stats")
async def stats():
    return get_stats()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

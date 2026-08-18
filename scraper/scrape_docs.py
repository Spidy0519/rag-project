import requests
from bs4 import BeautifulSoup
from ingestion.chunker import chunk_documents
from rag.embeddings import embed_texts
from rag.vectorstore import add_documents

SCRAPE_SOURCES = {
    "python_basics": "https://docs.python.org/3/tutorial/introduction.html",
    "python_data": "https://docs.python.org/3/tutorial/datastructures.html",
    "python_classes": "https://docs.python.org/3/tutorial/classes.html",
    "python_errors": "https://docs.python.org/3/tutorial/errors.html",
    "java_tutorial": "https://dev.java/tutorial/",
    "java_basics": "https://dev.java/tutorial/basics/",
    "c_basics": "https://www.learn-c.org/",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def scrape_url(url: str, name: str) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        main = soup.find("main") or soup.find("article") or soup.find("body")
        if main is None:
            main = soup
        text = main.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
    except Exception as e:
        return f"[Scrape error for {name}: {e}]"

def scrape_all() -> dict:
    docs = []
    results = {}
    for name, url in SCRAPE_SOURCES.items():
        text = scrape_url(url, name)
        if text and not text.startswith("[Scrape error"):
            docs.append({"text": text, "source": url, "metadata": {"name": name}})
            results[name] = {"url": url, "chars": len(text), "status": "ok"}
        else:
            results[name] = {"url": url, "chars": 0, "status": "failed"}
    if docs:
        chunks = chunk_documents(docs)
        if chunks:
            texts = [c["text"] for c in chunks]
            metadatas = [c["metadata"] for c in chunks]
            ids = [c["id"] for c in chunks]
            embeddings = embed_texts(texts)
            add_documents(texts, embeddings, metadatas, ids)
    return results

def scrape_single(url: str, name: str = "custom") -> dict:
    text = scrape_url(url, name)
    if text and not text.startswith("[Scrape error"):
        docs = [{"text": text, "source": url, "metadata": {"name": name}}]
        chunks = chunk_documents(docs)
        if chunks:
            texts = [c["text"] for c in chunks]
            metadatas = [c["metadata"] for c in chunks]
            ids = [c["id"] for c in chunks]
            embeddings = embed_texts(texts)
            add_documents(texts, embeddings, metadatas, ids)
        return {"url": url, "chars": len(text), "chunks": len(chunks), "status": "ok"}
    return {"url": url, "chars": 0, "chunks": 0, "status": "failed"}

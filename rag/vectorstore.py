import os
import chromadb

_client = None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is None:
        mode = os.getenv("CHROMA_MODE", "memory")
        if mode == "persist":
            from config import CHROMA_DIR
            os.makedirs(CHROMA_DIR, exist_ok=True)
            _client = chromadb.PersistentClient(path=CHROMA_DIR)
        else:
            _client = chromadb.Client()
        _collection = _client.get_or_create_collection(
            name="rag_docs",
            metadata={"hnsw:space": "cosine"}
        )
    return _collection

def add_documents(documents: list[str], embeddings: list[list[float]], metadatas: list[dict], ids: list[str]):
    col = get_collection()
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        end = min(i + batch_size, len(documents))
        col.add(
            documents=documents[i:end],
            embeddings=embeddings[i:end],
            metadatas=metadatas[i:end],
            ids=ids[i:end],
        )

def query_similar(query_embedding: list[float], top_k: int = 5) -> dict:
    col = get_collection()
    results = col.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    return results

def get_stats() -> dict:
    col = get_collection()
    return {"total_chunks": col.count()}

from config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str, source: str = "", extra_meta: dict = None) -> list[dict]:
    if not text or not text.strip():
        return []
    chunks = []
    start = 0
    idx = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text_str = text[start:end]
        if chunk_text_str.strip():
            meta = {"source": source}
            if extra_meta:
                meta.update(extra_meta)
            chunks.append({
                "text": chunk_text_str.strip(),
                "metadata": meta,
                "id": f"{source}_{idx}" if source else f"chunk_{idx}",
            })
            idx += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def chunk_documents(documents: list[dict]) -> list[dict]:
    all_chunks = []
    for doc in documents:
        text = doc.get("text", "")
        source = doc.get("source", "unknown")
        extra_meta = doc.get("metadata", {})
        chunks = chunk_text(text, source=source, extra_meta=extra_meta)
        all_chunks.extend(chunks)
    return all_chunks

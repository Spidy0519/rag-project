import os
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME

_pc = None
_index = None


def get_index():
    global _pc, _index
    if _index is None:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
        existing = [idx.name for idx in _pc.indexes.list()]
        if PINECONE_INDEX_NAME not in existing:
            _pc.indexes.create(
                name=PINECONE_INDEX_NAME,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        _index = _pc.index(PINECONE_INDEX_NAME)
    return _index


def add_documents(documents, embeddings, metadatas, ids):
    index = get_index()
    vectors = []
    for id_val, emb, doc, meta in zip(ids, embeddings, documents, metadatas):
        safe_meta = {k: v for k, v in meta.items() if isinstance(v, (str, int, float, bool))}
        safe_meta["text"] = doc[:1000]
        vectors.append({
            "id": id_val,
            "values": emb,
            "metadata": safe_meta,
        })
    index.upsert(vectors=vectors)


def query_similar(query_embedding, top_k=3):
    index = get_index()
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )
    docs = []
    metas = []
    dists = []
    for match in results.matches:
        meta = dict(match.metadata) if match.metadata else {}
        text = meta.pop("text", "")
        docs.append(text)
        metas.append(meta)
        dists.append(match.score)
    return {
        "documents": [docs],
        "metadatas": [metas],
        "distances": [dists],
    }


def get_stats():
    index = get_index()
    stats = index.describe_index_stats()
    return {"total_chunks": stats.total_vector_count}

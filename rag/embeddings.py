from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return model.encode(texts, show_progress_bar=False, batch_size=32).tolist()

def embed_query(query: str) -> list[float]:
    model = get_model()
    return model.encode([query], show_progress_bar=False)[0].tolist()

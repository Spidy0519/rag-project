import torch
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

_model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")


def get_model():
    return _model


def embed_texts(texts):
    return _model.encode(texts, show_progress_bar=False, batch_size=32, device="cpu").tolist()


def embed_query(query):
    return _model.encode([query], show_progress_bar=False, device="cpu")[0].tolist()

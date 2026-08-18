import time
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from config import GEMINI_API_KEY, TOP_K
from rag.embeddings import embed_query
from rag.vectorstore import query_similar

_client = None
MODEL = "gemini-3.5-flash-lite"

def get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client

def generate_answer(query: str) -> dict:
    try:
        q_emb = embed_query(query)
        results = query_similar(q_emb, top_k=TOP_K)
    except Exception as e:
        return {"answer": f"Search error: {str(e)}", "sources": []}

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    context_parts = []
    sources = []
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        context_parts.append(doc)
        sources.append({
            "source": meta.get("source", "unknown"),
            "distance": round(dist, 4),
            "snippet": doc[:150],
        })

    if not context_parts:
        return {"answer": "No relevant documents found. Upload documents or scrape sources first.", "sources": []}

    context = "\n---\n".join(context_parts)

    prompt = (
        "Answer using ONLY the context below. Be concise.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {query}\n\n"
        "ANSWER:"
    )

    for attempt in range(3):
        try:
            client = get_client()
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=1024,
                ),
            )
            return {"answer": response.text, "sources": sources}
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                return {"answer": "Rate limit hit. Wait a minute and try again.", "sources": sources}
            return {"answer": f"API error: {str(e)}", "sources": sources}
        except Exception as e:
            return {"answer": f"Error: {str(e)}", "sources": sources}

    return {"answer": "Failed after retries.", "sources": sources}

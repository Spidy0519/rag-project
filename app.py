import os
import uuid
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from config import UPLOAD_DIR
from ingestion.document_parser import parse_file
from ingestion.chunker import chunk_text
from rag.embeddings import embed_texts
from rag.vectorstore import add_documents, get_stats
from rag.generator import generate_answer
from scraper.scrape_docs import scrape_all, scrape_single

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

os.makedirs(UPLOAD_DIR, exist_ok=True)

print("Loading embedding model...")
from rag.embeddings import get_model
get_model()
print("Model ready.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{filename}")
    file.save(filepath)
    try:
        text = parse_file(filepath)
        if not text.strip():
            return jsonify({"error": "Could not extract text from file"}), 400
        chunks = chunk_text(text, source=filename, extra_meta={"filename": filename})
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [c["id"] for c in chunks]
        embeddings = embed_texts(texts)
        add_documents(texts, embeddings, metadatas, ids)
        return jsonify({
            "message": f"Uploaded and indexed '{filename}'",
            "chunks": len(chunks),
            "chars": len(text),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json() or {}
    url = data.get("url")
    name = data.get("name", "custom")
    if url:
        result = scrape_single(url, name)
        return jsonify(result)
    results = scrape_all()
    return jsonify({"message": "Scraping complete", "results": results})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400
    result = generate_answer(query)
    return jsonify(result)

@app.route("/stats")
def stats():
    return jsonify(get_stats())

@app.route("/history")
def history():
    return jsonify({"history": []})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

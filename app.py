import spaces
import os
import uuid
import gradio as gr
from ingestion.document_parser import parse_file
from ingestion.chunker import chunk_text
from rag.embeddings import embed_texts, get_model
from rag.vectorstore import add_documents, get_stats
from rag.generator import generate_answer
from scraper.scrape_docs import scrape_all, scrape_single

get_model()


@spaces.GPU(duration=120)
def _gpu_init():
    pass


_gpu_init()


def chat(message, history):
    result = generate_answer(message.strip())
    answer = result.get("answer", "Error generating answer.")
    sources = result.get("sources", [])
    if sources:
        refs = "\n\n**Sources:** " + ", ".join(
            s["source"] for s in sources if s.get("source") and s["source"] != "unknown"
        )
        return answer + refs
    return answer


def upload_file(file):
    if file is None:
        return "No file selected."
    filename = os.path.basename(file.name)
    try:
        text = parse_file(file.name)
        if not text.strip():
            return f"Could not extract text from '{filename}'."
        chunks = chunk_text(text, source=filename, extra_meta={"filename": filename})
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [c["id"] for c in chunks]
        embeddings = embed_texts(texts)
        add_documents(texts, embeddings, metadatas, ids)
        return f"Indexed '{filename}' — {len(chunks)} chunks, {len(text)} chars."
    except Exception as e:
        return f"Error: {e}"


def scrape_all_sources():
    results = scrape_all()
    lines = []
    for name, info in results.items():
        status = "ok" if info["status"] == "ok" else "failed"
        lines.append(f"- {name}: {status} ({info.get('chars', 0)} chars)")
    return "\n".join(lines) if lines else "No sources scraped."


def scrape_url(url, name):
    if not url or not url.strip():
        return "Enter a URL."
    result = scrape_single(url.strip(), name.strip() if name else "custom")
    if result["status"] == "ok":
        return f"Scraped {result['chunks']} chunks from {url}"
    return f"Failed to scrape {url}"


with gr.Blocks(title="RAG Assistant") as demo:
    gr.Markdown("# RAG Assistant")
    gr.Markdown("Ask programming questions (Python, Java, C) or upload your own documents.")

    with gr.Tabs():
        with gr.Tab("Chat"):
            gr.ChatInterface(
                chat,
                examples=[
                    "What are Python data structures?",
                    "Explain Java exception handling",
                    "How does pointer work in C?",
                ],
            )

        with gr.Tab("Upload"):
            file_input = gr.File(label="Upload Document", file_types=[".pdf", ".docx", ".csv", ".xlsx", ".txt", ".md"])
            upload_output = gr.Textbox(label="Status")
            file_input.upload(upload_file, inputs=file_input, outputs=upload_output)

        with gr.Tab("Scrape"):
            gr.Markdown("### Scrape Default Sources")
            scrape_btn = gr.Button("Scrape Default Sources")
            scrape_all_output = gr.Textbox(label="Status")
            scrape_btn.click(scrape_all_sources, outputs=scrape_all_output)

            gr.Markdown("### Scrape Custom URL")
            with gr.Row():
                url_input = gr.Textbox(label="URL", placeholder="https://...")
                name_input = gr.Textbox(label="Label", placeholder="optional")
            scrape_url_btn = gr.Button("Scrape URL")
            scrape_url_output = gr.Textbox(label="Status")
            scrape_url_btn.click(scrape_url, inputs=[url_input, name_input], outputs=scrape_url_output)

demo.launch(server_name="0.0.0.0", server_port=7860)

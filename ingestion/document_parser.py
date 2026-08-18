import os
import pandas as pd
from pypdf import PdfReader
from docx import Document as DocxDocument

def parse_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return _parse_pdf(filepath)
    elif ext == ".docx":
        return _parse_docx(filepath)
    elif ext in (".csv", ".xlsx"):
        return _parse_spreadsheet(filepath)
    else:
        return _parse_text(filepath)

def _parse_pdf(filepath: str) -> str:
    reader = PdfReader(filepath)
    text_parts = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            text_parts.append(f"[Page {i+1}] {text}")
    return "\n\n".join(text_parts)

def _parse_docx(filepath: str) -> str:
    doc = DocxDocument(filepath)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)

def _parse_spreadsheet(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    return df.to_string(index=False)

def _parse_text(filepath: str) -> str:
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return ""

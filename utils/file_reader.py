import fitz  # PyMuPDF
from docx import Document
import io

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8")
    except:
        return file_bytes.decode("latin-1")

def extract_text(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif filename.lower().endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    else:
        return ""

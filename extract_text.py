import fitz  # PyMuPDF
import os
import docx

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extract text from DOCX using python-docx"""
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def extract_resume_text(file_path):
    """Main function to handle both PDF and DOCX"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type: Only PDF and DOCX supported")

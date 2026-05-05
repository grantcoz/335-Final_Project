"""
file_parser.py
--------------
Helper module for the TitanCampus Algorithmic Assistant (TCAA).

Provides functions to extract raw text from .txt, .pdf, and .docx files
so that the Notes Search Engine module can run pattern-matching algorithms
against a uniform, lowercase string.

External dependencies (per project spec):
    - PyPDF2          (PDF parsing)
    - python-docx     (DOCX parsing)
"""

import os


def parse_txt(file_path: str) -> str:
    """Read a plain-text file and return its contents."""
    # utf-8 with errors="ignore" tolerates stray bytes from Windows note files
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def parse_pdf(file_path: str) -> str:
    """Extract text from every page of a PDF using PyPDF2."""
    try:
        from PyPDF2 import PdfReader
    except ImportError as e:
        raise ImportError(
            "PyPDF2 is required to read PDF files. "
            "Install it with:  pip install PyPDF2"
        ) from e

    reader = PdfReader(file_path)
    pages = []
    for page in reader.pages:
        # extract_text() can return None on image-only pages
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)


def parse_docx(file_path: str) -> str:
    """Extract text from every paragraph of a DOCX using python-docx."""
    try:
        import docx  # python-docx exposes itself as the `docx` module
    except ImportError as e:
        raise ImportError(
            "python-docx is required to read DOCX files. "
            "Install it with:  pip install python-docx"
        ) from e

    document = docx.Document(file_path)
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def extract_text(file_path: str) -> str:
    """
    Dispatcher: choose the right parser based on the file extension and
    return the document's text in lowercase so that downstream string
    matching is case-insensitive (per project spec).
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        raw = parse_txt(file_path)
    elif ext == ".pdf":
        raw = parse_pdf(file_path)
    elif ext == ".docx":
        raw = parse_docx(file_path)
    else:
        raise ValueError(
            f"Unsupported file type '{ext}'. Use .txt, .pdf, or .docx."
        )

    return raw.lower()

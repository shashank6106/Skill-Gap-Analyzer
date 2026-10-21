"""
Resume Parser Module.
Extracts text, metadata, and structural sections from PDF documents using PyPDF.
"""

import io
import re
from typing import Dict, Any, Union, BinaryIO
from pypdf import PdfReader


def extract_text_from_pdf(pdf_source: Union[str, bytes, BinaryIO]) -> str:
    """
    Extracts concatenated raw text from all pages of a PDF document.
    Accepts a filepath, bytes buffer, or file-like stream (such as Streamlit UploadedFile).
    """
    try:
        if isinstance(pdf_source, bytes):
            stream = io.BytesIO(pdf_source)
            reader = PdfReader(stream)
        elif hasattr(pdf_source, "read"):
            reader = PdfReader(pdf_source)
        else:
            reader = PdfReader(pdf_source)

        text_pages = []
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text_pages.append(page_text)

        full_text = "\n".join(text_pages)
        # Normalize excessive whitespace and consecutive blank lines
        cleaned_text = re.sub(r"[ \t]+", " ", full_text)
        cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text).strip()
        return cleaned_text
    except Exception as exc:
        raise ValueError(f"Failed to extract text from PDF: {str(exc)}") from exc


def extract_candidate_name(text: str) -> str:
    """
    Heuristically extracts the candidate's name from the top header lines of the resume.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not lines:
        return "Unknown Candidate"

    # Usually the first 1-3 non-empty lines contain the applicant's name
    for line in lines[:3]:
        # Filter out lines that look like emails, phone numbers, or section headers
        if re.search(r"@|\+|www|http|curriculum|resume|page", line, re.IGNORECASE):
            continue
        cleaned = re.sub(r"[^a-zA-Z\s\.]", "", line).strip()
        words = cleaned.split()
        if 1 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
            return cleaned

    return lines[0][:40]


def extract_contact_info(text: str) -> Dict[str, str]:
    """
    Extracts email, phone, and degree keywords using regex patterns.
    """
    # Email regex
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email_match.group(0) if email_match else ""

    # Phone regex (Indian/international common formats)
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}", text)
    phone = phone_match.group(0).strip() if phone_match else ""

    # Education degree detection
    degree = "Not specified"
    degrees_catalog = ["B.Tech", "B.E", "M.Tech", "MCA", "B.Sc", "M.Sc", "BCA", "Ph.D", "MBA"]
    for deg in degrees_catalog:
        if re.search(r"\b" + re.escape(deg) + r"\b", text, re.IGNORECASE):
            degree = deg
            break

    return {
        "email": email,
        "phone": phone,
        "degree": degree
    }


def parse_resume_content(pdf_source: Union[str, bytes, BinaryIO], filename: str = "uploaded_resume.pdf") -> Dict[str, Any]:
    """
    High-level resume parser orchestrator.
    Returns structured resume metadata.
    """
    raw_text = extract_text_from_pdf(pdf_source)
    name = extract_candidate_name(raw_text)
    contact = extract_contact_info(raw_text)

    return {
        "filename": filename,
        "parsed_name": name,
        "email": contact["email"],
        "phone": contact["phone"],
        "degree": contact["degree"],
        "raw_text": raw_text
    }

"""
PDF Resume Generator Utility.
Generates valid, professional sample PDF resumes for immediate testing and demonstration.
"""

import os
from typing import List


def generate_pdf_document(filepath: str, lines: List[str]) -> None:
    """
    Constructs a standard, valid PDF v1.4 file with Helvetica font.
    """
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

    # Build text stream
    stream_content = "BT /F1 11 Tf 50 750 Td 15 TL "
    for line in lines:
        if line.startswith("### "):
            # Heading simulation
            clean = line.replace("### ", "").strip()
            safe = clean.replace("(", "\\(").replace(")", "\\)")
            stream_content += f"T* ({safe}) ' T* "
        elif line.startswith("# "):
            clean = line.replace("# ", "").strip()
            safe = clean.replace("(", "\\(").replace(")", "\\)")
            stream_content += f"/F1 16 Tf ({safe}) ' /F1 11 Tf T* "
        else:
            safe = line.replace("(", "\\(").replace(")", "\\)")
            stream_content += f"({safe}) ' "
    stream_content += "ET"

    stream_bytes = stream_content.encode("latin1", errors="replace")

    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = (
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    )
    obj4 = (
        f"4 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n".encode("latin1")
        + stream_bytes
        + b"\nendstream\nendobj\n"
    )
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"

    header = b"%PDF-1.4\n"
    body = obj1 + obj2 + obj3 + obj4 + obj5
    xref_offset = len(header) + len(body)

    offsets = [
        0,
        len(header),
        len(header) + len(obj1),
        len(header) + len(obj1) + len(obj2),
        len(header) + len(obj1) + len(obj2) + len(obj3),
        len(header) + len(obj1) + len(obj2) + len(obj3) + len(obj4)
    ]

    xref = b"xref\n0 6\n0000000000 65535 f \n"
    for off in offsets[1:]:
        xref += f"{off:010d} 00000 n \n".encode("latin1")

    trailer = f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin1")

    with open(filepath, "wb") as f:
        f.write(header + body + xref + trailer)


def generate_all_sample_resumes(output_dir: str = "sample_resumes") -> List[str]:
    """Generates 3 ready-to-upload PDF resumes."""
    resumes = [
        (
            "shashank_resume.pdf",
            [
                "# Shashank",
                "Email: student@example.com | Phone: +91 98765 43210 | Location: Bengaluru",
                "",
                "### Education",
                "B.Tech in Computer Science and Engineering (CSE)",
                "National Institute of Technology - CGPA 8.6",
                "",
                "### Technical Skills",
                "Programming: Python, C++, SQL",
                "Databases: MongoDB, MySQL",
                "Libraries & Tools: Pandas, Git, Linux",
                "",
                "### Projects",
                "1. Air Quality Analysis: Cleaned and analyzed sensor datasets using Python and Pandas.",
                "2. Library Catalog API: Built a FastAPI backend with MongoDB document storage.",
                "",
                "### Experience",
                "Software Engineering Intern at CodeCraft Technologies (6 months)"
            ]
        ),
        (
            "ananya_resume.pdf",
            [
                "# Ananya Sharma",
                "Email: ananya.sharma@example.com | Phone: +91 98765 43211 | Location: Pune",
                "",
                "### Education",
                "B.Tech in Data Science & Artificial Intelligence",
                "Tech University - CGPA 9.1",
                "",
                "### Technical Skills",
                "Data Analysis: Python, SQL, Statistics, Excel",
                "BI & Visualization: Power BI, Tableau, Matplotlib",
                "Databases: PostgreSQL, MySQL",
                "",
                "### Projects",
                "1. Retail Sales Forecasting Dashboard: Built interactive Power BI reports and SQL queries.",
                "2. Customer Churn Statistical Study: Applied hypothesis testing and regression in Python.",
                "",
                "### Experience",
                "Data Analyst Intern at FinMetrics Corp (1 year)"
            ]
        ),
        (
            "rahul_resume.pdf",
            [
                "# Rahul Verma",
                "Email: rahul.v@example.com | Phone: +91 98765 43212 | Location: Hyderabad",
                "",
                "### Education",
                "B.E in Information Technology",
                "Apex Engineering Institute - CGPA 8.3",
                "",
                "### Technical Skills",
                "Languages: JavaScript, TypeScript, Python",
                "Web & Backend: React, Node.js, Express, HTML, CSS",
                "Databases: MongoDB, Redis",
                "DevOps: Git, Docker, Linux",
                "",
                "### Projects",
                "1. Campus Market MERN App: Built a full-stack e-commerce marketplace using React, Node.js, and MongoDB.",
                "2. Real-time Chat App: Integrated WebSockets with Express and Redis caching.",
                "",
                "### Experience",
                "Frontend Web Developer at StartupHub (1 year)"
            ]
        )
    ]

    generated_paths = []
    for fname, lines in resumes:
        dest = os.path.join(output_dir, fname)
        generate_pdf_document(dest, lines)
        generated_paths.append(dest)

    return generated_paths


if __name__ == "__main__":
    paths = generate_all_sample_resumes()
    print("Generated sample PDF resumes:")
    for p in paths:
        print(f" - {p}")

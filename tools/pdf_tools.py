from PyPDF2 import PdfMerger
import os
from docx import Document
import pikepdf

# 1️⃣ Merge PDFs
def merge_pdfs(file_paths, output_path="merged.pdf"):
    merger = PdfMerger()
    for pdf in file_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    return {"message": f"Merged {len(file_paths)} PDFs into {output_path}"}

# 2️⃣ Convert PDF to Word (basic text extraction)
def pdf_to_word(pdf_path, output_path=None):
    if output_path is None:
        output_path = pdf_path.replace(".pdf", ".docx")
    from pdfplumber import open as pdf_open
    doc = Document()
    with pdf_open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
    doc.save(output_path)
    return {"message": f"Converted {pdf_path} to {output_path}"}

# 3️⃣ Compress PDF
def compress_pdf(pdf_path, output_path=None):
    if output_path is None:
        output_path = pdf_path.replace(".pdf", "_compressed.pdf")
    pdf = pikepdf.open(pdf_path)
    pdf.save(output_path, optimize_streams=True)
    pdf.close()
    return {"message": f"Compressed {pdf_path} to {output_path}"}

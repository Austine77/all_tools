import pdfplumber

KEYWORDS = ["experience", "education", "skills", "projects"]

def analyze_resume(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    word_count = len(text.split())
    found_keywords = [k for k in KEYWORDS if k in text.lower()]

    return {
        "word_count": word_count,
        "keywords_found": found_keywords,
        "score": min(100, word_count // 10 + len(found_keywords) * 10)
    }

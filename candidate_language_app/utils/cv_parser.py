import io
from pypdf import PdfReader
from docx import Document

def parse_cv(cv_file):
    """
    Parses a CV file (PDF or DOCX) and returns the extracted text.
    """
    text = ""
    try:
        if cv_file.name.endswith('.pdf'):
            reader = PdfReader(cv_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif cv_file.name.endswith('.docx'):
            doc = Document(cv_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error parsing CV: {e}")
        return ""

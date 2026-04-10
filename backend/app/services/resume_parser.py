from docx import Document
from pypdf import PdfReader


class ResumeParser:

    def extract_text_from_pdf(self, file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            pages_text = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    pages_text.append(page_text.strip())
            return "\n".join(pages_text)
        except Exception as e:
            print("PDF ERROR:", e)
            return ""

    def extract_text_from_docx(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = []
            for p in doc.paragraphs:
                if p.text.strip():
                    text.append(p.text.strip())
            return "\n".join(text)
        except Exception as e:
            print("DOCX ERROR:", e)
            return ""

    def parse_resume_text(self, text: str):
        return {
            "skills": [],
            "education": [],
            "experiences": []
        }


resume_parser = ResumeParser()




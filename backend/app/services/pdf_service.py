from PyPDF2 import PdfReader
from typing import List
import os

class PDFService:
    def __init__(self):
        pass

    def extract_text(self, pdf_path: str) -> List[dict]:
        """
        Extracts text from PDF with page numbers
        """
        documents = []
        reader = PdfReader(pdf_path)
        
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                documents.append({
                    "content": text,
                    "page_number": page_num,
                    "source": os.path.basename(pdf_path)
                })
                
        return documents 
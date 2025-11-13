from pypdf import PdfReader
from io import BytesIO

class PDFDocument():

    def __init__(self,
                 pdf_file):
        """
        PDF Document from which to extract text and generate chunks.

        @param pdf_file: PDF file bytes        
        """
        # Opening pdf file from bytes
        self.pdf_file = PdfReader(BytesIO(pdf_file))
    
    def extract_text(self):
        """
        Extracts the text content from the opened pdf file        
        """
        # Extract text from all pages
        text_content = []
        for page in self.pdf_file.pages:
            text_content.append(page.extract_text())
        return "\n\n".join(text_content)

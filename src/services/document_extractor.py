from datetime import datetime
from src.models.extracted_document import ExtractedDoc
from src.utils.clean_text import clean_text
from werkzeug.datastructures import FileStorage
from pytesseract import pytesseract
from PIL import Image
import pdfplumber
import logging
from pdfminer.pdfparser import PDFSyntaxError

class Extractor:
    """extract text from documents"""

    def extract_text_pdf(self, file: FileStorage) -> str:
        logging.info(f"Processing PDF: {file.filename}")
        try:
            text = ""
            with pdfplumber.open(file.stream) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        #filtering out short words
                        words = page_text.split()
                        filtered_words = [word for word in words if len(word) > 2]
                        text += " ".join(filtered_words) + "\n"

            return text.strip()
        except PDFSyntaxError as e:
            logging.error(f"Invalid PDF structure: {str(e)}")
            return ""    
        except Exception as e:
            logging.error(f"PDF extraction failed: {str(e)}")
            raise

    def extract_text_image(self, file: FileStorage) -> str:
        logging.info(f"Processing image: {file.filename}")
        try:
            text = ""
            image = Image.open(file.stream)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logging.error(f"Image extraction failed: {str(e)}")
            raise

    def process_document(self, file: FileStorage) -> ExtractedDoc:
        logging.info(f"Starting document processing: {file.filename}")
        raw_text = ""
        try:
            if file.filename.lower().endswith(".pdf"):
                raw_text = self.extract_text_pdf(file)
            else:
                raw_text = self.extract_text_image(file)

            processed_text = clean_text(raw_text)
            return ExtractedDoc(file.filename, processed_text, datetime.now())
        except ValueError as e:
            logging.error(f"Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            return ExtractedDoc(file.filename, "", datetime.now())

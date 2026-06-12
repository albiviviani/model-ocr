"""OCR extraction helpers for local image and PDF text extraction."""

from io import BytesIO
from pathlib import Path

import pytesseract
from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFInfoNotInstalledError
from PIL import Image

from app.services.settings import Settings


class OCRProcessor:
    """Extract text from uploaded image or PDF content."""

    SUPPORTED_IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}
    SUPPORTED_DOCUMENT_TYPES = {".pdf"}

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        if self.settings.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = self.settings.tesseract_cmd

    def extract_text(self, filename: str, content: bytes) -> str:
        """Detect the file type and extract text from the uploaded content."""
        extension = Path(filename).suffix.lower()

        if extension in self.SUPPORTED_IMAGE_TYPES:
            return self._extract_text_from_image(content)

        if extension in self.SUPPORTED_DOCUMENT_TYPES:
            return self._extract_text_from_pdf(content)

        raise ValueError(
            "Unsupported file type. Upload an image or PDF file for OCR processing."
        )

    def _extract_text_from_image(self, image_bytes: bytes) -> str:
        """Perform OCR on image bytes and return extracted text."""
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        text = pytesseract.image_to_string(image, lang=self.settings.ocr_language)
        return text.strip()

    def _extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Convert PDF pages to images and OCR each page."""
        try:
            pages = convert_from_bytes(file_bytes, dpi=self.settings.pdf_dpi)
        except PDFInfoNotInstalledError as error:
            raise ValueError(
                "Poppler not installed or `pdfinfo` not found in PATH. "
                "Install Poppler (macOS: `brew install poppler`) and ensure `pdfinfo` is available."
            ) from error

        if not pages:
            raise ValueError("No pages extracted from PDF file.")

        extracted_pages = []
        for page_number, page in enumerate(pages, start=1):
            page_text = pytesseract.image_to_string(page, lang=self.settings.ocr_language)
            extracted_pages.append(f"--- Page {page_number} ---\n{page_text.strip()}")

        return "\n\n".join(extracted_pages).strip()

"""PDF manipulation service for adding OCR text layers."""

import io

from xberg import extract, ExtractInput, ExtractionConfig, OcrConfig, LlmConfig
from pypdf import PdfReader, PdfWriter

from ..config import settings


class PDFService:
    """Service for PDF manipulation and OCR layer embedding."""

    def __init__(self):
        """Initialize the PDF service."""
        self.config = ExtractionConfig(
            ocr=OcrConfig(
                backend="vlm",
                vlm_config=LlmConfig(
                    model=settings.vlm_model,
                    base_url=settings.ollama_base_url,
                    api_key=settings.ollama_api_key,
                ),
            ),
            force_ocr=True,
        )

    async def add_ocr_layer(self, pdf_bytes: bytes) -> bytes:
        """
        Add an OCR text layer to a PDF document.

        This extracts text using xberg and returns a searchable PDF.
        Currently returns the original PDF with extracted text available
        via the text format endpoint.

        Args:
            pdf_bytes: Raw PDF file bytes

        Returns:
            PDF bytes with embedded OCR text layer

        Raises:
            RuntimeError: If OCR or PDF manipulation fails
        """
        try:
            # Extract text using xberg
            result = await extract(
                ExtractInput(kind="bytes", bytes=pdf_bytes, mime_type="application/pdf"),
                self.config,
            )

            if not result.results:
                raise RuntimeError("No extraction results returned")

            doc = result.results[0]
            extracted_text = doc.content

            # For now, we'll add the extracted text as metadata to the PDF
            # A full implementation would overlay invisible text at correct positions
            pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
            pdf_writer = PdfWriter()

            # Copy all pages
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Add OCR text as metadata
            pdf_writer.add_metadata({
                "/OCRText": extracted_text,
                "/OCRProcessor": "xberg-vlm",
            })

            # Write to bytes
            output_buffer = io.BytesIO()
            pdf_writer.write(output_buffer)
            output_buffer.seek(0)

            return output_buffer.read()

        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"PDF OCR layer addition failed: {str(e)}")

"""OCR service using xberg with Ollama VLM backend."""

import time
from typing import Dict, Any

from xberg import extract, ExtractInput, ExtractionConfig, OcrConfig, VlmConfig

from ..config import settings


class OCRService:
    """Service for performing OCR on PDF documents using xberg."""

    def __init__(self):
        """Initialize the OCR service."""
        self.config = ExtractionConfig(
            ocr=OcrConfig(
                backend="vlm",
                vlm_config=VlmConfig(
                    model=settings.vlm_model,
                    base_url=settings.ollama_base_url,
                ),
            ),
            force_ocr=True,
        )

    async def extract_text(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Extract text from a PDF using xberg with Ollama VLM backend.

        Args:
            pdf_bytes: Raw PDF file bytes

        Returns:
            Dictionary with extracted text, page count, and processing time

        Raises:
            RuntimeError: If OCR processing fails
        """
        start_time = time.time()

        try:
            # Use xberg SDK to extract from bytes
            result = await extract(
                ExtractInput(kind="bytes", bytes=pdf_bytes, mime_type="application/pdf"),
                self.config,
            )

            if not result.results:
                raise RuntimeError("No extraction results returned")

            doc = result.results[0]
            extracted_text = doc.content

            # Get page count from metadata or pages array
            page_count = len(doc.pages) if doc.pages else 0

            processing_time_ms = int((time.time() - start_time) * 1000)

            return {
                "success": True,
                "text": extracted_text,
                "pages": page_count,
                "processing_time_ms": processing_time_ms,
            }

        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {str(e)}")

"""API routes for the OCR server."""

from enum import Enum
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile, Query
from fastapi.responses import Response

from ..services import OCRService, PDFService


class OutputFormat(str, Enum):
    """Supported output formats for OCR."""

    TEXT = "text"
    PDF = "pdf"


router = APIRouter()
ocr_service = OCRService()
pdf_service = PDFService()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "xberg-ocr"}


@router.post("/ocr")
async def process_ocr(
    file: UploadFile = File(...),
    format: OutputFormat = Query(OutputFormat.TEXT, description="Output format: text or pdf"),
):
    """
    Process a PDF file with OCR.

    Args:
        file: PDF file to process
        format: Output format (text or pdf)

    Returns:
        JSON with extracted text (format=text) or PDF file (format=pdf)
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        pdf_bytes = await file.read()

        if format == OutputFormat.TEXT:
            result = await ocr_service.extract_text(pdf_bytes)
            return result

        elif format == OutputFormat.PDF:
            output_pdf = await pdf_service.add_ocr_layer(pdf_bytes)
            return Response(
                content=output_pdf,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'attachment; filename="ocr_{file.filename}"'
                },
            )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error during OCR processing: {str(e)}"
        )

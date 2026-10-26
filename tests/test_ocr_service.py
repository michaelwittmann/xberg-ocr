"""Tests for OCR service."""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from src.xberg_ocr.services.ocr_service import OCRService


@pytest.fixture
def ocr_service():
    """Fixture for OCR service instance."""
    return OCRService()


@pytest.fixture
def sample_pdf_bytes():
    """Fixture for sample PDF bytes."""
    return b"%PDF-1.4\n%mock pdf content"


@pytest.fixture
def mock_extraction_result():
    """Fixture for mock xberg extraction result."""
    mock_doc = Mock()
    mock_doc.content = "Extracted text from PDF"
    mock_doc.pages = [Mock(), Mock(), Mock()]

    mock_result = Mock()
    mock_result.results = [mock_doc]

    return mock_result


@pytest.mark.asyncio
async def test_extract_text_success(ocr_service, sample_pdf_bytes, mock_extraction_result):
    """Test successful text extraction using xberg SDK."""
    with patch("src.xberg_ocr.services.ocr_service.extract", new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = mock_extraction_result

        result = await ocr_service.extract_text(sample_pdf_bytes)

        assert result["success"] is True
        assert result["text"] == "Extracted text from PDF"
        assert result["pages"] == 3
        assert "processing_time_ms" in result
        assert isinstance(result["processing_time_ms"], int)

        # Verify extract was called with correct parameters
        mock_extract.assert_called_once()
        call_args = mock_extract.call_args
        extract_input = call_args[0][0]
        assert extract_input.kind == "bytes"
        assert extract_input.bytes == sample_pdf_bytes
        assert extract_input.mime_type == "application/pdf"


@pytest.mark.asyncio
async def test_extract_text_no_results(ocr_service, sample_pdf_bytes):
    """Test extraction when no results are returned."""
    mock_result = Mock()
    mock_result.results = []

    with patch("src.xberg_ocr.services.ocr_service.extract", new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = mock_result

        with pytest.raises(RuntimeError, match="No extraction results returned"):
            await ocr_service.extract_text(sample_pdf_bytes)


@pytest.mark.asyncio
async def test_extract_text_exception_handling(ocr_service, sample_pdf_bytes):
    """Test extraction failure handling."""
    with patch("src.xberg_ocr.services.ocr_service.extract", new_callable=AsyncMock) as mock_extract:
        mock_extract.side_effect = Exception("Extraction failed")

        with pytest.raises(RuntimeError, match="OCR processing failed: Extraction failed"):
            await ocr_service.extract_text(sample_pdf_bytes)

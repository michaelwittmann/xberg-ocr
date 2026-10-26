"""Tests for API endpoints."""

import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock
from pypdf import PdfWriter

from src.xberg_ocr.main import app


@pytest.fixture
def client():
    """Fixture for test client."""
    return TestClient(app)


def _make_minimal_pdf() -> bytes:
    w = PdfWriter()
    w.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    w.write(buf)
    return buf.getvalue()


@pytest.fixture
def sample_pdf_file():
    """Fixture for sample PDF file upload."""
    return ("test.pdf", _make_minimal_pdf(), "application/pdf")


def test_root_endpoint(client):
    """Test root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "xberg-ocr"
    assert "version" in data
    assert "docs" in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "xberg-ocr"


def test_ocr_text_format_success(client, sample_pdf_file):
    """Test OCR with text format output."""
    mock_result = {
        "success": True,
        "text": "Sample extracted text",
        "pages": 1,
        "processing_time_ms": 100,
    }

    with patch(
        "src.xberg_ocr.services.ocr_service.extract",
        new_callable=AsyncMock,
    ) as mock_extract:
        mock_doc = Mock()
        mock_doc.content = "Sample extracted text"
        mock_doc.pages = [Mock()]

        mock_extraction_result = Mock()
        mock_extraction_result.results = [mock_doc]
        mock_extract.return_value = mock_extraction_result

        response = client.post(
            "/ocr?format=text",
            files={"file": sample_pdf_file},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["text"] == "Sample extracted text"
        assert data["pages"] == 1


def test_ocr_pdf_format_success(client, sample_pdf_file):
    """Test OCR with PDF format output."""
    mock_pdf_output = b"%PDF-1.4\n%output with ocr"

    with patch(
        "src.xberg_ocr.services.pdf_service.extract",
        new_callable=AsyncMock,
    ) as mock_extract:
        mock_doc = Mock()
        mock_doc.content = "Extracted text"
        mock_doc.pages = [Mock()]

        mock_extraction_result = Mock()
        mock_extraction_result.results = [mock_doc]
        mock_extract.return_value = mock_extraction_result

        response = client.post(
            "/ocr?format=pdf",
            files={"file": sample_pdf_file},
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert b"PDF" in response.content


def test_ocr_invalid_file_type(client):
    """Test OCR with non-PDF file."""
    response = client.post(
        "/ocr",
        files={"file": ("test.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 400
    assert "Only PDF files are supported" in response.json()["detail"]


def test_ocr_processing_error(client, sample_pdf_file):
    """Test OCR processing error handling."""
    with patch(
        "src.xberg_ocr.services.ocr_service.extract",
        new_callable=AsyncMock,
        side_effect=RuntimeError("OCR failed"),
    ):
        response = client.post(
            "/ocr?format=text",
            files={"file": sample_pdf_file},
        )

        assert response.status_code == 500
        assert "OCR failed" in response.json()["detail"]


def test_ocr_default_format(client, sample_pdf_file):
    """Test OCR with default format (text)."""
    with patch(
        "src.xberg_ocr.services.ocr_service.extract",
        new_callable=AsyncMock,
    ) as mock_extract:
        mock_doc = Mock()
        mock_doc.content = "Default format text"
        mock_doc.pages = [Mock()]

        mock_extraction_result = Mock()
        mock_extraction_result.results = [mock_doc]
        mock_extract.return_value = mock_extraction_result

        response = client.post(
            "/ocr",  # No format parameter
            files={"file": sample_pdf_file},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

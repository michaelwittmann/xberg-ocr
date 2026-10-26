# Xberg OCR Server

A lightweight REST API server for processing PDFs with OCR using xberg's VLMOCR capabilities and Ollama.

## Features

- FastAPI-based REST API
- OCR processing via xberg with Ollama VLM backend (glm-ocr)
- Dual output formats:
  - Extracted text as JSON
  - PDF with embedded OCR text layer
- Configurable via environment variables
- Proper Python project structure with tests

## Prerequisites

- Python 3.10+
- Poetry for dependency management
- Ollama server with glm-ocr model running (local or remote)

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd xberg-ocr
```

2. Install dependencies:
```bash
poetry install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Ollama server URL
```

## Configuration

Create a `.env` file with the following variables:

```env
OLLAMA_BASE_URL=http://localhost:11434
VLM_MODEL=glm-ocr
HOST=0.0.0.0
PORT=8000
```

## Usage

### Start the server

```bash
poetry run uvicorn src.xberg_ocr.main:app --reload
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### OCR - Extract Text (JSON)
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/ocr?format=text
```

Response:
```json
{
  "success": true,
  "text": "Extracted text content...",
  "pages": 5,
  "processing_time_ms": 1234
}
```

#### OCR - Get Searchable PDF
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/ocr?format=pdf -o output.pdf
```

Returns the original PDF with an embedded OCR text layer.

### API Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## Development

### Run Tests

```bash
poetry run pytest
```

### Project Structure

```
xberg-ocr/
├── src/
│   └── xberg_ocr/
│       ├── __init__.py
│       ├── main.py              # FastAPI app
│       ├── config.py            # Configuration management
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py        # API endpoints
│       └── services/
│           ├── __init__.py
│           ├── ocr_service.py   # OCR logic with xberg
│           └── pdf_service.py   # PDF manipulation
└── tests/
    ├── __init__.py
    ├── test_api.py
    └── test_ocr_service.py
```

## License

MIT License - see LICENSE file for details.

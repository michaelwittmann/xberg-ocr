# Xberg OCR Server

A lightweight REST API for OCR-processing PDFs using [xberg](https://github.com/xberg-io/xberg) with an Ollama VLM backend.

## What it does

Upload a scanned PDF and get back either:

- **Extracted text** as JSON — for search indexing, data pipelines, or downstream processing
- **A searchable PDF** — the original file with an embedded OCR text layer

## How it works

```
Client → FastAPI → xberg SDK → Ollama (glm-ocr / deepseek-ocr / …)
```

xberg handles page rendering and image preprocessing; Ollama runs the vision-language model that reads each page.

## Quick start

=== "Docker"

    ```bash
    docker run -p 8000:8000 \
      -e OLLAMA_BASE_URL=http://your-ollama-host:11434/v1 \
      -e OLLAMA_API_KEY=your-api-key \
      -e VLM_MODEL=glm-ocr:latest \
      ghcr.io/michaelwittmann/xberg-ocr:latest
    ```

=== "Local"

    ```bash
    git clone https://github.com/michaelwittmann/xberg-ocr.git
    cd xberg-ocr
    cp .env.example .env   # edit with your Ollama URL and key
    poetry install
    poetry run uvicorn src.xberg_ocr.main:app --reload
    ```

Then test it:

```bash
# Extract text
curl -X POST -F "file=@document.pdf" http://localhost:8000/ocr?format=text

# Get searchable PDF
curl -X POST -F "file=@document.pdf" http://localhost:8000/ocr?format=pdf -o output.pdf
```

## Prerequisites

- An [Ollama](https://ollama.com) server with a vision model pulled (e.g. `glm-ocr`, `deepseek-ocr`)
- Python 3.13+ or Docker

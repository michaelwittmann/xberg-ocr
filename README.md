# Xberg OCR Server

[![CI/CD](https://github.com/michaelwittmann/xberg-ocr/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/michaelwittmann/xberg-ocr/actions/workflows/ci-cd.yml)
[![Docs](https://github.com/michaelwittmann/xberg-ocr/actions/workflows/docs.yml/badge.svg)](https://michaelwittmann.github.io/xberg-ocr)

A lightweight REST API server for OCR-processing PDFs using [xberg](https://github.com/xberg-io/xberg) with an Ollama VLM backend.

**[Full documentation →](https://michaelwittmann.github.io/xberg-ocr)**

## Quick start

```bash
docker run -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://your-ollama-host:11434/v1 \
  -e OLLAMA_API_KEY=your-api-key \
  -e VLM_MODEL=glm-ocr:latest \
  ghcr.io/michaelwittmann/xberg-ocr:latest
```

```bash
# Extract text from a PDF
curl -X POST -F "file=@document.pdf" http://localhost:8000/ocr?format=text

# Get a searchable PDF
curl -X POST -F "file=@document.pdf" http://localhost:8000/ocr?format=pdf -o output.pdf
```

## Prerequisites

- Ollama server with a vision model (e.g. `ollama pull glm-ocr`)
- Python 3.13+ or Docker

## License

MIT

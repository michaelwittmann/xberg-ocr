# API Reference

Interactive docs are also available at `http://localhost:8000/docs` when the server is running.

## Endpoints

### `GET /health`

Health check.

**Response**

```json
{"status": "healthy", "service": "xberg-ocr"}
```

---

### `POST /ocr`

Process a PDF file with OCR.

**Query parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `format` | `text` \| `pdf` | `text` | Output format |

**Request body**

`multipart/form-data` with a `file` field containing the PDF.

```bash
curl -X POST \
  -F "file=@document.pdf" \
  "http://localhost:8000/ocr?format=text"
```

**Response — `format=text`**

```json
{
  "success": true,
  "text": "Extracted text content...",
  "pages": 3,
  "processing_time_ms": 4821
}
```

**Response — `format=pdf`**

Returns the original PDF with the extracted text embedded as metadata (`Content-Type: application/pdf`).

```bash
curl -X POST \
  -F "file=@document.pdf" \
  "http://localhost:8000/ocr?format=pdf" \
  -o output.pdf
```

**Error responses**

| Status | Condition |
|---|---|
| `400` | File is not a PDF |
| `500` | OCR processing failed (check Ollama connectivity and model availability) |

---

### `GET /`

Returns service metadata.

```json
{
  "service": "xberg-ocr",
  "version": "0.1.0",
  "docs": "/docs",
  "health": "/health"
}
```

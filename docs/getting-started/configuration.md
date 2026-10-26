# Configuration

Configuration is via environment variables, loaded from a `.env` file in the project root.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Base URL of the Ollama OpenAI-compatible API. Must include `/v1`. |
| `OLLAMA_API_KEY` | _(none)_ | API key for the Ollama server, if authentication is enabled. |
| `VLM_MODEL` | `glm-ocr:latest` | Ollama model name to use for OCR. Include the tag (e.g. `:latest`). |
| `HOST` | `0.0.0.0` | Interface the server binds to. |
| `PORT` | `8000` | Port the server listens on. |

## Example `.env`

```env
OLLAMA_BASE_URL=http://your-ollama-host:11434/v1
OLLAMA_API_KEY=your-api-key-here
VLM_MODEL=glm-ocr:latest
HOST=0.0.0.0
PORT=8000
```

!!! warning "Base URL must include `/v1`"
    xberg uses the OpenAI-compatible chat completions endpoint. Always append `/v1` to your Ollama host URL — omitting it causes 404 errors.

## Choosing a model

| Model | Size | Notes |
|---|---|---|
| `glm-ocr:latest` | ~2.6 GB | Good general-purpose OCR, fast on CPU |
| `deepseek-ocr:latest` | ~6.7 GB | Higher accuracy on dense layouts |
| `maternion/LightOnOCR-2:1b` | ~1.5 GB | Smallest, lowest accuracy |

All models must be pulled in Ollama before use: `ollama pull <model>`.

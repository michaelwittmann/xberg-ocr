# Installation

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.13+ | Required for local setup |
| Poetry | 2.x | Dependency management |
| Docker | any | Alternative to local setup |
| Ollama | any | Must be reachable from the server |

## Local setup

**1. Clone the repository**

```bash
git clone https://github.com/michaelwittmann/xberg-ocr.git
cd xberg-ocr
```

**2. Install dependencies**

```bash
poetry install
```

**3. Configure environment**

```bash
cp .env.example .env
```

Edit `.env` with your Ollama details (see [Configuration](configuration.md)).

**4. Pull an OCR model in Ollama**

```bash
ollama pull glm-ocr
```

Other supported models: `deepseek-ocr`, `maternion/LightOnOCR-2:1b`.

**5. Start the server**

```bash
poetry run uvicorn src.xberg_ocr.main:app --reload
```

The server starts at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive API documentation.

## Verify the installation

```bash
curl http://localhost:8000/health
# {"status":"healthy","service":"xberg-ocr"}
```

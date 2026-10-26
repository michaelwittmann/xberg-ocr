# Docker Deployment

## Pull the image

```bash
docker pull ghcr.io/michaelwittmann/xberg-ocr:latest
```

## Run the container

```bash
docker run -d \
  --name xberg-ocr \
  -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://your-ollama-host:11434/v1 \
  -e OLLAMA_API_KEY=your-api-key \
  -e VLM_MODEL=glm-ocr:latest \
  ghcr.io/michaelwittmann/xberg-ocr:latest
```

## Docker Compose

```yaml
services:
  xberg-ocr:
    image: ghcr.io/michaelwittmann/xberg-ocr:latest
    ports:
      - "8000:8000"
    environment:
      OLLAMA_BASE_URL: http://ollama:11434/v1
      OLLAMA_API_KEY: your-api-key
      VLM_MODEL: glm-ocr:latest
    restart: unless-stopped
```

## Image tags

| Tag | Description |
|---|---|
| `latest` | Most recent build from `main` |
| `sha-<commit>` | Pinned to a specific commit SHA |

## Available images

Images are published to the GitHub Container Registry:

```
ghcr.io/michaelwittmann/xberg-ocr
```

!!! note "First pull"
    The image is ~540 MB due to xberg's bundled ONNX runtime. Subsequent pulls are fast thanks to layer caching.

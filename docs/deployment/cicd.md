# CI/CD Pipeline

The project uses GitHub Actions for automated testing and deployment.

## Workflow overview

```
push / PR to main
       │
       ▼
   ┌────────┐
   │  test  │  pytest on Python 3.13
   └────┬───┘
        │ (main branch only)
        ▼
   ┌──────────────────┐
   │  build-and-push  │  Docker → ghcr.io
   └──────────────────┘
```

## Jobs

### `test`

Runs on every push and pull request to `main`.

- Sets up Python 3.13
- Installs dependencies via Poetry (venv cached by `poetry.lock` hash)
- Runs `pytest tests/ -v`

### `build-and-push`

Runs only on pushes to `main`, after `test` passes.

- Logs in to GHCR using `GITHUB_TOKEN` (no secrets to configure)
- Builds the Docker image with layer caching via the GHA cache
- Pushes two tags: `latest` and `sha-<commit>`

## Caching strategy

| Cache | Key | Benefit |
|---|---|---|
| Poetry venv | `poetry.lock` hash | Skips `pip install` when deps unchanged |
| Docker layers | GHA cache | Skips rebuilding unchanged image layers |

## Required permissions

The workflow uses `GITHUB_TOKEN` with `packages: write` — no additional secrets or tokens need to be configured in the repository settings.

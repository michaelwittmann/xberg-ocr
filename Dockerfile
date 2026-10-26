FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY pyproject.toml poetry.lock README.md ./

RUN pip install poetry==2.1.1 && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction && \
    pip uninstall -y poetry

COPY src/ ./src/

RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "src.xberg_ocr.main:app", "--host", "0.0.0.0", "--port", "8000"]

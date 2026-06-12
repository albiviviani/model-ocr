# Local OCR Microservice 📄🔍

A compact OCR microservice for extracting text from images and PDF documents. Designed to be used as a standalone extractor by other services (for example a RAG pipeline or indexing service).

## 🚀 Highlights

- FastAPI HTTP API for file and text submission
- Image OCR via Tesseract (`pytesseract`) and multi-page PDF support via `pdf2image` 📸
- Lightweight demo frontend served by the service for quick verification 🧭
- Small CLI utilities for local extraction and API interaction 🛠️

## 🔧 Prerequisites

1. Install Tesseract OCR (required by `pytesseract`): https://github.com/tesseract-ocr/tesseract
2. Install Poppler (required by `pdf2image`):
    - macOS: `brew install poppler`
3. Create and activate a Python virtual environment and install runtime dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Run (development)

Start the FastAPI app from the project root:

```bash
uvicorn app.main:app --reload
```

Open the demo UI at:

http://127.0.0.1:8000

## 🧭 HTTP API

All API endpoints are rooted at `/api`.

- Health

   ```bash
   curl http://127.0.0.1:8000/api/health
   ```

- OCR extraction (file upload or raw text)

   ```bash
   # File upload (image or PDF)
   curl -F "file=@path/to/document.pdf" http://127.0.0.1:8000/api/ocr

   # Direct text submission
   curl -F "text=Hello world" http://127.0.0.1:8000/api/ocr
   ```

Response JSON example:

```json
{ "success": true, "source": "filename.pdf" , "text": "...extracted text..." }
```

## 🛠 CLI utilities

- Extract text locally from a file:

```bash
python ingest.py --file data/sample_document.pdf
```

- Send a file or text to a running OCR API:

```bash
python query.py --file data/sample_document.pdf
python query.py --text "Some raw text"
```

## ⚙️ Configuration

`app/services/settings.py` exposes runtime settings that can be configured via environment variables or a `.env` file:

- `OCR_LANGUAGE` (default: `eng`) — Tesseract OCR language
- `TESSERACT_CMD` — optional full path to the `tesseract` binary
- `PDF_DPI` (default: `300`) — DPI used when converting PDF pages to images

## 📁 Project layout

```
model-ocr/
├── app/
│   ├── main.py                # FastAPI entrypoint
│   └── services/
│       ├── ocr_service.py     # OCR extraction helpers
│       └── settings.py        # environment-backed settings
├── app/static/                # demo frontend (served by FastAPI)
├── data/                      # sample files (optional)
├── ingest.py                  # CLI: extract from local file
├── query.py                   # CLI: call running OCR API
├── requirements.txt
├── README.md
└── .gitignore
```

## ⛳ Production notes

- Run Tesseract on a machine with sufficient CPU; for higher throughput place the service behind a job queue / worker pool.
- For large or asynchronous workloads consider a background worker (Celery, RQ) and returning job IDs from a submission endpoint.
- Add authentication, TLS, and rate limiting when exposing the service publicly.

## 🤝 Contribution

Contributions welcome — open a feature branch (e.g. `feature/ocr-service`) and submit a PR against `main`.

---
Updated README with emoji-enhanced, production-style layout.

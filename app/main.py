"""FastAPI entrypoint for the local OCR microservice."""

import logging

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.services.ocr_service import OCRProcessor
from app.services.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_ocr_processor() -> OCRProcessor:
    """Return a configured OCR processor."""
    return OCRProcessor(settings)


@app.get("/api/health")
def health() -> dict[str, str]:
    """Return a health check payload for the OCR service."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "ocr_language": settings.ocr_language,
    }


@app.post("/api/ocr")
async def extract_text(
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
) -> dict[str, object]:
    """Extract text from an uploaded file or raw text payload."""
    try:
        if file is not None:
            contents = await file.read()
            extracted_text = get_ocr_processor().extract_text(file.filename, contents)
            return {"success": True, "source": file.filename, "text": extracted_text}

        if text is not None and text.strip():
            return {"success": True, "source": "raw_text", "text": text.strip()}

        raise ValueError("The request must include either an uploaded file or text.")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        logger.exception("Failed to extract OCR text")
        raise HTTPException(status_code=500, detail="Failed to extract OCR text.") from error


@app.get("/")
def home():
    """Serve the frontend homepage HTML file."""
    return FileResponse("app/static/index.html")


app.mount("/static", StaticFiles(directory="app/static"), name="static")

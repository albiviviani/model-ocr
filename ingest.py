"""CLI helper for extracting OCR text from local files."""

import argparse
import sys
from pathlib import Path

from app.services.ocr_service import OCRProcessor
from app.services.settings import Settings


def main() -> int:
    """Parse CLI options and extract text from a local image or PDF file."""
    parser = argparse.ArgumentParser(
        description="Extract text from a local image or PDF file using OCR."
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to an image or PDF file to extract text from.",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found at {path}", file=sys.stderr)
        return 1

    settings = Settings()
    processor = OCRProcessor(settings)

    try:
        content = path.read_bytes()
        extracted = processor.extract_text(path.name, content)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(extracted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""CLI helper for submitting files to the running OCR microservice."""

import argparse
import sys

import requests


def main() -> int:
    """Parse CLI arguments and send a file or raw text to the OCR API."""
    parser = argparse.ArgumentParser(
        description="Send a file or raw text to the local OCR service API."
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000/api/ocr",
        help="OCR service API endpoint URL.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Path to an image or PDF file to send to the API.",
    )
    parser.add_argument(
        "--text",
        help="Raw text to send to the API.",
    )
    args = parser.parse_args()

    if not args.file and not args.text:
        print("Error: Provide either --file or --text.", file=sys.stderr)
        return 1

    try:
        if args.file:
            with open(args.file, "rb") as file_obj:
                response = requests.post(
                    args.url,
                    files={"file": file_obj},
                )
        else:
            response = requests.post(
                args.url,
                data={"text": args.text},
            )

        response.raise_for_status()
        payload = response.json()
        print(payload.get("text", ""))
        return 0
    except requests.RequestException as error:
        print(f"Request error: {error}", file=sys.stderr)
        return 1
    except ValueError:
        print("Error: Invalid JSON response from OCR service.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

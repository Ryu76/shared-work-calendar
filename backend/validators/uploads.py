"""Private upload validation boundary preserving the established API errors."""
from __future__ import annotations

import zipfile
from io import BytesIO
from typing import Any

from fastapi import HTTPException

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_DOCUMENT_BYTES = 25 * 1024 * 1024
MAX_VIDEO_BYTES = 100 * 1024 * 1024
IMAGE_SIGNATURES = {
    "image/jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
    "image/png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    "image/webp": lambda data: len(data) >= 12
    and data[:4] == b"RIFF"
    and data[8:12] == b"WEBP",
}
IMAGE_SUFFIXES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
# Non-image files are limited to formats whose declared MIME type can be checked
# against their bytes. Filename extensions and browser MIME claims are never trusted.
ATTACHMENT_RULES = {
    "application/pdf": ("DOCUMENT", ".pdf", MAX_DOCUMENT_BYTES),
    "text/plain": ("DOCUMENT", ".txt", MAX_DOCUMENT_BYTES),
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": (
        "DOCUMENT",
        ".docx",
        MAX_DOCUMENT_BYTES,
    ),
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": (
        "DOCUMENT",
        ".xlsx",
        MAX_DOCUMENT_BYTES,
    ),
    "video/mp4": ("VIDEO", ".mp4", MAX_VIDEO_BYTES),
    "video/webm": ("VIDEO", ".webm", MAX_VIDEO_BYTES),
}


def validate_image_upload(upload: Any, content: bytes) -> str:
    """Validate the declared image MIME type against its byte signature."""
    claimed_type = (upload.content_type or "").lower()
    signature_check = IMAGE_SIGNATURES.get(claimed_type)
    if not signature_check or not signature_check(content):
        raise HTTPException(
            status_code=422,
            detail="이미지는 JPG, PNG, WEBP 파일만 허용하며 파일 형식과 실제 시그니처가 일치해야 합니다.",
        )
    return claimed_type


def validate_attachment_upload(upload: Any, content: bytes) -> tuple[str, str, str]:
    """Validate the declared document/video MIME type against local file bytes."""
    claimed_type = (upload.content_type or "").lower()
    rule = ATTACHMENT_RULES.get(claimed_type)
    if not rule:
        raise HTTPException(
            status_code=422,
            detail="문서는 PDF, TXT, DOCX, XLSX만, 동영상은 MP4, WEBM만 허용합니다.",
        )
    attachment_type, suffix, _ = rule
    valid = (
        (claimed_type == "application/pdf" and content.startswith(b"%PDF-"))
        or (claimed_type == "text/plain" and b"\x00" not in content and _is_utf8_text(content))
        or (
            claimed_type.endswith("wordprocessingml.document")
            and _valid_office_zip(content, "word/document.xml")
        )
        or (
            claimed_type.endswith("spreadsheetml.sheet")
            and _valid_office_zip(content, "xl/workbook.xml")
        )
        or (claimed_type == "video/mp4" and len(content) >= 12 and content[4:8] == b"ftyp")
        or (claimed_type == "video/webm" and content.startswith(b"\x1aE\xdf\xa3"))
    )
    if not valid:
        raise HTTPException(
            status_code=422,
            detail="첨부 파일의 MIME 형식과 실제 파일 구조가 일치하지 않습니다.",
        )
    return attachment_type, suffix, claimed_type


def _valid_office_zip(content: bytes, required_member: str) -> bool:
    try:
        with zipfile.ZipFile(BytesIO(content)) as archive:
            names = set(archive.namelist())
            return "[Content_Types].xml" in names and required_member in names
    except (OSError, zipfile.BadZipFile):
        return False


def _is_utf8_text(content: bytes) -> bool:
    try:
        content.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False

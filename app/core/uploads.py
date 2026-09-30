import os
import uuid
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads"


def ensure_upload_dir():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)


async def save_file(file: UploadFile) -> str:
    ensure_upload_dir()

    allowed_types = [
        "application/pdf",
        "image/jpeg",
        "image/png",
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, and PNG files are allowed"
        )

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    return filename
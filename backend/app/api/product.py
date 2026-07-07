from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile


router = APIRouter(prefix="/products", tags=["Products"])

STORAGE_DIR = Path("storage/products")
ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


@router.post("/image")
async def upload_product_image(
    image: UploadFile = File(...),
):
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG, and WebP images are allowed.",
        )

    extension = ALLOWED_CONTENT_TYPES[image.content_type]
    filename = f"{uuid4().hex}{extension}"
    file_path = STORAGE_DIR / filename

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    contents = await image.read()
    file_path.write_bytes(contents)

    return {
        "image_path": str(file_path),
        "original_filename": image.filename,
    }
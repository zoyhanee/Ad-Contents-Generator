from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.product import (
    create_product,
    get_product_by_id,
    get_products_by_user,
)
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
)

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
    
@router.post(
    "",
    response_model=ProductResponse,
    status_code=201,
)
def create_product_api(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_product(
        db=db,
        user_id=current_user.id,
        product=product,
    )
    
    
@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_my_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_products_by_user(
        db=db,
        user_id=current_user.id,
    )
    
    
@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = get_product_by_id(
        db=db,
        product_id=product_id,
        user_id=current_user.id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    return product
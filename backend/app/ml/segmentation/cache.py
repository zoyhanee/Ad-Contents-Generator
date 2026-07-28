import hashlib
from pathlib import Path

from app.ml.segmentation.product_segmenter import extract_product_foreground

STORAGE_DIR = Path("storage/products")


def get_or_create_foreground(image_path: str, model=None) -> tuple[str, str]:

    image_bytes = Path(image_path).read_bytes()
    product_hash = hashlib.sha256(image_bytes).hexdigest()
    product_dir = STORAGE_DIR / product_hash
    product_dir.mkdir(parents=True, exist_ok=True)

    fg_path = product_dir / "foreground.png"
    mask_path = product_dir / "mask.png"

    if fg_path.exists() and mask_path.exists():
        print(f"캐시 hit: {product_dir}")
        return str(fg_path), str(mask_path)

    print(f"신규 처리: {product_dir}")
    extract_product_foreground(image_path, str(fg_path), str(mask_path), model=model)
    return str(fg_path), str(mask_path)

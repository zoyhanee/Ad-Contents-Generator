from io import BytesIO

from api.client import get, get_bytes, patch, post


def upload_product_image(
    uploaded_file: BytesIO,
) -> dict:
    return post(
        "/products/image",
        files={
            "image": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        },
    )


def create_product(
    name: str,
    price: int | None,
    description: str,
    industry: str,
    image_path: str,
):
    return post(
        "/products",
        json={
            "name": name,
            "price": price,
            "description": description,
            "industry": industry,
            "image_path": image_path,
        },
    )
    

def update_product(
    product_id: int,
    name: str,
    price: int | None,
    description: str,
    industry: str,
    image_path: str,
):
    return patch(
        f"/products/{product_id}",
        json={
            "name": name,
            "price": price,
            "description": description,
            "industry": industry,
            "image_path": image_path,
        },
    )
    
    
def get_products():
    return get("/products")


def get_product(product_id: int):
    return get(f"/products/{product_id}")


def get_product_image(
    product_id: int,
) -> tuple[bytes, str]:
    return get_bytes(
        f"/products/{product_id}/image"
    )
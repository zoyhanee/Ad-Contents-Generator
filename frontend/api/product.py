from api.client import post, get
from streamlit.runtime.uploaded_file_manager import UploadedFile


def upload_product_image(
    uploaded_file: UploadedFile,
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
    
    
def get_products():
    return get("/products")


def get_product(product_id: int):
    return get(f"/products/{product_id}")
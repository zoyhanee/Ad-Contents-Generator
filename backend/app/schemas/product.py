from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    price: int | None = None
    description: str | None = None
    industry: str | None = None
    image_path: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int | None
    description: str | None
    industry: str | None
    image_path: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )
from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    product_id: int


class ProjectResponse(BaseModel):
    id: int
    product_id: int
    status: str

    model_config = ConfigDict(
        from_attributes=True,
    )
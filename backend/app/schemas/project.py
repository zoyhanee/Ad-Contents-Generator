from datetime import datetime

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
    

class ProjectSummaryResponse(BaseModel):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
    
class FinalizeProjectRequest(BaseModel):
    draft_id: str
    post_copy: str | None = None


class FinalResultResponse(BaseModel):
    id: int
    project_id: int
    version: int
    selected_draft_id: int
    image_path: str | None
    post_copy: str | None
    saved_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
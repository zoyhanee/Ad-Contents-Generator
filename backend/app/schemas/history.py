from datetime import datetime

from pydantic import BaseModel


class HistoryItemResponse(BaseModel):
    project_id: int
    product_name: str
    version: int
    image_path: str | None
    post_copy: str | None
    saved_at: datetime
    
    
class HistoryVersionResponse(BaseModel):
    id: int
    version: int
    selected_draft_id: int
    image_path: str | None
    post_copy: str | None
    saved_at: datetime


class HistoryDetailResponse(BaseModel):
    project_id: int

    product_id: int
    product_name: str
    product_price: int | None
    product_description: str | None
    product_industry: str | None

    latest_version: int
    image_path: str | None
    post_copy: str | None
    saved_at: datetime

    versions: list[HistoryVersionResponse]
    

class HistoryUpdateRequest(BaseModel):
    post_copy: str | None = None
    image_feedback: str | None = None
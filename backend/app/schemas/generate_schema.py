from pydantic import BaseModel


class GenerateRequest(BaseModel):
    project_id: int
    selected_slogan: str


class DraftResponse(BaseModel):
    id: str
    title: str
    version: int
    image_path: str | None = None
    image_prompt: str | None = None
    post_copy: str | None = None


class GenerateResponse(BaseModel):
    project_id: int
    drafts: list[DraftResponse]
    

class RegenerateDraftRequest(BaseModel):
    project_id: int
    draft_id: str
    feedback: str


class RegenerateDraftResponse(BaseModel):
    project_id: int
    draft: dict
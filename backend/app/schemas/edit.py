from pydantic import BaseModel


class EditRequest(BaseModel):
    draft_id: int
    instruction: str


class EditResponse(BaseModel):
    success: bool
    message: str
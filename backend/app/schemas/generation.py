from pydantic import BaseModel, Field


class SloganGenerationResult(BaseModel):
    slogans: list[str] = Field(default_factory=list, description="Generated slogan candidates")
    selected_slogan: str | None = Field(default=None, description="User-selected slogan")
    prompt_text: str | None = Field(default=None, description="Prompt used for slogan generation")
    model_name: str | None = Field(default=None, description="Model used for slogan generation")
    status: str = Field(default="completed", description="Generation status")


class ImageGenerationResult(BaseModel):
    image_prompt: str = Field(..., description="Prompt used for image generation")
    image_path: str | None = Field(default=None, description="Generated image file path")
    image_url: str | None = Field(default=None, description="Generated image URL")
    model_name: str | None = Field(default=None, description="Model used for image generation")
    status: str = Field(default="pending", description="Generation status")


class AdDraftResult(BaseModel):
    draft_id: str = Field(..., description="Draft label, such as A, B, or C")
    title: str | None = Field(default=None, description="Draft title")
    version: int = Field(default=1, description="Draft version")
    slogan: str | None = Field(default=None, description="Draft slogan or main copy")
    image_result: ImageGenerationResult | None = Field(default=None, description="Image generation result")
    feedback: str | None = Field(default=None, description="User feedback for regeneration")
    is_selected: bool = Field(default=False, description="Whether this draft is selected")


class AdGenerationResult(BaseModel):
    platform: str = Field(..., description="Advertising platform")
    slogan_result: SloganGenerationResult | None = Field(default=None, description="Slogan generation result")
    drafts: list[AdDraftResult] = Field(default_factory=list, description="Generated ad draft results")
    selected_draft_id: str | None = Field(default=None, description="Selected draft ID")
    status: str = Field(default="completed", description="Overall generation status")


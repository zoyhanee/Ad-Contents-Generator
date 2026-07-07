from pydantic import BaseModel, Field


class ProductPromptInput(BaseModel):
    name: str = Field(..., description="Product name")
    price: str | None = Field(default=None, description="Product price")
    description: str = Field(..., description="Product description")
    industry: str = Field(..., description="Business category")
    image_name: str | None = Field(default=None, description="Uploaded image name")
    image_type: str | None = Field(default=None, description="Uploaded image MIME type")


class StrategyPromptInput(BaseModel):
    mode: str = Field(default="faster", description="Strategy mode")
    platform: str = Field(..., description="Selected advertising platform")
    goal: str | None = Field(default=None, description="Selected advertising goal")
    style: str | None = Field(default=None, description="Selected visual style")
    poster_size: str | None = Field(default=None, description="Offline poster size")
    reuse_tone: bool = Field(default=False, description="Whether to reuse previous tone")
    custom_theme: str | None = Field(default=None, description="Optional custom theme")


class SloganPromptInput(BaseModel):
    product: ProductPromptInput
    strategy: StrategyPromptInput


class ImagePromptInput(BaseModel):
    product: ProductPromptInput
    strategy: StrategyPromptInput
    selected_slogan: str = Field(..., description="Selected slogan for image generation")


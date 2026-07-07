from typing import Optional

from pydantic import BaseModel


class ProductInfo(BaseModel):
    name: str
    price: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image_path: Optional[str] = None


class StrategyInfo(BaseModel):
    mode: str
    reuse_tone: bool = False
    platform: str
    poster_size: Optional[str] = None
    goal: Optional[str] = None
    style: Optional[str] = None


class StrategyRecommendRequest(BaseModel):
    product: ProductInfo
    strategy: StrategyInfo
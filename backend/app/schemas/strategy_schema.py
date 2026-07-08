from typing import List, Optional

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
    platforms: List[str] = []
    poster_size: Optional[str] = None
    goal: Optional[str] = None
    style: Optional[str] = None

    @property
    def platform(self) -> str:
        if self.platforms:
            return self.platforms[0]
        return "instagram"


class StrategyRecommendRequest(BaseModel):
    product: ProductInfo
    strategy: StrategyInfo
from typing import Optional

from pydantic import BaseModel


class StrategyInfo(BaseModel):
    mode: str
    reuse_tone: bool = False
    platform: str
    poster_size: Optional[str] = None
    goal: Optional[str] = None
    style: Optional[str] = None


class StrategyRecommendRequest(BaseModel):
    project_id: int
    strategy: StrategyInfo
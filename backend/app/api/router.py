from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.generate import router as generate_router
from app.api.strategy import router as strategy_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(generate_router)
api_router.include_router(strategy_router)
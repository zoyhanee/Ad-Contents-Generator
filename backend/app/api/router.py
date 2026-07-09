from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.generate import router as generate_router
from app.api.product import router as product_router
from app.api.strategy import router as strategy_router
from app.api.project import router as project_router


api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(generate_router)
api_router.include_router(product_router)
api_router.include_router(strategy_router)
api_router.include_router(project_router)
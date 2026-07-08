from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.mount(
    "/storage",
    StaticFiles(directory="storage"),
    name="storage",
)

app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": settings.PROJECT_NAME
    }
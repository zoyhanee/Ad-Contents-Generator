from fastapi import APIRouter

router = APIRouter()


@router.post("/generate", tags=["Generate"])
def generate():
    return {
        "message": "Generate endpoint is under development."
    }
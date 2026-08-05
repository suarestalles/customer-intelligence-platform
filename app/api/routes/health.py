from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_router() -> dict[str, str]:
    return {"status": "Healthy"}

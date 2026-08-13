from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.core.database import get_database
from pipelines.warehouse.database_config import Database

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_router() -> dict[str, str]:
    return {"status": "Healthy"}


@router.get("/ready")
async def readiness_router(
    database: Database = Depends(get_database),
) -> JSONResponse:
    try:
        database.query("SELECT 1")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "ready",
                "database": "healthy",
            },
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "database": "unavailable",
            },
        )

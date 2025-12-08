from fastapi import APIRouter, Depends
from sqlmodel import Session, text

from src.api.dependencies import get_session

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Health check",
    description="Check if the service is running"
)
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "lego-brick-manager"
    }


@router.get(
    "/health/ready",
    summary="Readiness check",
    description="Check if the service is ready to accept requests"
)
async def readiness_check(session: Session = Depends(get_session)):
    """Check if database connection is ready."""
    try:
        session.exec(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "not ready",
            "database": str(e)
        }
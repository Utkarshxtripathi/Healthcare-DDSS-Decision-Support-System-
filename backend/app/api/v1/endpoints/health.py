"""Health Check Endpoint."""
from fastapi import APIRouter
from backend.app.core.config import settings

router = APIRouter()


@router.get("/health", summary="System Health & Readiness")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "mode": "Research Prototype",
        "data_scope": "Synthetic Clinical Data Only",
    }

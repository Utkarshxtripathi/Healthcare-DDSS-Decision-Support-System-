"""
FastAPI Main Application
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Research Clinical Decision Support System (CDSS) powered by Machine Learning and Explainable AI (XAI). "
        "Built for CSIR scientists, clinicians, and researchers. Note: Uses synthetic patient data only."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development / PoC
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", summary="Root Status")
def root():
    return {
        "message": "Welcome to CSIR Healthcare Clinical Decision Support System (CDSS / DDSS) API",
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "health_url": f"{settings.API_V1_STR}/health",
        "data_scope": "Synthetic Clinical Data Only (Research Prototype)",
    }

"""API v1 Router aggregation."""
from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, predict, explain, research, presets

api_router = APIRouter()
api_router.include_router(health.router, tags=["System Health"])
api_router.include_router(predict.router, tags=["Clinical Risk Prediction"])
api_router.include_router(explain.router, tags=["Explainable AI (XAI)"])
api_router.include_router(research.router, tags=["Research & Benchmarks"])
api_router.include_router(presets.router, tags=["Clinical Presets"])

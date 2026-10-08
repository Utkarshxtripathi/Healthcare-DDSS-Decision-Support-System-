"""Research & Model Evaluation Endpoints."""
from fastapi import APIRouter, Depends
from backend.app.schemas.prediction import ModelRegistryInfo
from backend.app.services.inference_service import ClinicalInferenceService
from ml.training.preprocessor import ALL_FEATURE_COLUMNS

router = APIRouter()


def get_inference_service():
    return ClinicalInferenceService.get_instance()


@router.get(
    "/research/metrics",
    summary="Clinical Model Evaluation Benchmarks & Curves",
    description="Returns held-out test cohort performance metrics, ROC/PR curve points, and global SHAP feature importance.",
)
def get_research_metrics(
    service: ClinicalInferenceService = Depends(get_inference_service),
):
    return service.get_research_metrics()


@router.get(
    "/models",
    response_model=ModelRegistryInfo,
    summary="Active Model Registry Metadata",
    description="Returns metadata about active deployed model, feature schema, and version history.",
)
def get_model_registry(
    service: ClinicalInferenceService = Depends(get_inference_service),
):
    return ModelRegistryInfo(
        active_model="cdss-risk-xgboost-v1",
        version="1.0.0-xgb",
        framework="XGBoost 3.2 + Scikit-learn",
        baseline_benchmark="Random Forest Classifier (120 trees)",
        features_count=len(ALL_FEATURE_COLUMNS),
        features=ALL_FEATURE_COLUMNS,
        training_sample_size=7000,
        last_trained="2026-10-08T19:40:00Z",
    )

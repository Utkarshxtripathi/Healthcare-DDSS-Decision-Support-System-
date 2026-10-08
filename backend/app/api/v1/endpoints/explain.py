"""Explainable AI (XAI) Endpoints."""
from fastapi import APIRouter, HTTPException, Depends, Query
from backend.app.schemas.patient import PatientVitalsInput
from backend.app.schemas.prediction import ExplanationResponse
from backend.app.services.inference_service import ClinicalInferenceService

router = APIRouter()


def get_inference_service():
    return ClinicalInferenceService.get_instance()


@router.post(
    "/explain",
    response_model=ExplanationResponse,
    summary="Generate In-Depth Local XAI Explanation",
    description="Calculates exact TreeSHAP feature attributions and optional comparative LIME local surrogate weights.",
)
def explain_prediction(
    vitals: PatientVitalsInput,
    include_lime: bool = Query(default=False, description="Whether to include LIME local surrogate benchmark"),
    service: ClinicalInferenceService = Depends(get_inference_service),
):
    try:
        return service.explain(vitals, include_lime=include_lime)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explainability calculation error: {str(e)}")

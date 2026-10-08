"""Disease Risk Prediction Endpoint."""
from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.patient import PatientVitalsInput
from backend.app.schemas.prediction import PredictionResponse
from backend.app.services.inference_service import ClinicalInferenceService

router = APIRouter()


def get_inference_service():
    return ClinicalInferenceService.get_instance()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Estimate Patient Disease Risk",
    description="Processes structured patient vitals and biomarkers through the validated XGBoost model to produce calibrated risk scoring and top SHAP drivers.",
)
def predict_risk(
    vitals: PatientVitalsInput,
    service: ClinicalInferenceService = Depends(get_inference_service),
):
    try:
        return service.predict(vitals)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

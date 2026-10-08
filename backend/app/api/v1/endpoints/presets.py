"""Clinical Presets Endpoint."""
from fastapi import APIRouter, Depends
from backend.app.services.inference_service import ClinicalInferenceService

router = APIRouter()


def get_inference_service():
    return ClinicalInferenceService.get_instance()


@router.get(
    "/presets",
    summary="Clinically Plausible Sample Cases",
    description="Returns pre-configured clinical assessment cases for rapid testing and demonstrations.",
)
def get_clinical_presets(
    service: ClinicalInferenceService = Depends(get_inference_service),
):
    return service.get_presets()

"""
Prediction & XAI Response Schemas
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class FeatureContribution(BaseModel):
    feature: str
    label: str
    unit: str
    category: str
    value: float
    shap_value: float
    absolute_impact: float
    direction: str  # "increases_risk" or "decreases_risk"
    clinical_impact: str


class LimeFactor(BaseModel):
    condition: str
    weight: float
    direction: str


class PredictionResponse(BaseModel):
    patient_identifier: str
    risk_score: float = Field(..., description="Calibrated risk probability (0.0 to 1.0)")
    risk_category: str = Field(..., description="Triage classification: Low, Moderate, or High")
    risk_label: int = Field(..., description="Binary threshold indicator: 0 (Low/Mod) or 1 (High)")
    model_version: str
    model_family: str
    timestamp: str
    clinical_disclaimer: str
    top_risk_drivers: List[FeatureContribution]
    top_protective_factors: List[FeatureContribution]


class ExplanationResponse(BaseModel):
    patient_identifier: str
    predicted_risk_probability: float
    risk_category: str
    method: str = "TreeSHAP"
    base_value: float
    all_contributions: List[FeatureContribution]
    lime_comparison: Optional[Dict[str, Any]] = None
    interpretation_disclaimer: str


class ModelRegistryInfo(BaseModel):
    active_model: str
    version: str
    framework: str
    baseline_benchmark: str
    features_count: int
    features: List[str]
    training_sample_size: int
    last_trained: str

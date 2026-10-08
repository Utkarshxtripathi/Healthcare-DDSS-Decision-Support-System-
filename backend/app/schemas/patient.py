"""
Patient Clinical Observations Request Schema
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)

Enforces clinical range boundaries, physiological sanity checks,
and descriptive metadata for all patient vitals and biomarkers.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field, model_validator


class PatientVitalsInput(BaseModel):
    """
    Structured patient observations and biomarkers.
    Clinically plausible bounds are strictly validated.
    """
    age: int = Field(
        ...,
        ge=18,
        le=110,
        description="Patient age in years (Adult cohort: 18 - 110)",
        examples=[64],
    )
    sex: int = Field(
        ...,
        ge=0,
        le=1,
        description="Biological sex at birth (0: Female, 1: Male)",
        examples=[1],
    )
    heart_rate: int = Field(
        ...,
        ge=35,
        le=220,
        description="Resting heart rate in beats per minute (bpm)",
        examples=[82],
    )
    systolic_bp: int = Field(
        ...,
        ge=60,
        le=260,
        description="Systolic blood pressure in mmHg",
        examples=[148],
    )
    diastolic_bp: int = Field(
        ...,
        ge=35,
        le=150,
        description="Diastolic blood pressure in mmHg",
        examples=[92],
    )
    body_temperature: float = Field(
        ...,
        ge=34.0,
        le=42.5,
        description="Core body temperature in degrees Celsius (°C)",
        examples=[37.1],
    )
    spo2: float = Field(
        ...,
        ge=60.0,
        le=100.0,
        description="Blood oxygen saturation percentage (SpO2 %)",
        examples=[95.5],
    )
    respiratory_rate: int = Field(
        ...,
        ge=8,
        le=50,
        description="Respiratory rate in breaths per minute",
        examples=[18],
    )
    bmi: float = Field(
        ...,
        ge=12.0,
        le=65.0,
        description="Body Mass Index in kg/m²",
        examples=[29.4],
    )
    blood_glucose: int = Field(
        ...,
        ge=40,
        le=500,
        description="Fasting or random blood glucose in mg/dL",
        examples=[138],
    )
    cholesterol_total: int = Field(
        ...,
        ge=80,
        le=450,
        description="Total serum cholesterol in mg/dL",
        examples=[235],
    )
    troponin_level: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="High-sensitivity cardiac troponin in ng/mL (Normal < 0.04)",
        examples=[0.065],
    )
    crp: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="C-Reactive Protein (CRP) in mg/L (Normal < 3.0)",
        examples=[4.8],
    )
    creatinine: float = Field(
        ...,
        ge=0.2,
        le=8.0,
        description="Serum creatinine in mg/dL (Normal 0.6 - 1.3)",
        examples=[1.35],
    )
    history_hypertension: int = Field(
        ...,
        ge=0,
        le=1,
        description="Documented history of hypertension (0: No, 1: Yes)",
        examples=[1],
    )
    history_diabetes: int = Field(
        ...,
        ge=0,
        le=1,
        description="Documented history of type 2 diabetes (0: No, 1: Yes)",
        examples=[0],
    )
    smoking_status: int = Field(
        ...,
        ge=0,
        le=1,
        description="Smoking status (0: Non-smoker, 1: Active/Former smoker)",
        examples=[1],
    )
    patient_identifier: Optional[str] = Field(
        default="SYN-DEMO-001",
        description="Optional synthetic patient reference code",
    )

    @model_validator(mode="after")
    def validate_physiological_coherence(self):
        """Cross-feature physiological coherence validation."""
        if self.diastolic_bp >= self.systolic_bp:
            raise ValueError(
                f"Diastolic blood pressure ({self.diastolic_bp} mmHg) cannot be greater than or equal to systolic blood pressure ({self.systolic_bp} mmHg)."
            )
        return self

"""
Clinical Inference & XAI Orchestration Service
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)

Loads serialized XGBoost model, preprocessing pipelines, and XAI explainers;
provides synchronous inference and feature attributions for API endpoints.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pathlib import Path
import json
import joblib
import pandas as pd
import numpy as np

from backend.app.core.config import settings
from backend.app.schemas.patient import PatientVitalsInput
from backend.app.schemas.prediction import PredictionResponse, ExplanationResponse, FeatureContribution
from ml.training.preprocessor import ALL_FEATURE_COLUMNS
from ml.xai.shap_explainer import ClinicalShapExplainer
from ml.xai.lime_explainer import ClinicalLimeExplainer


class ClinicalInferenceService:
    _instance = None

    def __init__(self):
        self.models_dir = settings.ML_MODELS_DIR
        self.data_dir = settings.ML_DATA_DIR
        self.model = None
        self.rf_baseline = None
        self.preprocessor = None
        self.shap_explainer = None
        self.lime_explainer = None
        self.metrics_data = None
        self.curves_data = None
        self.global_shap_data = None
        self.load_artifacts()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_artifacts(self):
        """Load serialized models, preprocessors, and XAI explainers."""
        best_model_path = self.models_dir / "best_model.joblib"
        rf_path = self.models_dir / "random_forest_baseline.joblib"
        prep_path = self.models_dir / "preprocessor.joblib"
        metrics_path = self.models_dir / "metrics.json"
        curves_path = self.models_dir / "curves.json"
        global_shap_path = self.models_dir / "global_shap.json"

        if not best_model_path.exists():
            raise FileNotFoundError(f"Model file not found at {best_model_path}. Train the model first.")

        self.model = joblib.load(best_model_path)
        self.rf_baseline = joblib.load(rf_path) if rf_path.exists() else None
        self.preprocessor = joblib.load(prep_path) if prep_path.exists() else None

        # Load SHAP explainer
        self.shap_explainer = ClinicalShapExplainer(
            model=self.model,
            feature_names=ALL_FEATURE_COLUMNS,
        )

        # LIME explainer (lazy or background initialized)
        train_csv_path = self.data_dir / "train.csv"
        if train_csv_path.exists():
            train_df = pd.read_csv(train_csv_path)
            self.lime_explainer = ClinicalLimeExplainer(
                model=self.model,
                training_data=train_df[ALL_FEATURE_COLUMNS].values,
                feature_names=ALL_FEATURE_COLUMNS,
            )

        # Load metrics & curves
        if metrics_path.exists():
            with open(metrics_path, "r", encoding="utf-8") as f:
                self.metrics_data = json.load(f)

        if curves_path.exists():
            with open(curves_path, "r", encoding="utf-8") as f:
                self.curves_data = json.load(f)

        if global_shap_path.exists():
            with open(global_shap_path, "r", encoding="utf-8") as f:
                self.global_shap_data = json.load(f)

    def _prepare_dataframe(self, vitals: PatientVitalsInput) -> pd.DataFrame:
        """Convert pydantic patient input to ordered pandas DataFrame."""
        record = {
            "age": vitals.age,
            "sex": vitals.sex,
            "heart_rate": vitals.heart_rate,
            "systolic_bp": vitals.systolic_bp,
            "diastolic_bp": vitals.diastolic_bp,
            "body_temperature": vitals.body_temperature,
            "spo2": vitals.spo2,
            "respiratory_rate": vitals.respiratory_rate,
            "bmi": vitals.bmi,
            "blood_glucose": vitals.blood_glucose,
            "cholesterol_total": vitals.cholesterol_total,
            "troponin_level": vitals.troponin_level,
            "crp": vitals.crp,
            "creatinine": vitals.creatinine,
            "history_hypertension": vitals.history_hypertension,
            "history_diabetes": vitals.history_diabetes,
            "smoking_status": vitals.smoking_status,
        }
        return pd.DataFrame([record])[ALL_FEATURE_COLUMNS]

    def predict(self, vitals: PatientVitalsInput) -> PredictionResponse:
        """Execute risk inference and generate top feature drivers."""
        df = self._prepare_dataframe(vitals)
        probs = self.model.predict_proba(df)[0]
        risk_score = float(probs[1])

        # Risk stratification
        if risk_score < 0.30:
            risk_category = "Low"
            risk_label = 0
        elif risk_score < 0.65:
            risk_category = "Moderate"
            risk_label = 0 if risk_score < 0.50 else 1
        else:
            risk_category = "High"
            risk_label = 1

        # Calculate SHAP explanation for top drivers
        shap_res = self.shap_explainer.explain_instance(df, predicted_prob=risk_score)
        
        top_drivers = [FeatureContribution(**d) for d in shap_res["top_risk_drivers"]]
        top_protective = [FeatureContribution(**d) for d in shap_res["top_protective_factors"]]

        now_iso = datetime.now(timezone.utc).isoformat()

        return PredictionResponse(
            patient_identifier=vitals.patient_identifier or "SYN-PATIENT",
            risk_score=round(risk_score, 4),
            risk_category=risk_category,
            risk_label=risk_label,
            model_version="1.0.0-xgb",
            model_family="Gradient Boosted Decision Trees (XGBoost)",
            timestamp=now_iso,
            clinical_disclaimer=(
                "Research Proof of Concept: This output is a machine-learning statistical risk estimate "
                "based on synthetic observations. It does not constitute a clinical diagnosis or treatment directive. "
                "Clinical interpretation by a qualified healthcare professional is mandatory."
            ),
            top_risk_drivers=top_drivers,
            top_protective_factors=top_protective,
        )

    def explain(self, vitals: PatientVitalsInput, include_lime: bool = False) -> ExplanationResponse:
        """Generate comprehensive TreeSHAP and optional LIME explanations."""
        df = self._prepare_dataframe(vitals)
        risk_score = float(self.model.predict_proba(df)[0][1])
        
        risk_cat = "Low" if risk_score < 0.30 else ("Moderate" if risk_score < 0.65 else "High")
        shap_res = self.shap_explainer.explain_instance(df, predicted_prob=risk_score)
        
        all_contribs = [FeatureContribution(**d) for d in shap_res["all_contributions"]]

        lime_data = None
        if include_lime and self.lime_explainer is not None:
            lime_data = self.lime_explainer.explain_instance(df, num_features=8)

        return ExplanationResponse(
            patient_identifier=vitals.patient_identifier or "SYN-PATIENT",
            predicted_risk_probability=round(risk_score, 4),
            risk_category=risk_cat,
            method="TreeSHAP (Axiomatic Additive Shapley Values)",
            base_value=shap_res["base_value"],
            all_contributions=all_contribs,
            lime_comparison=lime_data,
            interpretation_disclaimer=shap_res["interpretation_disclaimer"],
        )

    def get_research_metrics(self) -> Dict[str, Any]:
        """Return benchmark evaluation metrics, curve points, and global SHAP summary."""
        return {
            "benchmarks": self.metrics_data,
            "curves": self.curves_data,
            "global_feature_importance": self.global_shap_data,
            "disclaimer": "Metrics evaluated on held-out synthetic test cohort (N=1,500).",
        }

    def get_presets(self) -> List[Dict[str, Any]]:
        """Return clinical prototype preset cases for one-click assessment demonstration."""
        return [
            {
                "id": "preset-normal",
                "name": "Normal Baseline Case",
                "description": "Healthy 34-year-old female, normal vitals, no pre-existing conditions.",
                "expected_tier": "Low",
                "data": {
                    "age": 34,
                    "sex": 0,
                    "heart_rate": 68,
                    "systolic_bp": 116,
                    "diastolic_bp": 74,
                    "body_temperature": 36.7,
                    "spo2": 99.0,
                    "respiratory_rate": 14,
                    "bmi": 22.4,
                    "blood_glucose": 88,
                    "cholesterol_total": 175,
                    "troponin_level": 0.005,
                    "crp": 1.1,
                    "creatinine": 0.82,
                    "history_hypertension": 0,
                    "history_diabetes": 0,
                    "smoking_status": 0,
                    "patient_identifier": "SYN-PRESET-LOW-01",
                },
            },
            {
                "id": "preset-moderate",
                "name": "Moderate Metabolic Risk Case",
                "description": "58-year-old male with history of hypertension, elevated BMI and borderline glucose.",
                "expected_tier": "Moderate",
                "data": {
                    "age": 58,
                    "sex": 1,
                    "heart_rate": 84,
                    "systolic_bp": 146,
                    "diastolic_bp": 88,
                    "body_temperature": 37.0,
                    "spo2": 96.2,
                    "respiratory_rate": 18,
                    "bmi": 31.8,
                    "blood_glucose": 142,
                    "cholesterol_total": 242,
                    "troponin_level": 0.018,
                    "crp": 3.8,
                    "creatinine": 1.15,
                    "history_hypertension": 1,
                    "history_diabetes": 0,
                    "smoking_status": 1,
                    "patient_identifier": "SYN-PRESET-MOD-02",
                },
            },
            {
                "id": "preset-acute",
                "name": "Acute Cardio-Metabolic Risk Case",
                "description": "71-year-old male presenting with acute hypertension, elevated troponin, and hypoxia.",
                "expected_tier": "High",
                "data": {
                    "age": 71,
                    "sex": 1,
                    "heart_rate": 112,
                    "systolic_bp": 178,
                    "diastolic_bp": 104,
                    "body_temperature": 37.8,
                    "spo2": 88.5,
                    "respiratory_rate": 26,
                    "bmi": 33.2,
                    "blood_glucose": 215,
                    "cholesterol_total": 288,
                    "troponin_level": 1.450,
                    "crp": 16.5,
                    "creatinine": 2.10,
                    "history_hypertension": 1,
                    "history_diabetes": 1,
                    "smoking_status": 1,
                    "patient_identifier": "SYN-PRESET-HIGH-03",
                },
            },
        ]

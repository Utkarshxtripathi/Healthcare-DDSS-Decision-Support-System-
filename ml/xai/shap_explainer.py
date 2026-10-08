"""
TreeSHAP Explainability Engine
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)

Calculates axiomatic Shapley values for local clinical predictions
and cohort-wide global feature importance.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import shap

from ml.training.preprocessor import ALL_FEATURE_COLUMNS


# Human-friendly clinical feature metadata
FEATURE_CLINICAL_LABELS: Dict[str, Dict[str, str]] = {
    "age": {"label": "Age", "unit": "years", "category": "Demographics"},
    "sex": {"label": "Biological Sex", "unit": "0=F, 1=M", "category": "Demographics"},
    "heart_rate": {"label": "Heart Rate", "unit": "bpm", "category": "Vital Signs"},
    "systolic_bp": {"label": "Systolic Blood Pressure", "unit": "mmHg", "category": "Vital Signs"},
    "diastolic_bp": {"label": "Diastolic Blood Pressure", "unit": "mmHg", "category": "Vital Signs"},
    "body_temperature": {"label": "Body Temperature", "unit": "°C", "category": "Vital Signs"},
    "spo2": {"label": "Oxygen Saturation (SpO2)", "unit": "%", "category": "Vital Signs"},
    "respiratory_rate": {"label": "Respiratory Rate", "unit": "breaths/min", "category": "Vital Signs"},
    "bmi": {"label": "Body Mass Index (BMI)", "unit": "kg/m²", "category": "Metabolic"},
    "blood_glucose": {"label": "Blood Glucose", "unit": "mg/dL", "category": "Metabolic"},
    "cholesterol_total": {"label": "Total Cholesterol", "unit": "mg/dL", "category": "Metabolic"},
    "troponin_level": {"label": "Cardiac Troponin", "unit": "ng/mL", "category": "Cardiac Biomarkers"},
    "crp": {"label": "C-Reactive Protein (CRP)", "unit": "mg/L", "category": "Inflammatory"},
    "creatinine": {"label": "Serum Creatinine", "unit": "mg/dL", "category": "Renal"},
    "history_hypertension": {"label": "Hypertension History", "unit": "0=No, 1=Yes", "category": "Medical History"},
    "history_diabetes": {"label": "Diabetes History", "unit": "0=No, 1=Yes", "category": "Medical History"},
    "smoking_status": {"label": "Smoking Status", "unit": "0=No, 1=Yes", "category": "Lifestyle"},
}


class ClinicalShapExplainer:
    """
    Manages TreeSHAP explanations for tree-based clinical risk models.
    """

    def __init__(self, model=None, feature_names: List[str] = None):
        self.feature_names = feature_names or ALL_FEATURE_COLUMNS
        self.model = model
        self.explainer = None
        if self.model is not None:
            self._init_explainer()

    def _init_explainer(self):
        # TreeExplainer is exact and fast for XGBoost and Random Forest
        self.explainer = shap.TreeExplainer(self.model)

    @classmethod
    def load(cls, model_path: str = "ml/models/best_model.joblib"):
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        model = joblib.load(path)
        return cls(model=model, feature_names=ALL_FEATURE_COLUMNS)

    def explain_instance(
        self,
        features_df: pd.DataFrame,
        predicted_prob: float,
    ) -> Dict[str, Any]:
        """
        Generate local SHAP feature contributions for a single patient assessment.
        """
        if self.explainer is None:
            raise RuntimeError("SHAP explainer is not initialized.")

        # Ensure correct column order
        df = features_df[self.feature_names]
        shap_values = self.explainer.shap_values(df)

        # Handle binary classification shapes (some versions return array of shape [1, N, 2] or [1, N])
        if isinstance(shap_values, list):
            vals = shap_values[1][0]  # Class 1 (High Risk)
        elif len(shap_values.shape) == 3:
            vals = shap_values[0, :, 1]
        elif len(shap_values.shape) == 2:
            vals = shap_values[0]
        else:
            vals = shap_values

        base_val = float(self.explainer.expected_value[1] if isinstance(self.explainer.expected_value, (list, np.ndarray)) else self.explainer.expected_value)

        contributions = []
        for feat_name, val in zip(self.feature_names, vals):
            raw_val = float(df[feat_name].iloc[0])
            meta = FEATURE_CLINICAL_LABELS.get(feat_name, {"label": feat_name, "unit": "", "category": "General"})
            shap_weight = float(val)

            # Generate clinically nuanced plain-language sentence
            if abs(shap_weight) < 0.01:
                clinical_impact = f"{meta['label']} ({raw_val} {meta['unit']}) had negligible impact on model output."
            elif shap_weight > 0:
                clinical_impact = f"{meta['label']} ({raw_val} {meta['unit']}) increased the estimated risk by {shap_weight:+.3f} log-odds."
            else:
                clinical_impact = f"{meta['label']} ({raw_val} {meta['unit']}) acted as a protective indicator, reducing estimated risk by {abs(shap_weight):.3f} log-odds."

            contributions.append({
                "feature": feat_name,
                "label": meta["label"],
                "unit": meta["unit"],
                "category": meta["category"],
                "value": raw_val,
                "shap_value": round(shap_weight, 4),
                "absolute_impact": round(abs(shap_weight), 4),
                "direction": "increases_risk" if shap_weight > 0 else "decreases_risk",
                "clinical_impact": clinical_impact,
            })

        # Rank by absolute magnitude of contribution
        contributions.sort(key=lambda x: x["absolute_impact"], reverse=True)

        top_risk_drivers = [c for c in contributions if c["direction"] == "increases_risk"][:5]
        top_protective = [c for c in contributions if c["direction"] == "decreases_risk"][:5]

        return {
            "method": "TreeSHAP",
            "base_value": round(base_val, 4),
            "predicted_risk_probability": round(predicted_prob, 4),
            "top_risk_drivers": top_risk_drivers,
            "top_protective_factors": top_protective,
            "all_contributions": contributions,
            "interpretation_disclaimer": "Feature contributions represent statistical associations within the trained model, not causal biological mechanisms. Human clinical judgment must supersede algorithmic estimates.",
        }

    def compute_global_importance(
        self,
        X_eval: pd.DataFrame,
        save_path: Optional[str] = "ml/models/global_shap.json",
    ) -> List[Dict[str, Any]]:
        """
        Compute mean absolute SHAP value for each feature across cohort.
        """
        df = X_eval[self.feature_names]
        shap_values = self.explainer.shap_values(df)

        if isinstance(shap_values, list):
            vals = shap_values[1]
        elif len(shap_values.shape) == 3:
            vals = shap_values[:, :, 1]
        else:
            vals = shap_values

        mean_abs_shap = np.mean(np.abs(vals), axis=0)
        
        global_summary = []
        for feat_name, importance in zip(self.feature_names, mean_abs_shap):
            meta = FEATURE_CLINICAL_LABELS.get(feat_name, {"label": feat_name, "unit": "", "category": "General"})
            global_summary.append({
                "feature": feat_name,
                "label": meta["label"],
                "category": meta["category"],
                "unit": meta["unit"],
                "mean_absolute_shap": round(float(importance), 4),
            })

        global_summary.sort(key=lambda x: x["mean_absolute_shap"], reverse=True)

        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(global_summary, f, indent=2)

        return global_summary

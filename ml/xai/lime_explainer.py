"""
LIME Tabular Explainability Benchmark Engine
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)

Implements local surrogate model approximations (LIME) for comparative
research evaluation alongside TreeSHAP.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from lime.lime_tabular import LimeTabularExplainer

from ml.training.preprocessor import ALL_FEATURE_COLUMNS, NUMERICAL_FEATURES, CATEGORICAL_FEATURES
from ml.xai.shap_explainer import FEATURE_CLINICAL_LABELS


class ClinicalLimeExplainer:
    """
    Local Interpretable Model-agnostic Explanations (LIME) for clinical records.
    """

    def __init__(
        self,
        model=None,
        training_data: np.ndarray = None,
        feature_names: List[str] = None,
        random_state: int = 42,
    ):
        self.model = model
        self.feature_names = feature_names or ALL_FEATURE_COLUMNS
        self.random_state = random_state
        self.explainer = None
        if training_data is not None:
            self._init_explainer(training_data)

    def _init_explainer(self, training_data: np.ndarray):
        cat_indices = [self.feature_names.index(c) for c in CATEGORICAL_FEATURES if c in self.feature_names]
        self.explainer = LimeTabularExplainer(
            training_data=training_data,
            feature_names=self.feature_names,
            class_names=["Low_Moderate_Risk", "High_Risk"],
            categorical_features=cat_indices,
            mode="classification",
            random_state=self.random_state,
        )

    @classmethod
    def load(
        cls,
        model_path: str = "ml/models/best_model.joblib",
        train_data_path: str = "ml/data/train.csv",
        random_state: int = 42,
    ):
        model = joblib.load(model_path)
        train_df = pd.read_csv(train_data_path)
        train_arr = train_df[ALL_FEATURE_COLUMNS].values
        instance = cls(
            model=model,
            training_data=train_arr,
            feature_names=ALL_FEATURE_COLUMNS,
            random_state=random_state,
        )
        return instance

    def explain_instance(
        self,
        features_df: pd.DataFrame,
        num_features: int = 10,
    ) -> Dict[str, Any]:
        """
        Generate local LIME explanation for a single clinical observation.
        """
        if self.explainer is None:
            raise RuntimeError("LIME explainer is not initialized with background data.")

        df = features_df[self.feature_names]
        row_arr = df.iloc[0].values

        # LIME requires a predict_proba function
        exp = self.explainer.explain_instance(
            data_row=row_arr,
            predict_fn=self.model.predict_proba,
            num_features=num_features,
            labels=[1],  # High Risk class
        )

        local_pred = float(exp.local_pred[0] if hasattr(exp, "local_pred") else 0.0)
        r2_score = float(exp.score if hasattr(exp, "score") else 0.0)

        raw_list = exp.as_list(label=1)
        factors = []
        for condition_str, weight in raw_list:
            factors.append({
                "condition": condition_str,
                "weight": round(float(weight), 4),
                "direction": "increases_risk" if weight > 0 else "decreases_risk",
            })

        return {
            "method": "LIME",
            "local_surrogate_prediction": round(local_pred, 4),
            "surrogate_fidelity_r2": round(r2_score, 4),
            "factors": factors,
            "disclaimer": "LIME fits a local linear surrogate model around the perturbed sample neighborhood for research comparison against TreeSHAP.",
        }

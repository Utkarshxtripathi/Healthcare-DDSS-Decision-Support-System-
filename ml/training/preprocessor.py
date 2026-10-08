"""
Clinical Feature Preprocessing Pipeline
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)

Constructs a reproducible Scikit-Learn preprocessing pipeline with
clinical imputation, scaling, and feature name preservation.
"""

from typing import List, Tuple, Dict, Any
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


NUMERICAL_FEATURES: List[str] = [
    "age",
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "body_temperature",
    "spo2",
    "respiratory_rate",
    "bmi",
    "blood_glucose",
    "cholesterol_total",
    "troponin_level",
    "crp",
    "creatinine",
]

CATEGORICAL_FEATURES: List[str] = [
    "sex",
    "history_hypertension",
    "history_diabetes",
    "smoking_status",
]

ALL_FEATURE_COLUMNS: List[str] = NUMERICAL_FEATURES + CATEGORICAL_FEATURES


class ClinicalFeaturePreprocessor:
    """
    Manages structured preprocessing for clinical vitals and laboratory records.
    Ensures identical transformations between training, inference, and XAI.
    """

    def __init__(self, scale_numerical: bool = True):
        self.scale_numerical = scale_numerical
        self.numerical_cols = NUMERICAL_FEATURES
        self.categorical_cols = CATEGORICAL_FEATURES
        self.all_feature_cols = ALL_FEATURE_COLUMNS

        # Build column transformers
        num_steps = [("imputer", SimpleImputer(strategy="median"))]
        if self.scale_numerical:
            num_steps.append(("scaler", StandardScaler()))

        self.num_pipeline = Pipeline(steps=num_steps)
        self.cat_pipeline = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent"))
        ])

        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", self.num_pipeline, self.numerical_cols),
                ("cat", self.cat_pipeline, self.categorical_cols),
            ],
            remainder="drop",
            verbose_feature_names_out=False,
        )
        self.is_fitted = False

    def fit(self, X: pd.DataFrame, y=None):
        """Fit preprocessing pipeline to training features."""
        self.preprocessor.fit(X[self.all_feature_cols])
        self.is_fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform features and return DataFrame with preserved column names."""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before transforming data.")
        
        # Ensure all columns exist, handle missing if needed
        data = X.copy()
        for col in self.all_feature_cols:
            if col not in data.columns:
                data[col] = np.nan

        arr = self.preprocessor.transform(data[self.all_feature_cols])
        return pd.DataFrame(arr, columns=self.all_feature_cols, index=X.index)

    def fit_transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        """Fit and transform training features."""
        return self.fit(X, y).transform(X)

    def get_feature_names(self) -> List[str]:
        return list(self.all_feature_cols)

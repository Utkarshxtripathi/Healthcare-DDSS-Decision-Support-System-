"""
Clinical Model Evaluation & Metric Engine
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)

Computes formal clinical performance metrics, calibration scores,
ROC/PR curves, and confusion matrix statistics.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    brier_score_loss,
    roc_curve,
    precision_recall_curve,
)
from sklearn.calibration import calibration_curve


class ClinicalModelEvaluator:
    """
    Evaluates binary clinical classification models with healthcare-specific metrics.
    """

    @staticmethod
    def evaluate(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: np.ndarray,
        model_name: str = "Model",
    ) -> Dict[str, Any]:
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()

        sensitivity = recall_score(y_true, y_pred, zero_division=0)
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        precision = precision_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        acc = accuracy_score(y_true, y_pred)
        bal_acc = balanced_accuracy_score(y_true, y_pred)
        roc_auc = roc_auc_score(y_true, y_prob)
        pr_auc = average_precision_score(y_true, y_prob)
        brier = brier_score_loss(y_true, y_prob)

        # ROC Curve
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_points = [
            {"fpr": round(float(f), 4), "tpr": round(float(t), 4)}
            for f, t in zip(fpr[:: max(1, len(fpr) // 30)], tpr[:: max(1, len(tpr) // 30)])
        ]
        # Always include endpoints
        roc_points.insert(0, {"fpr": 0.0, "tpr": 0.0})
        roc_points.append({"fpr": 1.0, "tpr": 1.0})

        # Precision-Recall Curve
        prec_arr, rec_arr, _ = precision_recall_curve(y_true, y_prob)
        pr_points = [
            {"recall": round(float(r), 4), "precision": round(float(p), 4)}
            for r, p in zip(rec_arr[:: max(1, len(rec_arr) // 30)], prec_arr[:: max(1, len(prec_arr) // 30)])
        ]

        # Calibration Curve
        prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10, strategy="uniform")
        calib_points = [
            {"predicted": round(float(p), 4), "fraction_positives": round(float(t), 4)}
            for p, t in zip(prob_pred, prob_true)
        ]

        return {
            "model_name": model_name,
            "metrics": {
                "accuracy": round(float(acc), 4),
                "balanced_accuracy": round(float(bal_acc), 4),
                "sensitivity_recall": round(float(sensitivity), 4),
                "specificity": round(float(specificity), 4),
                "precision": round(float(precision), 4),
                "f1_score": round(float(f1), 4),
                "roc_auc": round(float(roc_auc), 4),
                "pr_auc": round(float(pr_auc), 4),
                "brier_score": round(float(brier), 4),
            },
            "confusion_matrix": {
                "true_negative": int(tn),
                "false_positive": int(fp),
                "false_negative": int(fn),
                "true_positive": int(tp),
            },
            "curves": {
                "roc_curve": roc_points,
                "pr_curve": pr_points,
                "calibration_curve": calib_points,
            },
        }

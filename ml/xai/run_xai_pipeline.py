"""
XAI Pipeline: Compute Global SHAP & Verify Local Explainers
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)
"""

import json
from pathlib import Path
import pandas as pd
from ml.training.preprocessor import ALL_FEATURE_COLUMNS
from ml.xai.shap_explainer import ClinicalShapExplainer
from ml.xai.lime_explainer import ClinicalLimeExplainer


def main():
    print("Loading test data and trained models...")
    test_df = pd.read_csv("ml/data/test.csv")
    X_test = test_df[ALL_FEATURE_COLUMNS]

    # Initialize SHAP explainer
    print("Initializing TreeSHAP Explainer...")
    shap_engine = ClinicalShapExplainer.load("ml/models/best_model.joblib")

    # Compute Global SHAP importance over test cohort (sample 500 for fast reproducible baseline)
    print("Computing Global SHAP feature importance...")
    global_shap = shap_engine.compute_global_importance(
        X_test.iloc[:500],
        save_path="ml/models/global_shap.json",
    )
    print(f"Computed global SHAP for {len(global_shap)} features.")
    print("Top 5 most influential clinical features cohort-wide:")
    for i, item in enumerate(global_shap[:5], 1):
        print(f"  {i}. {item['label']} ({item['feature']}): {item['mean_absolute_shap']:.4f}")

    # Test single high-risk instance
    high_risk_idx = test_df[test_df["risk_label"] == 1].index[0]
    sample_patient = test_df.loc[[high_risk_idx]][ALL_FEATURE_COLUMNS]
    prob = float(shap_engine.model.predict_proba(sample_patient)[:, 1][0])
    
    print(f"\n--- Explaining Patient #{sample_patient.index[0]} (Predicted Risk: {prob:.1%}) ---")
    local_shap = shap_engine.explain_instance(sample_patient, predicted_prob=prob)
    print("TreeSHAP Top Risk Drivers:")
    for driver in local_shap["top_risk_drivers"]:
        print(f"  + {driver['label']} ({driver['value']} {driver['unit']}): {driver['shap_value']:+.3f}")

    # Initialize LIME explainer and verify
    print("\nInitializing LIME Explainer...")
    lime_engine = ClinicalLimeExplainer.load(
        model_path="ml/models/best_model.joblib",
        train_data_path="ml/data/train.csv",
    )
    lime_res = lime_engine.explain_instance(sample_patient, num_features=5)
    print(f"LIME Local Surrogate R^2: {lime_res['surrogate_fidelity_r2']}")
    print("LIME Top Factors:")
    for factor in lime_res["factors"]:
        print(f"  * {factor['condition']}: {factor['weight']:+.3f}")

    print("\nXAI Pipeline executed successfully!")


if __name__ == "__main__":
    main()

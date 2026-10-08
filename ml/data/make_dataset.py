"""
Dataset Pipeline: Generate, Split, and Document Synthetic Clinical Cohort
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)
"""

import json
import os
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

try:
    from ml.data.generator import SyntheticClinicalDataGenerator
except ImportError:
    from generator import SyntheticClinicalDataGenerator


def create_clinical_dataset(
    n_samples: int = 10000,
    random_state: int = 42,
    output_dir: str = "ml/data",
):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"Generating {n_samples} synthetic clinical records with random_state={random_state}...")
    generator = SyntheticClinicalDataGenerator(random_state=random_state)
    df = generator.generate(n_samples=n_samples)

    # Stratified Train/Val/Test Split (70% / 15% / 15%)
    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=random_state,
        stratify=df["risk_label"],
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=random_state,
        stratify=temp_df["risk_label"],
    )

    # Save CSV files
    full_path = out_path / "synthetic_patients.csv"
    train_path = out_path / "train.csv"
    val_path = out_path / "val.csv"
    test_path = out_path / "test.csv"

    df.to_csv(full_path, index=False)
    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"Saved full cohort: {full_path} ({len(df)} rows)")
    print(f"Saved train set:   {train_path} ({len(train_df)} rows)")
    print(f"Saved val set:     {val_path} ({len(val_df)} rows)")
    print(f"Saved test set:    {test_path} ({len(test_df)} rows)")

    # Compute Summary Metadata
    feature_meta = {
        "age": {"type": "integer", "unit": "years", "min": int(df["age"].min()), "max": int(df["age"].max()), "mean": round(float(df["age"].mean()), 1)},
        "sex": {"type": "binary", "unit": "0=Female, 1=Male", "distribution": df["sex"].value_counts(normalize=True).to_dict()},
        "heart_rate": {"type": "integer", "unit": "bpm", "min": int(df["heart_rate"].min()), "max": int(df["heart_rate"].max()), "mean": round(float(df["heart_rate"].mean()), 1)},
        "systolic_bp": {"type": "integer", "unit": "mmHg", "min": int(df["systolic_bp"].min()), "max": int(df["systolic_bp"].max()), "mean": round(float(df["systolic_bp"].mean()), 1)},
        "diastolic_bp": {"type": "integer", "unit": "mmHg", "min": int(df["diastolic_bp"].min()), "max": int(df["diastolic_bp"].max()), "mean": round(float(df["diastolic_bp"].mean()), 1)},
        "body_temperature": {"type": "float", "unit": "°C", "min": round(float(df["body_temperature"].min()), 1), "max": round(float(df["body_temperature"].max()), 1), "mean": round(float(df["body_temperature"].mean()), 2)},
        "spo2": {"type": "float", "unit": "%", "min": round(float(df["spo2"].min()), 1), "max": round(float(df["spo2"].max()), 1), "mean": round(float(df["spo2"].mean()), 1)},
        "respiratory_rate": {"type": "integer", "unit": "breaths/min", "min": int(df["respiratory_rate"].min()), "max": int(df["respiratory_rate"].max()), "mean": round(float(df["respiratory_rate"].mean()), 1)},
        "bmi": {"type": "float", "unit": "kg/m²", "min": round(float(df["bmi"].min()), 1), "max": round(float(df["bmi"].max()), 1), "mean": round(float(df["bmi"].mean()), 1)},
        "blood_glucose": {"type": "integer", "unit": "mg/dL", "min": int(df["blood_glucose"].min()), "max": int(df["blood_glucose"].max()), "mean": round(float(df["blood_glucose"].mean()), 1)},
        "cholesterol_total": {"type": "integer", "unit": "mg/dL", "min": int(df["cholesterol_total"].min()), "max": int(df["cholesterol_total"].max()), "mean": round(float(df["cholesterol_total"].mean()), 1)},
        "troponin_level": {"type": "float", "unit": "ng/mL", "min": round(float(df["troponin_level"].min()), 3), "max": round(float(df["troponin_level"].max()), 3), "mean": round(float(df["troponin_level"].mean()), 3)},
        "crp": {"type": "float", "unit": "mg/L", "min": round(float(df["crp"].min()), 1), "max": round(float(df["crp"].max()), 1), "mean": round(float(df["crp"].mean()), 1)},
        "creatinine": {"type": "float", "unit": "mg/dL", "min": round(float(df["creatinine"].min()), 2), "max": round(float(df["creatinine"].max()), 2), "mean": round(float(df["creatinine"].mean()), 2)},
        "history_hypertension": {"type": "binary", "unit": "0=No, 1=Yes", "prevalence": round(float(df["history_hypertension"].mean()), 3)},
        "history_diabetes": {"type": "binary", "unit": "0=No, 1=Yes", "prevalence": round(float(df["history_diabetes"].mean()), 3)},
        "smoking_status": {"type": "binary", "unit": "0=No, 1=Yes", "prevalence": round(float(df["smoking_status"].mean()), 3)},
    }

    metadata = {
        "dataset_name": "CSIR Synthetic Cardio-Metabolic Clinical Cohort",
        "version": "1.0.0-synthetic",
        "created_date": "2026-10-08",
        "total_records": n_samples,
        "random_state": random_state,
        "split_counts": {
            "train": len(train_df),
            "val": len(val_df),
            "test": len(test_df),
        },
        "target_variable": "risk_label",
        "class_balance": {
            "low_moderate_risk_0": int((df["risk_label"] == 0).sum()),
            "high_risk_1": int((df["risk_label"] == 1).sum()),
            "high_risk_prevalence": round(float(df["risk_label"].mean()), 4),
        },
        "risk_category_breakdown": df["risk_category"].value_counts().to_dict(),
        "features": feature_meta,
        "disclaimer": "This synthetic dataset is generated strictly for research, demonstration, and algorithm benchmarking at CSIR. It does not contain any real patient protected health information (PHI) and cannot be used for clinical diagnostic or treatment decisions.",
    }

    meta_path = out_path / "dataset_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved dataset metadata: {meta_path}")
    return metadata


if __name__ == "__main__":
    create_clinical_dataset()

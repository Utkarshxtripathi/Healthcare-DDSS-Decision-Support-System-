"""
Synthetic Patient Clinical Data Generator
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)

Generates clinically plausible synthetic patient records with realistic
physiological correlations, vital signs, metabolic indicators, and cardiovascular risk.
Strictly for research, demonstration, and benchmarking purposes.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd


class SyntheticClinicalDataGenerator:
    """
    Generates synthetic patient vitals and laboratory records based on
    epidemiological distributions and physiological covariances.
    """

    FEATURE_COLUMNS = [
        "age",
        "sex",
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
        "history_hypertension",
        "history_diabetes",
        "smoking_status",
    ]

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.rng = np.random.default_rng(random_state)

    def generate(self, n_samples: int = 10000) -> pd.DataFrame:
        """
        Generate n_samples of synthetic clinical patient records.
        """
        rng = self.rng

        # 1. Demographics
        # Age: mean 54, std 16, clipped [18, 90]
        age = np.clip(rng.normal(loc=54.0, scale=16.0, size=n_samples).round(), 18, 90).astype(int)
        
        # Sex: 1 = Male (52%), 0 = Female (48%)
        sex = rng.binomial(n=1, p=0.52, size=n_samples)

        # 2. Medical History & Habits
        # Hypertension prevalence increases with age
        p_htn = 0.15 + 0.55 * (age - 18) / (90 - 18)
        history_hypertension = rng.binomial(n=1, p=np.clip(p_htn, 0.05, 0.75))

        # Diabetes prevalence increases with age and hypertension
        p_dm = 0.08 + 0.25 * (age / 90) + 0.12 * history_hypertension
        history_diabetes = rng.binomial(n=1, p=np.clip(p_dm, 0.05, 0.45))

        # Smoking: higher in younger/middle-aged males
        p_smoke = 0.22 + 0.08 * sex - 0.05 * (age > 65)
        smoking_status = rng.binomial(n=1, p=np.clip(p_smoke, 0.10, 0.40))

        # 3. Body Mass Index (BMI)
        # Baseline normal ~26.5 with higher mean in diabetics and hypertensives
        bmi_base = rng.normal(loc=26.5, scale=4.8, size=n_samples)
        bmi = bmi_base + 3.2 * history_diabetes + 1.8 * history_hypertension
        bmi = np.clip(bmi, 15.0, 52.0).round(1)

        # 4. Cardiovascular Vitals (Correlated SBP and DBP)
        # SBP: influenced by age, BMI, hypertension history
        sbp_base = 118.0 + 0.35 * (age - 40) + 0.7 * (bmi - 25.0) + 22.0 * history_hypertension
        sbp_noise = rng.normal(0, 10.0, size=n_samples)
        systolic_bp = np.clip(sbp_base + sbp_noise, 80.0, 220.0).round().astype(int)

        # DBP: physiologically correlated with SBP
        dbp_base = 72.0 + 0.42 * (systolic_bp - 120.0)
        dbp_noise = rng.normal(0, 6.0, size=n_samples)
        diastolic_bp = np.clip(dbp_base + dbp_noise, 45.0, 130.0).round().astype(int)

        # 5. Core Temperature and Heart Rate
        # Body Temperature: normal 36.8 C, sub-population with low-grade to high fever
        has_infection = rng.binomial(1, p=0.07, size=n_samples)
        temp_normal = rng.normal(loc=36.75, scale=0.35, size=n_samples)
        temp_fever = rng.normal(loc=38.6, scale=0.65, size=n_samples)
        body_temperature = np.where(has_infection == 1, temp_fever, temp_normal)
        body_temperature = np.clip(body_temperature, 35.2, 41.2).round(1)

        # Heart rate: baseline 72 bpm, elevated with fever, stress, hypoxia
        temp_elevation = np.maximum(0.0, body_temperature - 37.0)
        hr_base = 73.0 + 8.5 * temp_elevation + 0.15 * (systolic_bp - 120.0)
        hr_noise = rng.normal(0, 11.0, size=n_samples)
        heart_rate = np.clip(hr_base + hr_noise, 45.0, 175.0).round().astype(int)

        # 6. Respiratory & Oxygenation
        # SpO2 (%): 98% baseline, reduced in smokers, acute illness
        spo2_drops = rng.exponential(scale=1.8, size=n_samples) * (smoking_status * 0.8 + has_infection * 1.5 + (age > 70) * 0.5)
        spo2 = 98.5 - spo2_drops + rng.normal(0, 0.8, size=n_samples)
        spo2 = np.clip(spo2, 72.0, 100.0).round(1)

        # Respiratory rate: normal 16 breaths/min, elevated when SpO2 drops or temp rises
        rr_base = 15.5 + 0.35 * (100.0 - spo2) + 1.2 * temp_elevation
        rr_noise = rng.normal(0, 2.5, size=n_samples)
        respiratory_rate = np.clip(rr_base + rr_noise, 10.0, 42.0).round().astype(int)

        # 7. Metabolic & Laboratory Biomarkers
        # Blood Glucose (mg/dL)
        glucose_norm = rng.normal(loc=92.0, scale=12.0, size=n_samples)
        glucose_dm = rng.normal(loc=172.0, scale=38.0, size=n_samples)
        blood_glucose = np.where(history_diabetes == 1, glucose_dm, glucose_norm)
        blood_glucose = np.clip(blood_glucose, 55.0, 390.0).round().astype(int)

        # Total Cholesterol (mg/dL)
        chol_base = 195.0 + 0.4 * age + 1.2 * (bmi - 25.0) + rng.normal(0, 28.0, size=n_samples)
        cholesterol_total = np.clip(chol_base, 110.0, 370.0).round().astype(int)

        # Troponin Level (ng/mL): Highly sensitive cardiac injury marker
        # Log-normal distribution with mostly near zero (<0.01), acute cardiac events elevated
        has_acute_cardiac = rng.binomial(1, p=0.065, size=n_samples)
        trop_baseline = rng.exponential(scale=0.008, size=n_samples)
        trop_acute = rng.exponential(scale=0.85, size=n_samples) + 0.12
        troponin_level = np.where(has_acute_cardiac == 1, trop_acute, trop_baseline)
        troponin_level = np.clip(troponin_level, 0.001, 4.80).round(3)

        # C-Reactive Protein (CRP, mg/L)
        crp_base = rng.exponential(scale=1.5, size=n_samples) + 0.5 * (bmi > 30)
        crp_elevated = rng.exponential(scale=12.0, size=n_samples) + 6.0
        crp = np.where(has_infection == 1, crp_elevated, crp_base)
        crp = np.clip(crp, 0.2, 48.0).round(1)

        # Serum Creatinine (mg/dL)
        creat_base = 0.85 + 0.18 * sex + 0.005 * age + 0.15 * history_hypertension
        creat_noise = rng.normal(0, 0.18, size=n_samples)
        creatinine = np.clip(creat_base + creat_noise, 0.45, 4.20).round(2)

        # 8. Clinical Risk Calculation (Ground-truth non-linear score)
        # Uses established clinical risk factors:
        # Troponin is a heavy cardiac risk driver
        # SBP > 160 or DBP > 100
        # Hypoxia (SpO2 < 92)
        # Severe hyperglycemia (Glucose > 200)
        # Age > 65 + Smoking + Hypertension synergy
        z = (
            -4.2
            + 0.045 * (age - 50)
            + 0.18 * sex
            + 0.035 * (bmi - 25.0)
            + 0.028 * (systolic_bp - 120.0)
            + 0.015 * (heart_rate - 75.0)
            - 0.095 * (spo2 - 96.0)
            + 0.055 * (respiratory_rate - 16.0)
            + 0.008 * (blood_glucose - 100.0)
            + 0.004 * (cholesterol_total - 200.0)
            + 4.8 * np.log1p(troponin_level * 10.0)
            + 0.038 * crp
            + 0.65 * (creatinine - 1.0)
            + 0.55 * history_hypertension
            + 0.60 * history_diabetes
            + 0.75 * smoking_status
            + 0.85 * (smoking_status * history_hypertension)  # Synergistic interaction
            + 1.10 * (troponin_level > 0.04).astype(float)    # Acute threshold penalty
        )

        # Sigmoid probability
        risk_probability = 1.0 / (1.0 + np.exp(-z))
        
        # Risk label (threshold 0.50, but with clinical calibration)
        risk_label = (risk_probability >= 0.50).astype(int)

        # Risk categories: Low (<0.30), Moderate (0.30 - 0.65), High (>=0.65)
        risk_category = np.select(
            [risk_probability < 0.30, risk_probability < 0.65],
            ["Low", "Moderate"],
            default="High",
        )

        # Assemble DataFrame
        patient_ids = [f"SYN-{i+1:05d}" for i in range(n_samples)]

        df = pd.DataFrame({
            "patient_id": patient_ids,
            "age": age,
            "sex": sex,
            "heart_rate": heart_rate,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "body_temperature": body_temperature,
            "spo2": spo2,
            "respiratory_rate": respiratory_rate,
            "bmi": bmi,
            "blood_glucose": blood_glucose,
            "cholesterol_total": cholesterol_total,
            "troponin_level": troponin_level,
            "crp": crp,
            "creatinine": creatinine,
            "history_hypertension": history_hypertension,
            "history_diabetes": history_diabetes,
            "smoking_status": smoking_status,
            "risk_score": risk_probability.round(4),
            "risk_category": risk_category,
            "risk_label": risk_label,
        })

        return df


if __name__ == "__main__":
    generator = SyntheticClinicalDataGenerator(random_state=42)
    df = generator.generate(n_samples=1000)
    print(f"Generated {len(df)} records.")
    print("Class distribution:")
    print(df["risk_label"].value_counts(normalize=True))
    print("\nRisk category distribution:")
    print(df["risk_category"].value_counts(normalize=True))

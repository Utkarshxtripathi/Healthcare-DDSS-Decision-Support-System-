# Model Card: Healthcare CDSS Disease Risk Classifier

## Model Details
- **Model Name**: Healthcare Clinical Decision Support Classifier (`cdss-risk-xgb`)
- **Version**: 1.0.0-poc (Release Date: October 2026)
- **Model Type**: Gradient Boosted Decision Trees (`XGBClassifier`) with Random Forest (`RandomForestClassifier`) Benchmark Baseline
- **Developers**: CSIR Healthcare Informatics Research Initiative
- **Target Task**: Binary estimation of patient acute cardio-metabolic risk (0: Low/Moderate Risk, 1: High Risk)
- **License**: MIT / Research Evaluation License

---

## Intended Use
- **Primary Use**: Assist clinicians, researchers, and healthcare professionals by providing probability estimates and feature-level attributions for synthetic patient vitals and metabolic measurements.
- **Primary Users**: CSIR researchers, clinical data scientists, medical trainees, and healthcare systems analysts.
- **Out-of-Scope Uses**: Autonomous diagnostic decisions, emergency triage without clinician oversight, pediatric assessment without recalibration, or real-world clinical use without institutional clinical trials.

---

## Factors & Feature Schema

The model evaluates structured physiological vitals and laboratory biomarkers:

| Feature Name | Description | Clinical Unit | Expected Range |
| :--- | :--- | :--- | :--- |
| `age` | Patient age in years | years | 18 - 95 |
| `sex` | Biological sex at birth | binary / category | Male (1), Female (0) |
| `heart_rate` | Resting heart rate | bpm | 40 - 180 |
| `systolic_bp` | Systolic blood pressure | mmHg | 70 - 220 |
| `diastolic_bp` | Diastolic blood pressure | mmHg | 40 - 130 |
| `body_temperature` | Core body temperature | °C | 35.0 - 41.5 |
| `spo2` | Blood oxygen saturation | % | 70 - 100 |
| `respiratory_rate` | Breaths per minute | breaths/min | 8 - 45 |
| `bmi` | Body Mass Index | kg/m² | 14.0 - 55.0 |
| `blood_glucose` | Fasting/random blood glucose | mg/dL | 50 - 400 |
| `cholesterol_total` | Total serum cholesterol | mg/dL | 100 - 380 |
| `troponin_level` | High-sensitivity cardiac troponin | ng/mL | 0.00 - 5.00 |
| `crp` | C-Reactive Protein (inflammatory marker) | mg/L | 0.1 - 50.0 |
| `creatinine` | Serum creatinine | mg/dL | 0.4 - 4.5 |
| `history_hypertension` | Past documented hypertension | binary (0/1) | 0 or 1 |
| `history_diabetes` | Past documented type 2 diabetes | binary (0/1) | 0 or 1 |
| `smoking_status` | Current or former smoking status | binary (0/1) | 0 or 1 |

---

## Training & Evaluation Data
- **Dataset**: CSIR Synthetic Cardio-Metabolic Cohort (`v1.0-synthetic`).
- **Sample Size**: 10,000 synthetic patient records generated using realistic epidemiological multivariate distributions with physiological covariances (e.g. correlation between SBP and DBP, BMI and Glucose).
- **Split Ratio**: 70% Train (7,000), 15% Validation (1,500), 15% Test (1,500) with stratified class balance.

---

## Performance Metrics & Evaluation Protocol
The models are evaluated against clinical priorities where false negatives (missing a high-risk patient) carry higher penalty than false positives:
- **Sensitivity / Recall**: Primary clinical safety metric.
- **ROC-AUC & PR-AUC**: Global discriminatory performance across all classification thresholds.
- **Brier Score**: Probability calibration fidelity.
- **F1-Score & Balanced Accuracy**: Balanced performance under class imbalance.

---

## Explainability (XAI) Protocol
- **TreeSHAP**: Calculates local Shapley values $\phi_i$ for each feature $i$, satisfying efficiency, symmetry, dummy, and additivity properties.
- **Reference Baseline**: Mean expected model output across background reference cohort.
- **LIME Comparison**: Local linear surrogate trained in the perturbation neighborhood of the instance for cross-method consistency validation.

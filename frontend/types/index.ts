export interface PatientVitals {
  age: number;
  sex: number;
  heart_rate: number;
  systolic_bp: number;
  diastolic_bp: number;
  body_temperature: number;
  spo2: number;
  respiratory_rate: number;
  bmi: number;
  blood_glucose: number;
  cholesterol_total: number;
  troponin_level: number;
  crp: number;
  creatinine: number;
  history_hypertension: number;
  history_diabetes: number;
  smoking_status: number;
  patient_identifier?: string;
}

export interface FeatureContribution {
  feature: string;
  label: string;
  unit: string;
  category: string;
  value: number;
  shap_value: number;
  absolute_impact: number;
  direction: "increases_risk" | "decreases_risk";
  clinical_impact: string;
}

export interface PredictionResult {
  patient_identifier: string;
  risk_score: number;
  risk_category: "Low" | "Moderate" | "High";
  risk_label: number;
  model_version: string;
  model_family: string;
  timestamp: string;
  clinical_disclaimer: string;
  top_risk_drivers: FeatureContribution[];
  top_protective_factors: FeatureContribution[];
}

export interface ExplanationResult {
  patient_identifier: string;
  predicted_risk_probability: number;
  risk_category: string;
  method: string;
  base_value: number;
  all_contributions: FeatureContribution[];
  lime_comparison?: {
    method: string;
    local_surrogate_prediction: number;
    surrogate_fidelity_r2: number;
    factors: Array<{ condition: string; weight: number; direction: string }>;
    disclaimer: string;
  };
  interpretation_disclaimer: string;
}

export interface ClinicalPreset {
  id: string;
  name: string;
  description: string;
  expected_tier: string;
  data: PatientVitals;
}

export interface ModelMetricsData {
  benchmarks: {
    timestamp: string;
    random_forest_baseline: {
      metrics: Record<string, number>;
      confusion_matrix: {
        true_negative: number;
        false_positive: number;
        false_negative: number;
        true_positive: number;
      };
    };
    xgboost_candidate: {
      metrics: Record<string, number>;
      confusion_matrix: {
        true_negative: number;
        false_positive: number;
        false_negative: number;
        true_positive: number;
      };
    };
    selected_model: string;
    selection_rationale: string;
  };
  curves: {
    random_forest: {
      roc_curve: Array<{ fpr: number; tpr: number }>;
      pr_curve: Array<{ recall: number; precision: number }>;
      calibration_curve: Array<{ predicted: number; fraction_positives: number }>;
    };
    xgboost: {
      roc_curve: Array<{ fpr: number; tpr: number }>;
      pr_curve: Array<{ recall: number; precision: number }>;
      calibration_curve: Array<{ predicted: number; fraction_positives: number }>;
    };
  };
  global_feature_importance: Array<{
    feature: string;
    label: string;
    category: string;
    unit: string;
    mean_absolute_shap: number;
  }>;
}

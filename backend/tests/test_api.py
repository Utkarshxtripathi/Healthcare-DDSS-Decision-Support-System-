"""
Backend API Test Suite
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "docs_url" in data


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "CSIR" in data["service"]


def test_presets_endpoint():
    response = client.get("/api/v1/presets")
    assert response.status_code == 200
    presets = response.json()
    assert len(presets) >= 3
    assert any(p["id"] == "preset-normal" for p in presets)
    assert any(p["id"] == "preset-acute" for p in presets)


def test_models_registry_endpoint():
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert data["active_model"] == "cdss-risk-xgboost-v1"
    assert data["features_count"] == 17


def test_research_metrics_endpoint():
    response = client.get("/api/v1/research/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "benchmarks" in data
    assert "curves" in data
    assert "global_feature_importance" in data
    assert data["benchmarks"]["selected_model"] == "xgboost_candidate"


def test_predict_risk_valid():
    sample_payload = {
        "age": 65,
        "sex": 1,
        "heart_rate": 88,
        "systolic_bp": 156,
        "diastolic_bp": 94,
        "body_temperature": 37.2,
        "spo2": 94.0,
        "respiratory_rate": 19,
        "bmi": 30.5,
        "blood_glucose": 165,
        "cholesterol_total": 245,
        "troponin_level": 0.08,
        "crp": 6.5,
        "creatinine": 1.45,
        "history_hypertension": 1,
        "history_diabetes": 1,
        "smoking_status": 1,
        "patient_identifier": "SYN-TEST-001",
    }
    response = client.post("/api/v1/predict", json=sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["patient_identifier"] == "SYN-TEST-001"
    assert 0.0 <= data["risk_score"] <= 1.0
    assert data["risk_category"] in ["Low", "Moderate", "High"]
    assert len(data["top_risk_drivers"]) > 0
    assert "Research Proof of Concept" in data["clinical_disclaimer"]


def test_predict_risk_invalid_bp_coherence():
    # Diastolic BP >= Systolic BP should fail validation
    invalid_payload = {
        "age": 50,
        "sex": 1,
        "heart_rate": 75,
        "systolic_bp": 110,
        "diastolic_bp": 125,  # Higher than SBP!
        "body_temperature": 37.0,
        "spo2": 98.0,
        "respiratory_rate": 16,
        "bmi": 25.0,
        "blood_glucose": 100,
        "cholesterol_total": 190,
        "troponin_level": 0.01,
        "crp": 1.5,
        "creatinine": 0.9,
        "history_hypertension": 0,
        "history_diabetes": 0,
        "smoking_status": 0,
    }
    response = client.post("/api/v1/predict", json=invalid_payload)
    assert response.status_code == 422  # Unprocessable Entity


def test_explain_endpoint():
    sample_payload = {
        "age": 72,
        "sex": 1,
        "heart_rate": 105,
        "systolic_bp": 172,
        "diastolic_bp": 102,
        "body_temperature": 37.6,
        "spo2": 89.0,
        "respiratory_rate": 24,
        "bmi": 32.0,
        "blood_glucose": 210,
        "cholesterol_total": 270,
        "troponin_level": 1.25,
        "crp": 14.0,
        "creatinine": 1.95,
        "history_hypertension": 1,
        "history_diabetes": 1,
        "smoking_status": 1,
        "patient_identifier": "SYN-TEST-EXPLAIN",
    }
    response = client.post("/api/v1/explain?include_lime=true", json=sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["method"] == "TreeSHAP (Axiomatic Additive Shapley Values)"
    assert len(data["all_contributions"]) == 17
    assert data["lime_comparison"] is not None
    assert "surrogate_fidelity_r2" in data["lime_comparison"]


def test_database_models_initialization():
    from backend.app.db.session import init_db, SessionLocal
    from backend.app.db.models import PatientRecord, AssessmentRecord, PredictionRecord

    init_db()
    db = SessionLocal()
    try:
        patient = PatientRecord(
            synthetic_patient_id="SYN-TEST-DB-001",
            age=55,
            sex=1,
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        assert patient.id is not None
        assert patient.synthetic_patient_id == "SYN-TEST-DB-001"
    finally:
        db.close()


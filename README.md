# Healthcare Clinical Decision Support System (CDSS / DDSS)

> **Research Proof-of-Concept & Decision Support System**  
> Developed for **CSIR (Council of Scientific and Industrial Research)** Scientists, Clinicians, and Healthcare Researchers.  
> *Combines Predictive Machine Learning (XGBoost / Random Forest) with Explainable AI (SHAP / LIME).*

---

## 🔬 Project Overview

Modern healthcare generates massive quantities of structured physiological and diagnostic data. However, translating this data into actionable, trustworthy clinical decision support remains a formidable challenge when machine learning models operate as opaque "black-boxes".

The **Healthcare CDSS/DDSS** prototype addresses this challenge by establishing **Explainable AI (XAI)** as a first-class requirement. Rather than simply classifying a patient as "high risk", the system:
1. Accepts structured vital signs and laboratory biomarkers via an intuitive clinical interface.
2. Estimates disease risk probability using calibrated supervised machine learning models.
3. Quantifies exact feature-level contributions using **TreeSHAP** (with comparative **LIME** analysis), detailing *why* the model assigned that risk score.
4. Distinguishes model-driven predictive risk from autonomous medical diagnosis to keep human medical expertise firmly in the loop.

> ⚠️ **Scope & Disclaimer**: This system is a **research prototype** utilizing **synthetic clinical data only**. It is not a certified diagnostic or therapeutic medical device. It does not replace professional clinical judgment.

---

## 🛠️ Technology Stack (2026 Architecture)

- **Frontend**: Next.js 16.4 (App Router), TypeScript, Tailwind CSS, shadcn/ui, Recharts.
- **Backend API**: FastAPI (Python 3.12), Pydantic v2 validation, Uvicorn.
- **Machine Learning**: XGBoost (Primary Candidate), Scikit-Learn (Random Forest Baseline), NumPy, Pandas.
- **Explainable AI**: SHAP (TreeExplainer for local & global attributions), LIME (TabularExplainer).
- **Persistence & Auth**: PostgreSQL via Supabase, Row-Level Security (RLS), JWT authentication foundation.
- **Deployment & DevOps**: Docker multi-stage containerization, GitHub Actions CI/CD, Render (API), Vercel (Frontend).

---

## 📐 System Architecture

```
[ Clinician / Researcher / Admin ]
               │
               ▼
   [ Next.js 16+ Frontend ]
   ├── Patient Vitals Ingestion Form (Real-time Validation)
   ├── Decision Support Dashboard (Risk Score & Tier Gauge)
   ├── Interactive XAI Studio (SHAP Waterfall, Top Risk Drivers)
   └── Research & Model Insights (ROC/PR Curves, Confusion Matrix)
               │
               ▼ HTTPS / JWT
   [ FastAPI Backend API ]
   ├── Schema Validation & Physiologic Range Enforcement
   ├── Scikit-Learn Preprocessing Pipeline
   ├── XGBoost Inference Engine (Calibrated Risk Probability)
   └── TreeSHAP Explainer Engine
               │
               ▼
   [ PostgreSQL Database (Supabase) ]
   └── Assessments, Predictions, Attributions & Audit Logs
```

---

## 📁 Repository Structure

```
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/v1/endpoints/ # API Routes (/predict, /explain, /metrics)
│   │   ├── schemas/          # Pydantic v2 Clinical Request/Response Schemas
│   │   ├── services/         # ML Inference & XAI Orchestration Services
│   │   ├── db/               # Database Connection & SQL Alchemy Models
│   │   └── ml/               # Model Loading & Preprocessing Bridges
│   ├── tests/                # Pytest Backend Test Suite
│   ├── Dockerfile            # Container configuration
│   └── requirements.txt      # Backend Python dependencies
├── ml/                       # Machine Learning & Research Workspace
│   ├── data/                 # Synthetic clinical dataset generation scripts
│   ├── training/             # RF Baseline & XGBoost training pipelines
│   ├── evaluation/           # Clinical metrics, calibration, benchmark reports
│   ├── xai/                  # SHAP & LIME explainer modules
│   ├── models/               # Serialized model artifacts (.joblib, metrics.json)
│   └── notebooks/            # Exploratory research notebooks
├── frontend/                 # Next.js 16+ Web Interface
│   ├── app/                  # Next.js App Router Pages
│   ├── components/           # UI Components (Cards, Forms, Charts, Dialogs)
│   ├── lib/                  # API Client, Utilities & Formatting
│   └── types/                # TypeScript Interfaces & Schemas
├── docs/                     # Technical Documentation
│   ├── architecture.md       # High-Level Architecture Blueprint
│   ├── model-card.md         # Mitchell et al. Model Card Specification
│   └── xai-methodology.md    # Theoretical & Applied Explainability Guide
└── README.md                 # Project Overview & Setup Instructions
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.12+
- Node.js 20+ / npm 10+
- Git

### 2. Backend & ML Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
API Documentation will be accessible at: `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
# In a separate terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend will be accessible at: `http://localhost:3000`

---

## 🧪 Synthetic Dataset & Physiological Features

The prototype evaluates structured clinical biomarkers:
- **Vital Signs**: Age, Sex, Heart Rate (bpm), Systolic & Diastolic Blood Pressure (mmHg), Body Temperature (°C), Oxygen Saturation SpO2 (%), Respiratory Rate (breaths/min), BMI (kg/m²).
- **Metabolic & Lab Markers**: Blood Glucose (mg/dL), Total Cholesterol (mg/dL), Cardiac Troponin (ng/mL), C-Reactive Protein (mg/L), Serum Creatinine (mg/dL).
- **Clinical History**: Past Hypertension, Type 2 Diabetes, Smoking Status.

---

## 📜 Ethical & Responsible AI Principles

1. **Human-in-the-Loop**: Decision support informs human clinical judgment; it never replaces it.
2. **Transparent Explanations**: Every prediction is delivered with exact feature attributions explaining the directional push of each biomarker.
3. **Data Privacy**: Built strictly with synthetic patient data, guaranteeing zero disclosure of protected health information (PHI).
4. **Reproducible Science**: All dataset random seeds, model hyperparameter configurations, and evaluation metrics are version-controlled.

---

## 📄 License
This research prototype is distributed under the Apache-2.0 / MIT Research License for scientific evaluation.

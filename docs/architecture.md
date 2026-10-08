# System Architecture: Healthcare Clinical Decision Support System (CDSS / DDSS)

## 1. Executive Summary & Architecture Goal

The **Healthcare Clinical Decision Support System (CDSS/DDSS)** is a research prototype developed for CSIR scientists, clinicians, and medical researchers. Its mission is to demonstrate how predictive machine learning (XGBoost / Random Forest) combined with Explainable AI (SHAP / LIME) can bridge the gap between complex algorithmic outputs and clinical decision-making.

The architecture emphasizes:
1. **Human-in-the-Loop Workflow**: Estimates disease risk while explicitly maintaining clinical professional judgment as the ultimate decision-maker.
2. **First-Class Explainability**: Every prediction is accompanied by feature-level attributions explaining *why* the model assigned a risk score.
3. **Decoupled Modern Stack**: Separation of presentation (Next.js 16+ TypeScript), inference orchestration (FastAPI Python), and relational persistence (PostgreSQL / Supabase).
4. **Reproducibility**: Strict versioning of synthetic datasets, preprocessing pipelines, model checkpoints, and XAI configurations.

---

## 2. System Architecture Diagram

```
                        +---------------------------------------+
                        |     Clinician / Researcher / Admin    |
                        +---------------------------------------+
                                            |
                                            | HTTPS / User Session
                                            v
+-----------------------------------------------------------------------------------+
|                            Next.js 16+ Frontend App Router                         |
|  - Patient Assessment Ingestion Form (Zod validation & Clinical Plausibility)    |
|  - Real-Time Decision Support Dashboard (Risk Score, Tier, Plausibility Flags)   |
|  - Interactive XAI Visualization (SHAP Waterfall, Top Drivers, LIME Comparison)  |
|  - Research & Model Benchmark Suite (Confusion Matrix, ROC/PR Curves, Metrics)    |
+-----------------------------------------------------------------------------------+
                                            |
                                            | JSON over HTTPS (JWT Bearer Auth)
                                            v
+-----------------------------------------------------------------------------------+
|                                FastAPI Backend Service                            |
|  - API Gateway & Versioned Endpoints (/api/v1/predict, /api/v1/explain, etc.)     |
|  - Pydantic v2 Request Validation & Clinical Bounds Enforcement                   |
|  - Role-Based Access Control Middleware (Clinician / Researcher / Admin)          |
|  - Preprocessing & Imputation Pipeline (Scikit-Learn ColumnTransformer)          |
+-----------------------------------------+-----------------------------------------+
                    |                                           |
                    v                                           v
+---------------------------------------+   +---------------------------------------+
|          ML Inference Engine          |   |          Relational Storage           |
|  - Baseline: Random Forest Classifier |   |  - PostgreSQL via Supabase            |
|  - Primary: Tuned XGBoost Classifier  |   |  - Assessments & Clinical Inputs      |
|  - Calibrated Probability Scoring     |   |  - Predictions & SHAP Attributions    |
|  - Model Registry & Metadata Store    |   |  - Audit Log & Role Level Security    |
+---------------------------------------+   +---------------------------------------+
                    |
                    v
+---------------------------------------+
|      Explainable AI (XAI) Engine      |
|  - TreeSHAP Local & Global Explainer  |
|  - Additive Feature Attribution       |
|  - Comparative LIME Local Surrogates  |
|  - Clinical Plain-Text Synthesizer    |
+---------------------------------------+
```

---

## 3. Technology Stack & Design Decisions

| Layer | Technology | Version / Specification | Rationale |
| :--- | :--- | :--- | :--- |
| **Frontend** | Next.js + React | Next.js 16+, TypeScript, Tailwind CSS | Enterprise React framework providing responsive layouts, server-side data fetching, and strict typing for clinical payloads. |
| **UI Components** | shadcn/ui + Lucide | Accessible Radix UI primitives | Fast, accessible, un-opinionated clinical component library with clean aesthetic for research review. |
| **Visualization** | Recharts / Custom SVG | Vector charting | High-performance interactive charts for risk gauges, feature attribution bars, and ROC curves. |
| **Backend API** | FastAPI | Python 3.12+ | High-throughput async framework with automatic OpenAPI documentation and native Pydantic schema validation. |
| **ML Framework** | XGBoost & Scikit-learn | Scikit-learn 1.6+, XGBoost 2.1+ | Primary gradient-boosted tree candidate paired with Random Forest baseline for structured tabular clinical data. |
| **XAI Framework** | SHAP & LIME | SHAP 0.46+, LIME 0.2+ | TreeSHAP provides mathematically axiomatic Shapley values; LIME serves as independent local surrogate benchmark. |
| **Database** | PostgreSQL | Supabase Managed Postgres | Relational schema integrity for patient assessments, risk predictions, feature contributions, and audit trails. |
| **Packaging** | Docker & Compose | Multi-stage build | Ensures consistent Python ML runtime across local environments, CI runners, and cloud hosts. |

---

## 4. Clinical Safety & Responsible AI Boundaries

1. **Human-in-the-Loop Mandate**: The application is strictly a research and decision-support prototype. It never autonomously diagnoses, prescribes, or authorizes clinical interventions.
2. **Attribution vs. Causality**: SHAP values are explicitly presented as *model-driven feature contributions* and never mischaracterized as biological causation.
3. **Plausibility & Out-of-Distribution Guardrails**: Clinical inputs that fall outside physiologically survivable bounds are flagged with clear validation warnings before inference.
4. **Synthetic Data Policy**: The proof-of-concept operates exclusively on synthetic patient records generated using clinical epidemiological statistics. No protected health information (PHI) is processed.

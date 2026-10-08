"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  Stethoscope,
  Heart,
  Activity,
  Flame,
  Wind,
  Droplets,
  FlaskConical,
  AlertCircle,
  Sparkles,
  CheckCircle2,
  HelpCircle,
} from "lucide-react";
import { PatientVitals, ClinicalPreset } from "@/types";
import { runPrediction, runExplanation, fetchPresets } from "@/lib/api";

const DEFAULT_VITALS: PatientVitals = {
  age: 62,
  sex: 1,
  heart_rate: 84,
  systolic_bp: 148,
  diastolic_bp: 92,
  body_temperature: 37.1,
  spo2: 95.0,
  respiratory_rate: 18,
  bmi: 29.5,
  blood_glucose: 145,
  cholesterol_total: 235,
  troponin_level: 0.055,
  crp: 4.5,
  creatinine: 1.25,
  history_hypertension: 1,
  history_diabetes: 0,
  smoking_status: 1,
  patient_identifier: "SYN-ASSESS-001",
};

export default function AssessmentPage() {
  const router = useRouter();
  const [vitals, setVitals] = useState<PatientVitals>(DEFAULT_VITALS);
  const [presets, setPresets] = useState<ClinicalPreset[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPresets()
      .then((data) => setPresets(data))
      .catch((err) => console.warn("Could not load presets from backend:", err));
  }, []);

  const handleInputChange = (field: keyof PatientVitals, value: any) => {
    setVitals((prev) => ({
      ...prev,
      [field]: typeof prev[field] === "number" ? Number(value) : value,
    }));
  };

  const handlePresetSelect = (preset: ClinicalPreset) => {
    setVitals(preset.data);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Client-side clinical validations
    if (vitals.diastolic_bp >= vitals.systolic_bp) {
      setError("Diastolic Blood Pressure must be lower than Systolic Blood Pressure.");
      return;
    }

    setLoading(true);
    try {
      // Run prediction and explanation simultaneously
      const [predResult, expResult] = await Promise.all([
        runPrediction(vitals),
        runExplanation(vitals, true),
      ]);

      // Save to sessionStorage for decision support view
      if (typeof window !== "undefined") {
        sessionStorage.setItem("last_prediction", JSON.stringify(predResult));
        sessionStorage.setItem("last_explanation", JSON.stringify(expResult));
        sessionStorage.setItem("last_vitals", JSON.stringify(vitals));
      }

      router.push("/decision-support");
    } catch (err: any) {
      setError(err.message || "Failed to execute clinical inference.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 flex items-center gap-2.5">
            <Stethoscope className="w-7 h-7 text-teal-600" />
            <span>Structured Patient Clinical Assessment</span>
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Ingest synthetic vitals, metabolic indicators, and biomarkers for ML risk prediction and TreeSHAP attribution.
          </p>
        </div>

        {/* Rapid Preset Loader */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            Presets:
          </span>
          {presets.length > 0 ? (
            presets.map((p) => (
              <button
                key={p.id}
                type="button"
                onClick={() => handlePresetSelect(p)}
                className="text-xs px-3 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-teal-50 hover:border-teal-400 text-slate-700 hover:text-teal-800 font-medium transition-all shadow-2xs"
              >
                {p.name.replace(" Case", "")}
              </button>
            ))
          ) : (
            <span className="text-xs text-slate-400 italic">Default synthetic profile active</span>
          )}
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm font-medium">{error}</div>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Patient Identifier */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase">Synthetic Patient ID</label>
            <input
              type="text"
              value={vitals.patient_identifier || ""}
              onChange={(e) => handleInputChange("patient_identifier", e.target.value)}
              className="mt-1 px-3 py-1.5 border border-slate-300 rounded-md text-sm font-mono font-medium focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              placeholder="SYN-PATIENT-001"
            />
          </div>
          <div className="text-xs text-slate-500 bg-slate-50 border border-slate-200 px-3 py-2 rounded-lg max-w-md">
            All entered values are mapped to the fixed 17-feature schema verified during model training and calibration.
          </div>
        </div>

        {/* Section 1: Demographics & Lifestyle */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-200 px-6 py-3 font-semibold text-sm text-slate-800 flex items-center gap-2">
            <Activity className="w-4 h-4 text-teal-600" />
            <span>1. Demographics & Lifestyle Factors</span>
          </div>
          <div className="p-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <label className="block text-xs font-medium text-slate-700">Age (years)</label>
              <input
                type="number"
                min="18"
                max="105"
                value={vitals.age}
                onChange={(e) => handleInputChange("age", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Adult cohort (18 - 105)</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Biological Sex</label>
              <select
                value={vitals.sex}
                onChange={(e) => handleInputChange("sex", e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              >
                <option value={1}>Male (1)</option>
                <option value={0}>Female (0)</option>
              </select>
              <span className="text-[11px] text-slate-400">Biological sex at birth</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Smoking Status</label>
              <select
                value={vitals.smoking_status}
                onChange={(e) => handleInputChange("smoking_status", e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              >
                <option value={0}>Non-smoker (0)</option>
                <option value={1}>Active / Former smoker (1)</option>
              </select>
              <span className="text-[11px] text-slate-400">Tobacco history</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Body Mass Index (BMI)</label>
              <input
                type="number"
                step="0.1"
                min="15.0"
                max="60.0"
                value={vitals.bmi}
                onChange={(e) => handleInputChange("bmi", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Normal 18.5 - 24.9 kg/m²</span>
            </div>
          </div>
        </div>

        {/* Section 2: Hemodynamic & Vital Signs */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-200 px-6 py-3 font-semibold text-sm text-slate-800 flex items-center gap-2">
            <Heart className="w-4 h-4 text-rose-600" />
            <span>2. Hemodynamic & Vital Signs</span>
          </div>
          <div className="p-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            <div>
              <label className="block text-xs font-medium text-slate-700">Heart Rate (bpm)</label>
              <input
                type="number"
                min="40"
                max="200"
                value={vitals.heart_rate}
                onChange={(e) => handleInputChange("heart_rate", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Normal 60 - 100</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Systolic BP (mmHg)</label>
              <input
                type="number"
                min="70"
                max="240"
                value={vitals.systolic_bp}
                onChange={(e) => handleInputChange("systolic_bp", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Normal &lt; 120</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Diastolic BP (mmHg)</label>
              <input
                type="number"
                min="40"
                max="140"
                value={vitals.diastolic_bp}
                onChange={(e) => handleInputChange("diastolic_bp", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Normal &lt; 80</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Oxygen SpO2 (%)</label>
              <input
                type="number"
                step="0.1"
                min="70"
                max="100"
                value={vitals.spo2}
                onChange={(e) => handleInputChange("spo2", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Normal 95 - 100%</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Respiratory Rate</label>
              <input
                type="number"
                min="8"
                max="45"
                value={vitals.respiratory_rate}
                onChange={(e) => handleInputChange("respiratory_rate", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Normal 12 - 20 bpm</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Body Temp (°C)</label>
              <input
                type="number"
                step="0.1"
                min="35.0"
                max="42.0"
                value={vitals.body_temperature}
                onChange={(e) => handleInputChange("body_temperature", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Normal 36.5 - 37.2</span>
            </div>
          </div>
        </div>

        {/* Section 3: Metabolic & Laboratory Biomarkers */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-200 px-6 py-3 font-semibold text-sm text-slate-800 flex items-center gap-2">
            <FlaskConical className="w-4 h-4 text-indigo-600" />
            <span>3. Metabolic & Laboratory Biomarkers</span>
          </div>
          <div className="p-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <label className="block text-xs font-medium text-slate-700">Blood Glucose (mg/dL)</label>
              <input
                type="number"
                min="50"
                max="450"
                value={vitals.blood_glucose}
                onChange={(e) => handleInputChange("blood_glucose", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Fasting &lt; 100 mg/dL</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Total Cholesterol (mg/dL)</label>
              <input
                type="number"
                min="100"
                max="400"
                value={vitals.cholesterol_total}
                onChange={(e) => handleInputChange("cholesterol_total", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Desirable &lt; 200 mg/dL</span>
            </div>

            <div className="bg-rose-50/50 p-2.5 rounded-lg border border-rose-200/60">
              <label className="block text-xs font-semibold text-rose-900">Cardiac Troponin (ng/mL)</label>
              <input
                type="number"
                step="0.001"
                min="0.0"
                max="5.0"
                value={vitals.troponin_level}
                onChange={(e) => handleInputChange("troponin_level", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-rose-300 rounded-md text-sm bg-white focus:ring-2 focus:ring-rose-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-rose-700 font-medium">Acute marker (Normal &lt; 0.04)</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">C-Reactive Protein (mg/L)</label>
              <input
                type="number"
                step="0.1"
                min="0.1"
                max="60.0"
                value={vitals.crp}
                onChange={(e) => handleInputChange("crp", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Inflammation (Normal &lt; 3.0)</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Serum Creatinine (mg/dL)</label>
              <input
                type="number"
                step="0.01"
                min="0.4"
                max="5.0"
                value={vitals.creatinine}
                onChange={(e) => handleInputChange("creatinine", e.target.value)}
                required
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              />
              <span className="text-[11px] text-slate-400">Renal function (0.6 - 1.3)</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Hypertension History</label>
              <select
                value={vitals.history_hypertension}
                onChange={(e) => handleInputChange("history_hypertension", e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              >
                <option value={0}>No (0)</option>
                <option value={1}>Yes (1)</option>
              </select>
              <span className="text-[11px] text-slate-400">Documented diagnosis</span>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700">Diabetes History</label>
              <select
                value={vitals.history_diabetes}
                onChange={(e) => handleInputChange("history_diabetes", e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
              >
                <option value={0}>No (0)</option>
                <option value={1}>Yes (1)</option>
              </select>
              <span className="text-[11px] text-slate-400">Type 2 diabetes history</span>
            </div>
          </div>
        </div>

        {/* Submit Action */}
        <div className="flex items-center justify-between pt-4">
          <p className="text-xs text-slate-500 max-w-lg">
            Submitting calls the <code>/api/v1/predict</code> and <code>/api/v1/explain</code> endpoints to produce
            calibrated risk scoring and feature-level TreeSHAP attributions.
          </p>

          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center gap-2.5 px-8 py-3.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold shadow-md transition-all disabled:opacity-50 text-base"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Executing ML Inference...</span>
              </>
            ) : (
              <>
                <CheckCircle2 className="w-5 h-5" />
                <span>Run Decision Support Assessment</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}

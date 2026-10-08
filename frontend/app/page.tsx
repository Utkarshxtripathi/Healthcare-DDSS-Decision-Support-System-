import React from "react";
import Link from "next/link";
import {
  Activity,
  ArrowRight,
  ShieldCheck,
  Cpu,
  Eye,
  FileCheck2,
  Users,
  Database,
  BarChart2,
  Lock,
} from "lucide-react";

export default function Home() {
  return (
    <div className="py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-teal-950 rounded-2xl p-8 sm:p-12 text-white shadow-xl border border-slate-700/60 relative overflow-hidden">
        <div className="max-w-3xl space-y-5 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30 text-xs font-semibold">
            <Activity className="w-3.5 h-3.5" />
            <span>CSIR Research Prototype & Proof-of-Concept</span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
            Healthcare Clinical Decision Support System{" "}
            <span className="text-teal-400 font-light block sm:inline">(CDSS / DDSS)</span>
          </h1>

          <p className="text-base sm:text-lg text-slate-300 leading-relaxed">
            Bridging machine learning and clinical practice with <strong>Explainable AI (XAI)</strong>.
            Estimates patient cardio-metabolic risk from structured vital signs and laboratory biomarkers
            while quantifying exact feature-level contributions using <strong>TreeSHAP</strong>.
          </p>

          <div className="flex flex-wrap gap-4 pt-2">
            <Link
              href="/assessment"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-semibold shadow-md transition-all transform hover:-translate-y-0.5"
            >
              <span>Begin Clinical Assessment</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              href="/research"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium border border-slate-600 transition-colors"
            >
              <BarChart2 className="w-4 h-4 text-teal-400" />
              <span>Research & Benchmarks</span>
            </Link>

            <Link
              href="/architecture"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium border border-slate-600 transition-colors"
            >
              <Cpu className="w-4 h-4 text-teal-400" />
              <span>Architecture Spec</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Proof-of-Concept Core Metrics Banner */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Model Accuracy", value: "97.1%", desc: "XGBoost candidate on held-out test cohort" },
          { label: "Clinical Sensitivity", value: "98.4%", desc: "High-risk recall minimizing false negatives" },
          { label: "ROC-AUC Score", value: "0.998", desc: "Discriminative ability across thresholds" },
          { label: "Synthetic Cohort", value: "10,000", desc: "Statistically validated patient records" },
        ].map((stat, idx) => (
          <div key={idx} className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
            <div className="text-2xl sm:text-3xl font-extrabold text-teal-700">{stat.value}</div>
            <div className="font-semibold text-slate-900 text-sm mt-1">{stat.label}</div>
            <div className="text-xs text-slate-500 mt-0.5">{stat.desc}</div>
          </div>
        ))}
      </div>

      {/* System Pillars */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 mb-6">Foundational System Capabilities</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center font-bold">
              <Activity className="w-5 h-5" />
            </div>
            <h3 className="font-semibold text-slate-900 text-base">Structured Clinical Ingestion</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Real-time validation for 17 vital signs, metabolic indicators, and history markers with physiological
              coherence enforcement (e.g., SBP &gt; DBP).
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-lg bg-teal-50 text-teal-700 flex items-center justify-center font-bold">
              <Eye className="w-5 h-5" />
            </div>
            <h3 className="font-semibold text-slate-900 text-base">First-Class Explainable AI</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Every risk score is backed by axiomatic <strong>TreeSHAP</strong> feature contributions, accompanied by
              independent <strong>LIME</strong> local surrogate comparisons.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center font-bold">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="font-semibold text-slate-900 text-base">Human-in-the-Loop Safety</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Explicit guardrails ensure predictive output is contextualized as decision support, guaranteeing medical
              professionals retain total clinical authority.
            </p>
          </div>
        </div>
      </div>

      {/* Target Audiences */}
      <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-xs space-y-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Designed for Multidisciplinary Healthcare Research</h2>
          <p className="text-sm text-slate-500 mt-1">Aligned with CSIR and clinical partner evaluation needs.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 pt-2">
          <div className="border-l-4 border-teal-500 pl-4 space-y-1">
            <h4 className="font-semibold text-slate-900 text-sm">Clinicians</h4>
            <p className="text-xs text-slate-600">
              Rapid structured assessment, intuitive risk tier categorization, and plain-language driver breakdowns.
            </p>
          </div>

          <div className="border-l-4 border-blue-500 pl-4 space-y-1">
            <h4 className="font-semibold text-slate-900 text-sm">Medical Researchers</h4>
            <p className="text-xs text-slate-600">
              Rigorous performance evaluation, confusion matrix inspection, calibration analysis, and SHAP/LIME comparison.
            </p>
          </div>

          <div className="border-l-4 border-indigo-500 pl-4 space-y-1">
            <h4 className="font-semibold text-slate-900 text-sm">Healthcare Administrators</h4>
            <p className="text-xs text-slate-600">
              Operational feasibility, reproducible ML containerization, role-based governance, and API extensibility roadmap.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

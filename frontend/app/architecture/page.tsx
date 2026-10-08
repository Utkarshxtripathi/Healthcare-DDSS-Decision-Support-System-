import React from "react";
import { Layers, Server, Globe, Cpu, Database, ShieldCheck, GitBranch } from "lucide-react";

export default function ArchitecturePage() {
  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto space-y-8">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 flex items-center gap-3">
          <Layers className="w-8 h-8 text-teal-600" />
          <span>Healthcare CDSS / DDSS System Architecture</span>
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Modern 2026 decoupled architecture: Next.js frontend + FastAPI ML backend + TreeSHAP XAI + PostgreSQL.
        </p>
      </div>

      {/* Layer Matrix */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-teal-50 text-teal-700">
              <Globe className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-base">Frontend Layer</h3>
              <p className="text-xs text-slate-500">Next.js 16+ / React 19 / TypeScript / Tailwind CSS</p>
            </div>
          </div>
          <ul className="text-xs text-slate-600 space-y-2 list-disc list-inside">
            <li>Structured clinical input validation and physiological coherence checks.</li>
            <li>Real-time visual risk gauge with calibrated thresholds.</li>
            <li>Interactive TreeSHAP feature contribution waterfalls and LIME comparison tabs.</li>
            <li>Role-aware UI states (Clinician, Researcher, Healthcare Administrator).</li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-blue-50 text-blue-700">
              <Server className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-base">Backend & Inference API</h3>
              <p className="text-xs text-slate-500">FastAPI / Python 3.12 / Pydantic v2 / Uvicorn</p>
            </div>
          </div>
          <ul className="text-xs text-slate-600 space-y-2 list-disc list-inside">
            <li>High-throughput async REST endpoints (<code>/predict</code>, <code>/explain</code>, <code>/metrics</code>).</li>
            <li>Strict Pydantic field-level boundary validation with clinical range limits.</li>
            <li>In-memory singleton model cache ensuring sub-100ms inference latency.</li>
            <li>CORS configured for secure decoupled deployment.</li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-purple-50 text-purple-700">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-base">Machine Learning & XAI Engine</h3>
              <p className="text-xs text-slate-500">XGBoost 3.2 / Scikit-Learn / SHAP / LIME</p>
            </div>
          </div>
          <ul className="text-xs text-slate-600 space-y-2 list-disc list-inside">
            <li>Supervised XGBoost classifier evaluated against Random Forest baseline.</li>
            <li>Axiomatic polynomial-time TreeSHAP computation for exact local Shapley values.</li>
            <li>LIME tabular local surrogate module for cross-methodological verification.</li>
            <li>Calibrated risk probability scoring and confusion matrix benchmarking.</li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-amber-50 text-amber-700">
              <Database className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-base">Persistence & Auth Foundation</h3>
              <p className="text-xs text-slate-500">PostgreSQL / Supabase / Row-Level Security</p>
            </div>
          </div>
          <ul className="text-xs text-slate-600 space-y-2 list-disc list-inside">
            <li>Relational schemas for patients, assessments, predictions, and audit logs.</li>
            <li>JWT token-based authentication with role-based access control.</li>
            <li>Row-Level Security (RLS) policies guaranteeing audit trail immutability.</li>
            <li>Clean migration path to HIPAA/enterprise VPC environments.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  ArrowLeft,
  Eye,
  TrendingUp,
  TrendingDown,
  Info,
  Layers,
  Sparkles,
  FileText,
  Activity,
  CheckCircle2,
} from "lucide-react";
import { PredictionResult, ExplanationResult, FeatureContribution, PatientVitals } from "@/types";

export default function DecisionSupportPage() {
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [explanation, setExplanation] = useState<ExplanationResult | null>(null);
  const [vitals, setVitals] = useState<PatientVitals | null>(null);
  const [activeTab, setActiveTab] = useState<"shap" | "lime" | "summary">("shap");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedPred = sessionStorage.getItem("last_prediction");
      const storedExp = sessionStorage.getItem("last_explanation");
      const storedVitals = sessionStorage.getItem("last_vitals");

      if (storedPred) setPrediction(JSON.parse(storedPred));
      if (storedExp) setExplanation(JSON.parse(storedExp));
      if (storedVitals) setVitals(JSON.parse(storedVitals));
    }
  }, []);

  if (!prediction) {
    return (
      <div className="py-16 px-4 max-w-4xl mx-auto text-center space-y-6">
        <div className="w-16 h-16 rounded-full bg-teal-50 text-teal-600 flex items-center justify-center mx-auto">
          <Activity className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-slate-800">No Assessment Found</h2>
        <p className="text-sm text-slate-500 max-w-md mx-auto">
          Please run a patient assessment first to generate calibrated risk probabilities and TreeSHAP explainability attributions.
        </p>
        <Link
          href="/assessment"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold transition-all shadow-md"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Go to Patient Assessment</span>
        </Link>
      </div>
    );
  }

  const riskTierColor = {
    Low: {
      badge: "bg-emerald-100 text-emerald-800 border-emerald-300",
      gauge: "bg-emerald-500",
      icon: ShieldCheck,
      border: "border-emerald-200",
      bg: "bg-emerald-50/50",
    },
    Moderate: {
      badge: "bg-amber-100 text-amber-800 border-amber-300",
      gauge: "bg-amber-500",
      icon: AlertTriangle,
      border: "border-amber-200",
      bg: "bg-amber-50/50",
    },
    High: {
      badge: "bg-rose-100 text-rose-800 border-rose-300",
      gauge: "bg-rose-600",
      icon: ShieldAlert,
      border: "border-rose-200",
      bg: "bg-rose-50/50",
    },
  }[prediction.risk_category] || {
    badge: "bg-slate-100 text-slate-800 border-slate-300",
    gauge: "bg-slate-500",
    icon: Info,
    border: "border-slate-200",
    bg: "bg-slate-50",
  };

  const RiskIcon = riskTierColor.icon;
  const riskPct = Math.round(prediction.risk_score * 100);

  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto space-y-8">
      {/* Top Header with Back button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-semibold text-slate-500 bg-slate-100 px-2.5 py-0.5 rounded border border-slate-200">
              {prediction.patient_identifier}
            </span>
            <span className="text-xs text-slate-400">Assessment Timestamp: {new Date(prediction.timestamp).toLocaleTimeString()}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 mt-1">Clinical Decision Support & XAI Report</h1>
        </div>

        <Link
          href="/assessment"
          className="inline-flex items-center gap-2 text-sm text-slate-600 hover:text-teal-700 font-medium self-start sm:self-auto px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Adjust Observations</span>
        </Link>
      </div>

      {/* Primary Clinical Risk Card */}
      <div className={`p-6 sm:p-8 rounded-2xl border ${riskTierColor.border} ${riskTierColor.bg} shadow-sm space-y-6`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-xl bg-white shadow-xs border border-slate-200">
                <RiskIcon className="w-8 h-8 text-teal-700" />
              </div>
              <div>
                <span className={`text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider border ${riskTierColor.badge}`}>
                  {prediction.risk_category} Risk Tier
                </span>
                <h2 className="text-3xl font-extrabold text-slate-900 mt-1.5">
                  {riskPct}% <span className="text-base font-normal text-slate-600">Estimated Cardio-Metabolic Risk</span>
                </h2>
              </div>
            </div>
          </div>

          <div className="text-right md:border-l md:border-slate-200/80 md:pl-6 space-y-1">
            <div className="text-xs font-semibold text-slate-500 uppercase">Model Specification</div>
            <div className="text-sm font-semibold text-slate-900">{prediction.model_family}</div>
            <div className="text-xs text-slate-500 font-mono">Version: {prediction.model_version}</div>
          </div>
        </div>

        {/* Visual Risk Gauge Bar */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs font-medium text-slate-600">
            <span>Low Risk (0 - 29%)</span>
            <span>Moderate (30 - 64%)</span>
            <span>High Risk (65 - 100%)</span>
          </div>
          <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden flex">
            <div className="w-[30%] bg-emerald-200 border-r border-white"></div>
            <div className="w-[35%] bg-amber-200 border-r border-white"></div>
            <div className="w-[35%] bg-rose-200"></div>
          </div>
          <div className="relative pt-1">
            <div
              className="absolute -top-3 transform -translate-x-1/2 flex flex-col items-center"
              style={{ left: `${Math.min(98, Math.max(2, riskPct))}%` }}
            >
              <div className="w-3 h-3 bg-slate-900 rotate-45 transform"></div>
              <span className="text-[10px] font-bold text-slate-900 font-mono mt-0.5">{riskPct}%</span>
            </div>
          </div>
        </div>

        {/* Clinical Safety Box */}
        <div className="bg-white/90 p-4 rounded-xl border border-slate-200 text-xs text-slate-600 flex items-start gap-3 mt-4">
          <Info className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
          <p className="leading-relaxed">
            <strong>Clinical Notice:</strong> {prediction.clinical_disclaimer}
          </p>
        </div>
      </div>

      {/* Tabs for XAI Exploration */}
      <div className="space-y-6">
        <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
          <button
            onClick={() => setActiveTab("shap")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
              activeTab === "shap"
                ? "bg-teal-600 text-white shadow-xs"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>TreeSHAP Feature Contributions</span>
          </button>

          <button
            onClick={() => setActiveTab("lime")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
              activeTab === "lime"
                ? "bg-teal-600 text-white shadow-xs"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>LIME Local Surrogate Comparison</span>
          </button>

          <button
            onClick={() => setActiveTab("summary")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
              activeTab === "summary"
                ? "bg-teal-600 text-white shadow-xs"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Clinical Summary & Observations</span>
          </button>
        </div>

        {/* Tab 1: TreeSHAP */}
        {activeTab === "shap" && explanation && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                <div>
                  <h3 className="text-base font-bold text-slate-900">TreeSHAP Local Attribution Breakdown</h3>
                  <p className="text-xs text-slate-500">
                    Quantifies the marginal push (in log-odds) that each clinical biomarker added or subtracted from the baseline population risk.
                  </p>
                </div>
                <div className="text-xs font-mono bg-slate-50 px-3 py-1.5 rounded border border-slate-200 text-slate-600">
                  Base Value (\u03c6\u2080): {explanation.base_value}
                </div>
              </div>

              {/* Attribution Bars */}
              <div className="space-y-3 pt-2">
                {explanation.all_contributions.map((c, idx) => {
                  const isRisk = c.direction === "increases_risk";
                  const widthPct = Math.min(100, Math.round(c.absolute_impact * 25));

                  return (
                    <div key={idx} className="p-3 rounded-lg border border-slate-100 hover:bg-slate-50/80 transition-colors space-y-1.5">
                      <div className="flex items-center justify-between text-xs font-medium">
                        <div className="flex items-center gap-2">
                          {isRisk ? (
                            <TrendingUp className="w-4 h-4 text-rose-600 flex-shrink-0" />
                          ) : (
                            <TrendingDown className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                          )}
                          <span className="font-bold text-slate-900">{c.label}</span>
                          <span className="text-slate-500 font-mono">
                            = {c.value} {c.unit}
                          </span>
                        </div>
                        <div className="flex items-center gap-2 font-mono">
                          <span
                            className={`font-bold ${
                              isRisk ? "text-rose-600" : "text-emerald-600"
                            }`}
                          >
                            {c.shap_value > 0 ? `+${c.shap_value.toFixed(3)}` : c.shap_value.toFixed(3)}
                          </span>
                        </div>
                      </div>

                      {/* Visual Bar */}
                      <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all ${
                            isRisk ? "bg-rose-500" : "bg-emerald-500"
                          }`}
                          style={{ width: `${Math.max(4, widthPct)}%` }}
                        ></div>
                      </div>

                      <div className="text-[11px] text-slate-500 italic pl-6">{c.clinical_impact}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: LIME */}
        {activeTab === "lime" && explanation?.lime_comparison && (
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-6">
            <div className="border-b border-slate-100 pb-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h3 className="text-base font-bold text-slate-900">LIME Local Surrogate Benchmark</h3>
                <p className="text-xs text-slate-500">
                  Independent linear approximation in the local perturbation neighborhood of this patient instance.
                </p>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full font-semibold border border-blue-200">
                  Surrogate Fidelity R\u00b2: {explanation.lime_comparison.surrogate_fidelity_r2}
                </span>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {explanation.lime_comparison.factors.map((f, idx) => (
                <div key={idx} className="p-3 rounded-lg border border-slate-200 bg-slate-50/60 flex items-center justify-between text-xs">
                  <div className="font-mono text-slate-800">{f.condition}</div>
                  <div
                    className={`font-mono font-bold ${
                      f.weight > 0 ? "text-rose-600" : "text-emerald-600"
                    }`}
                  >
                    {f.weight > 0 ? `+${f.weight}` : f.weight}
                  </div>
                </div>
              ))}
            </div>

            <div className="text-xs text-slate-500 italic bg-amber-50/60 p-3 rounded-lg border border-amber-200/60">
              {explanation.lime_comparison.disclaimer}
            </div>
          </div>
        )}

        {/* Tab 3: Clinical Summary */}
        {activeTab === "summary" && vitals && (
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-6">
            <h3 className="text-base font-bold text-slate-900">Recorded Patient Vitals & Indicators</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 text-xs">
              {Object.entries(vitals).map(([key, val]) => (
                <div key={key} className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                  <div className="text-slate-400 capitalize">{key.replace(/_/g, " ")}</div>
                  <div className="font-semibold text-slate-800 text-sm mt-0.5">{String(val)}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

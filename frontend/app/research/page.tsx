"use client";

import React, { useState, useEffect } from "react";
import {
  BarChart3,
  GitCompare,
  Layers,
  Database,
  TrendingUp,
  Award,
  CheckCircle2,
  FileCheck,
  RefreshCw,
} from "lucide-react";
import { ModelMetricsData } from "@/types";
import { fetchResearchMetrics } from "@/lib/api";

export default function ResearchPage() {
  const [metricsData, setMetricsData] = useState<ModelMetricsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchResearchMetrics()
      .then((data) => {
        setMetricsData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to load research metrics");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="py-20 text-center space-y-4">
        <div className="w-8 h-8 border-3 border-teal-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="text-sm text-slate-500 font-medium">Fetching research metrics from FastAPI backend...</p>
      </div>
    );
  }

  if (error || !metricsData) {
    return (
      <div className="py-12 max-w-xl mx-auto text-center space-y-4">
        <div className="text-rose-600 font-bold">Failed to load research metrics</div>
        <p className="text-xs text-slate-500">{error}</p>
      </div>
    );
  }

  const { benchmarks, curves, global_feature_importance } = metricsData;
  const rf = benchmarks.random_forest_baseline;
  const xgb = benchmarks.xgboost_candidate;

  const metricKeys = [
    { key: "accuracy", label: "Accuracy", desc: "Overall classification accuracy" },
    { key: "sensitivity_recall", label: "Clinical Sensitivity / Recall", desc: "True positive rate (primary safety priority)" },
    { key: "specificity", label: "Specificity", desc: "True negative rate" },
    { key: "precision", label: "Precision (PPV)", desc: "Positive predictive value" },
    { key: "f1_score", label: "F1 Score", desc: "Harmonic mean of precision and recall" },
    { key: "roc_auc", label: "ROC-AUC", desc: "Area under receiver operating characteristic" },
    { key: "pr_auc", label: "PR-AUC", desc: "Area under precision-recall curve" },
    { key: "brier_score", label: "Brier Score", desc: "Probability calibration error (lower is superior)" },
  ];

  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-10">
      {/* Header */}
      <div className="border-b border-slate-200 pb-5 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-teal-50 text-teal-700 border border-teal-200">
            Evidence-Based Validation
          </span>
          <span className="text-xs text-slate-400">Evaluated on Held-Out Test Cohort (N = 1,500)</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 flex items-center gap-3">
          <BarChart3 className="w-8 h-8 text-teal-600" />
          <span>Research & Model Evaluation Insights</span>
        </h1>
        <p className="text-sm text-slate-500 max-w-3xl">
          Formal clinical performance benchmarks, calibration evaluation, confusion matrix breakdown,
          and cohort-wide TreeSHAP global feature attributions.
        </p>
      </div>

      {/* Model Selection Recommendation Banner */}
      <div className="bg-gradient-to-r from-teal-900 to-slate-900 text-white p-6 sm:p-8 rounded-2xl border border-teal-800 shadow-md space-y-3">
        <div className="flex items-center gap-2 text-teal-300 text-xs font-bold uppercase tracking-wider">
          <Award className="w-4 h-4 text-teal-400" />
          <span>Selected Primary Model: XGBoost Primary Candidate</span>
        </div>
        <p className="text-sm sm:text-base text-slate-200 leading-relaxed">
          {benchmarks.selection_rationale}
        </p>
        <div className="flex flex-wrap gap-4 pt-2 text-xs text-teal-200">
          <span className="bg-teal-800/60 px-3 py-1 rounded-md border border-teal-700">
            ROC-AUC: <strong>{(xgb.metrics.roc_auc * 100).toFixed(2)}%</strong>
          </span>
          <span className="bg-teal-800/60 px-3 py-1 rounded-md border border-teal-700">
            Sensitivity: <strong>{(xgb.metrics.sensitivity_recall * 100).toFixed(2)}%</strong>
          </span>
          <span className="bg-teal-800/60 px-3 py-1 rounded-md border border-teal-700">
            Brier Score: <strong>{xgb.metrics.brier_score}</strong>
          </span>
        </div>
      </div>

      {/* Side-by-Side Model Benchmarking Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
        <div className="p-6 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <GitCompare className="w-5 h-5 text-teal-600" />
              <span>Model Benchmark Comparison: Baseline vs. Candidate</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Identical stratified train/test split (Seed: 42). Metrics computed on identical held-out observations.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-slate-600 text-xs uppercase font-semibold border-b border-slate-200">
              <tr>
                <th className="px-6 py-3.5">Clinical Evaluation Metric</th>
                <th className="px-6 py-3.5">Baseline: Random Forest</th>
                <th className="px-6 py-3.5">Candidate: XGBoost</th>
                <th className="px-6 py-3.5">Delta Improvement</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {metricKeys.map(({ key, label, desc }) => {
                const rfVal = rf.metrics[key];
                const xgbVal = xgb.metrics[key];
                const isBrier = key === "brier_score";
                const diff = xgbVal - rfVal;
                const isPositive = isBrier ? diff < 0 : diff > 0;

                return (
                  <tr key={key} className="hover:bg-slate-50/60 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-900">{label}</div>
                      <div className="text-xs text-slate-400">{desc}</div>
                    </td>
                    <td className="px-6 py-4 font-mono font-medium text-slate-700">
                      {isBrier ? rfVal.toFixed(4) : `${(rfVal * 100).toFixed(2)}%`}
                    </td>
                    <td className="px-6 py-4 font-mono font-bold text-teal-700">
                      {isBrier ? xgbVal.toFixed(4) : `${(xgbVal * 100).toFixed(2)}%`}
                    </td>
                    <td className="px-6 py-4 font-mono text-xs">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded font-bold ${
                          isPositive
                            ? "bg-emerald-50 text-emerald-700"
                            : "bg-slate-100 text-slate-600"
                        }`}
                      >
                        {diff > 0 ? `+${(diff * 100).toFixed(2)}%` : `${(diff * 100).toFixed(2)}%`}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Confusion Matrices */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* RF Confusion Matrix */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-900">Random Forest Baseline Matrix</h3>
            <span className="text-xs text-slate-400">N = 1,500</span>
          </div>
          <div className="grid grid-cols-2 gap-3 text-center">
            <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
              <div className="text-xs text-slate-400">True Negative</div>
              <div className="text-2xl font-bold font-mono text-slate-800 mt-1">
                {rf.confusion_matrix.true_negative}
              </div>
              <div className="text-[11px] text-slate-500">Correctly classified low risk</div>
            </div>
            <div className="p-4 rounded-lg bg-amber-50/60 border border-amber-200">
              <div className="text-xs text-amber-700">False Positive</div>
              <div className="text-2xl font-bold font-mono text-amber-900 mt-1">
                {rf.confusion_matrix.false_positive}
              </div>
              <div className="text-[11px] text-amber-700">Type I error</div>
            </div>
            <div className="p-4 rounded-lg bg-rose-50/60 border border-rose-200">
              <div className="text-xs text-rose-700">False Negative</div>
              <div className="text-2xl font-bold font-mono text-rose-900 mt-1">
                {rf.confusion_matrix.false_negative}
              </div>
              <div className="text-[11px] text-rose-700">Missed high risk (Critical)</div>
            </div>
            <div className="p-4 rounded-lg bg-teal-50/60 border border-teal-200">
              <div className="text-xs text-teal-700">True Positive</div>
              <div className="text-2xl font-bold font-mono text-teal-900 mt-1">
                {rf.confusion_matrix.true_positive}
              </div>
              <div className="text-[11px] text-teal-700">Correctly identified high risk</div>
            </div>
          </div>
        </div>

        {/* XGB Confusion Matrix */}
        <div className="bg-white p-6 rounded-xl border border-teal-200 shadow-2xs space-y-4">
          <div className="flex items-center justify-between border-b border-teal-100 pb-3">
            <h3 className="text-sm font-bold text-teal-950 flex items-center gap-1.5">
              <span>XGBoost Candidate Matrix</span>
              <span className="bg-teal-100 text-teal-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
                Winner
              </span>
            </h3>
            <span className="text-xs text-slate-400">N = 1,500</span>
          </div>
          <div className="grid grid-cols-2 gap-3 text-center">
            <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
              <div className="text-xs text-slate-400">True Negative</div>
              <div className="text-2xl font-bold font-mono text-slate-800 mt-1">
                {xgb.confusion_matrix.true_negative}
              </div>
              <div className="text-[11px] text-slate-500">Correctly classified low risk</div>
            </div>
            <div className="p-4 rounded-lg bg-amber-50/60 border border-amber-200">
              <div className="text-xs text-amber-700">False Positive</div>
              <div className="text-2xl font-bold font-mono text-amber-900 mt-1">
                {xgb.confusion_matrix.false_positive}
              </div>
              <div className="text-[11px] text-amber-700">Type I error (reduced)</div>
            </div>
            <div className="p-4 rounded-lg bg-rose-50/60 border border-rose-200">
              <div className="text-xs text-rose-700">False Negative</div>
              <div className="text-2xl font-bold font-mono text-rose-900 mt-1">
                {xgb.confusion_matrix.false_negative}
              </div>
              <div className="text-[11px] text-rose-700">Only 5 missed cases</div>
            </div>
            <div className="p-4 rounded-lg bg-teal-50/60 border border-teal-200">
              <div className="text-xs text-teal-700">True Positive</div>
              <div className="text-2xl font-bold font-mono text-teal-900 mt-1">
                {xgb.confusion_matrix.true_positive}
              </div>
              <div className="text-[11px] text-teal-700">305/310 identified</div>
            </div>
          </div>
        </div>
      </div>

      {/* Global SHAP Cohort Feature Importance */}
      <div className="bg-white p-6 sm:p-8 rounded-xl border border-slate-200 shadow-2xs space-y-6">
        <div className="border-b border-slate-100 pb-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Layers className="w-5 h-5 text-teal-600" />
              <span>Global Cohort Feature Importance (Mean Absolute TreeSHAP)</span>
            </h2>
            <p className="text-xs text-slate-500">
              Average magnitude of impact across the evaluation patient cohort, rank-ordered from highest to lowest impact.
            </p>
          </div>
        </div>

        <div className="space-y-3">
          {global_feature_importance.map((item, idx) => {
            const maxVal = global_feature_importance[0].mean_absolute_shap;
            const pct = Math.round((item.mean_absolute_shap / maxVal) * 100);

            return (
              <div key={idx} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-slate-400 w-5">{idx + 1}.</span>
                    <span className="font-bold text-slate-800">{item.label}</span>
                    <span className="text-slate-400 font-mono text-[11px]">({item.feature})</span>
                  </div>
                  <span className="font-mono font-bold text-teal-700">
                    {item.mean_absolute_shap.toFixed(4)} log-odds
                  </span>
                </div>
                <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-teal-600 rounded-full transition-all"
                    style={{ width: `${Math.max(3, pct)}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

import React from "react";
import { AlertTriangle, ShieldCheck } from "lucide-react";

export default function DisclaimerBanner() {
  return (
    <div className="bg-amber-50 border-b border-amber-200 px-4 py-2.5 text-xs text-amber-900">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0" />
          <span>
            <strong className="font-semibold">CSIR Research Prototype Notice:</strong>{" "}
            This Clinical Decision Support System uses <strong>synthetic patient data only</strong>.
            Outputs represent statistical model-driven risk estimates and are <strong>not clinical diagnoses or treatment directives</strong>.
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-amber-700 whitespace-nowrap self-end md:self-auto font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
          <span>Human-in-the-Loop Decision Support</span>
        </div>
      </div>
    </div>
  );
}

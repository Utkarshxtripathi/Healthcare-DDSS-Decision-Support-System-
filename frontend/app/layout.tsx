import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import DisclaimerBanner from "@/components/DisclaimerBanner";

export const metadata: Metadata = {
  title: "CSIR Healthcare CDSS / DDSS | Explainable Clinical Decision Support",
  description:
    "A machine learning and Explainable AI (XAI) clinical decision support prototype developed for CSIR scientists, clinicians, and medical researchers.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-slate-50 text-slate-900 antialiased">
        <DisclaimerBanner />
        <Navbar />
        <main className="flex-1">{children}</main>
        <footer className="bg-slate-900 border-t border-slate-800 text-slate-400 py-6 text-xs">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
            <p>© 2026 CSIR Healthcare Informatics Initiative. Clinical Decision Support Research Prototype.</p>
            <p>Strictly for Scientific Evaluation & Demonstration. Synthetic Data Only.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}

"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, Stethoscope, BarChart3, Layers, UserCheck, Shield } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();
  const [activeRole, setActiveRole] = useState<"Clinician" | "Researcher" | "Admin">("Clinician");

  const navLinks = [
    { href: "/", label: "Overview", icon: Activity },
    { href: "/assessment", label: "Patient Assessment", icon: Stethoscope },
    { href: "/decision-support", label: "Decision Support & XAI", icon: Shield },
    { href: "/research", label: "Research & Benchmarks", icon: BarChart3 },
    { href: "/architecture", label: "Architecture", icon: Layers },
  ];

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo & Name */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-teal-600 flex items-center justify-center text-white shadow-md">
              <Activity className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg tracking-tight text-white">CSIR CDSS / DDSS</span>
                <span className="bg-teal-500/20 text-teal-300 text-[10px] font-semibold px-2 py-0.5 rounded-full border border-teal-500/40">
                  XAI PoC 2026
                </span>
              </div>
              <p className="text-xs text-slate-400">Clinical Decision Support & Explainable AI</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-teal-600 text-white shadow-sm"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Role Switcher Simulator */}
          <div className="flex items-center gap-3">
            <div className="hidden lg:flex items-center bg-slate-800/80 p-1 rounded-lg border border-slate-700 text-xs">
              <UserCheck className="w-3.5 h-3.5 text-slate-400 ml-1.5 mr-1" />
              {(["Clinician", "Researcher", "Admin"] as const).map((role) => (
                <button
                  key={role}
                  onClick={() => setActiveRole(role)}
                  className={`px-2.5 py-1 rounded font-medium transition-all ${
                    activeRole === role
                      ? "bg-teal-600 text-white shadow-xs"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {role}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-950/60 border border-emerald-800/50 px-2.5 py-1 rounded-full">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              <span className="font-medium">FastAPI ML Ready</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

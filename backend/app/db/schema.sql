-- CSIR Healthcare Clinical Decision Support System (CDSS / DDSS)
-- PostgreSQL & Supabase Database Migration & RLS Policy Definition

-- 1. Custom Types
CREATE TYPE user_role AS ENUM ('clinician', 'researcher', 'admin');
CREATE TYPE risk_tier AS ENUM ('Low', 'Moderate', 'High');

-- 2. User Profiles Table (Linked to Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role user_role NOT NULL DEFAULT 'clinician',
    department TEXT DEFAULT 'Clinical Research',
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 3. Synthetic Patients Table
CREATE TABLE IF NOT EXISTS public.patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    synthetic_patient_id TEXT UNIQUE NOT NULL,
    age INT NOT NULL CHECK (age >= 18 AND age <= 120),
    sex INT NOT NULL CHECK (sex IN (0, 1)),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 4. Clinical Assessments Table
CREATE TABLE IF NOT EXISTS public.assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES public.patients(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    vitals JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 5. Risk Predictions Table
CREATE TABLE IF NOT EXISTS public.predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES public.assessments(id) ON DELETE CASCADE,
    risk_score NUMERIC(5, 4) NOT NULL CHECK (risk_score >= 0.0 AND risk_score <= 1.0),
    risk_category risk_tier NOT NULL,
    risk_label INT NOT NULL CHECK (risk_label IN (0, 1)),
    model_version TEXT NOT NULL,
    model_family TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 6. Feature Attributions (TreeSHAP) Table
CREATE TABLE IF NOT EXISTS public.feature_attributions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prediction_id UUID NOT NULL REFERENCES public.predictions(id) ON DELETE CASCADE,
    feature_name TEXT NOT NULL,
    feature_value NUMERIC(10, 4) NOT NULL,
    shap_value NUMERIC(10, 4) NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('increases_risk', 'decreases_risk')),
    clinical_impact TEXT NOT NULL
);

-- 7. Audit Trail Logs Table
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id UUID,
    metadata JSONB DEFAULT '{}'::jsonb,
    ip_address TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 8. Indexes for Query Performance
CREATE INDEX IF NOT EXISTS idx_assessments_user_id ON public.assessments(user_id);
CREATE INDEX IF NOT EXISTS idx_assessments_patient_id ON public.assessments(patient_id);
CREATE INDEX IF NOT EXISTS idx_predictions_assessment_id ON public.predictions(assessment_id);
CREATE INDEX IF NOT EXISTS idx_feature_attributions_pred_id ON public.feature_attributions(prediction_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON public.audit_logs(user_id);

-- 9. Row Level Security (RLS) Enablement
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.feature_attributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- 10. RLS Policies

-- Profiles: Users can view their own profile; admins can view all
CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id OR (SELECT role FROM public.profiles WHERE id = auth.uid()) = 'admin');

-- Assessments: Clinicians view their own; researchers and admins view all research assessments
CREATE POLICY "Clinicians can view their own assessments"
    ON public.assessments FOR SELECT
    USING (
        auth.uid() = user_id
        OR (SELECT role FROM public.profiles WHERE id = auth.uid()) IN ('researcher', 'admin')
    );

CREATE POLICY "Clinicians can create assessments"
    ON public.assessments FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Predictions: Readable if the user can read the parent assessment
CREATE POLICY "Users can view predictions for authorized assessments"
    ON public.predictions FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.assessments a
            WHERE a.id = predictions.assessment_id
            AND (
                a.user_id = auth.uid()
                OR (SELECT role FROM public.profiles WHERE id = auth.uid()) IN ('researcher', 'admin')
            )
        )
    );

-- Audit logs: Read-only for admins; system inserts
CREATE POLICY "Admins can view audit logs"
    ON public.audit_logs FOR SELECT
    USING ((SELECT role FROM public.profiles WHERE id = auth.uid()) = 'admin');

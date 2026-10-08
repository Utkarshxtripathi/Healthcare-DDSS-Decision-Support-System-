# Explainable AI (XAI) Methodology in Clinical Decision Support

## 1. The Imperative of Clinical Explainability

In medical informatics, high predictive accuracy without transparency is insufficient for adoption. Clinicians require interpretability to:
1. **Validate Biological Plausibility**: Confirm that model predictions align with established pathophysiological mechanisms.
2. **Detect Artifacts & Spurious Correlations**: Identify if a model is relying on dataset anomalies rather than genuine risk factors.
3. **Facilitate Clinician-Patient Communication**: Enable doctors to explain why a patient is identified as high-risk and discuss targeted interventions.
4. **Foster Trust and Accountability**: Ensure decisions are verifiable rather than deriving from an opaque "black-box".

---

## 2. SHAP (SHapley Additive exPlanations)

### Theoretical Foundation
SHAP is grounded in cooperative game theory (Lloyd Shapley, 1953) and unifies six prior explanation methods into a single axiomatic framework (Lundberg & Lee, 2017).

For an individual patient assessment with feature vector $x$, the local explanation model $g(z')$ is linear in simplified inputs:
$$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i$$

Where:
- $f(x)$ is the model output (log-odds or probability margin).
- $\phi_0 = \mathbb{E}[f(x)]$ is the base value (expected outcome across the background population).
- $\phi_i \in \mathbb{R}$ is the Shapley value for feature $i$, representing the marginal contribution of that feature to the deviation from the base value.

### TreeSHAP Algorithm
Because our primary models are tree-based ensembles (XGBoost and Random Forest), we deploy **TreeSHAP** (Lundberg et al., Nature Machine Intelligence 2020). TreeSHAP computes exact Shapley values in polynomial time $\mathcal{O}(TLD^2)$ rather than exponential time $\mathcal{O}(M 2^M)$ required for model-agnostic sampling:
- $T$: Number of trees
- $L$: Maximum number of leaves
- $D$: Maximum tree depth

### Local vs. Global Insights
- **Local Explanations**: For a specific patient, SHAP quantifies exact directional pushes:
  - *Positive $\phi_i$*: Feature value increased the patient's predicted risk (e.g. SBP = 168 mmHg pushes risk upwards by +0.24).
  - *Negative $\phi_i$*: Feature value served as a protective factor (e.g. SpO2 = 99% pushes risk downwards by -0.11).
- **Global Explanations**: Mean absolute Shapley value across the cohort:
  $$I_j = \frac{1}{N} \sum_{k=1}^N |\phi_j^{(k)}|$$
  Rank-orders features by overall clinical importance across the patient population.

---

## 3. LIME (Local Interpretable Model-agnostic Explanations)

As an independent benchmark, we implement **LIME** (Ribeiro et al., KDD 2016). LIME approximates any complex model locally around a specific patient instance $x$ by training an interpretable surrogate model:
$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$

Where:
- $\pi_x(z)$ defines an exponential kernel distance measuring proximity between perturbation samples $z$ and instance $x$.
- $g$ is a sparse linear regressor.
- $\Omega(g)$ penalizes model complexity to ensure human readability.

### Methodological Comparison

| Property | TreeSHAP | LIME |
| :--- | :--- | :--- |
| **Foundational Theory** | Cooperative Game Theory (Shapley Values) | Local linear surrogate regression |
| **Theoretical Guarantees** | Consistency, Missingness, Efficiency | Empirical local approximation |
| **Computation Speed** | Deterministic polynomial $\mathcal{O}(TLD^2)$ | Perturbation sampling $\mathcal{O}(K \cdot M)$ |
| **Stability** | 100% deterministic & exact for trees | Stochastic across perturbation seeds |
| **Role in Prototype** | **Primary Local & Global Explainer** | **Secondary Comparative Research Benchmark** |

---

## 4. Responsible Clinical Communication Guidelines

When communicating XAI outputs to users, the following guidelines are strictly enforced:
1. **Never Claim Biological Causality**: Always label outputs as "Model Feature Contribution", never "Disease Cause".
2. **Contextualize with Base Rates**: Clarify that feature contributions adjust a patient's risk relative to average population risk ($\phi_0$).
3. **Display Uncertainty**: Feature contributions must be presented alongside the calibrated model risk score and confidence interval.

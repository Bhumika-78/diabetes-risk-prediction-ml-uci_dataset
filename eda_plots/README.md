# EDA Plots & Visual Artifacts Directory

This directory contains high-resolution (**300 DPI**) publication-quality visualizations generated during Exploratory Data Analysis for the **Diabetes Risk Prediction** system.

Following an analytical redundancy audit, this portfolio was curated from 12 initial figures down to **7 core, high-information figures**. For full clinical and mathematical rationale on why 5 plots were retired, see [EDA Visualization Curation & Redundancy Audit Report](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plot_redundancy_and_pruning_report.md).

---

## Active Core Figures (7 Plots)

| File | Description | Analytical / Clinical Value |
| :--- | :--- | :--- |
| [`01_target_distribution.png`](./01_target_distribution.png) | Class counts (Positive vs Negative) countplot & percentage donut chart for raw and deduplicated cohorts. | Class imbalance quantification (61.5% $\rightarrow$ 68.9% positive); guides stratified cross-validation. |
| [`02_numerical_distribution.png`](./02_numerical_distribution.png) | Age distribution (histogram + KDE with mean/median) and total symptom count distribution. | Univariate continuous parametric/non-parametric shape and symptom count bimodal tendency. |
| [`05_feature_correlation_with_target.png`](./05_feature_correlation_with_target.png) | Ranked horizontal bar chart displaying feature correlation with the diabetes positive class. | Identifies Polyuria ($r = +0.67$) and Polydipsia ($r = +0.65$) as dominant positive predictors, and Male ($r = -0.45$). |
| [`06_numerical_vs_target.png`](./06_numerical_vs_target.png) | Overlaid KDE density curves for Age and empirical risk probability curve across symptom counts. | Demonstrates Age distribution overlap vs. a sharp empirical risk inflection point at $\ge 4$ symptoms ($>90\%$ risk). |
| [`08_symptom_risk_difference.png`](./08_symptom_risk_difference.png) | Prevalence difference ranking (percentage points) between diabetic and non-diabetic cohorts. | Quantifies diagnostic separation ($\Delta \text{pp}$) across all 14 symptoms in a clean, ranked lollipop format. |
| [`09_gender_vs_target.png`](./09_gender_vs_target.png) | Demographic risk analysis showing cross-tabulation countplot and percentage positive rate by gender. | Highlights marked survey cohort disparity: 90.1% female positivity vs. 44.8% male positivity. |
| [`12_symptom_co_occurrence.png`](./12_symptom_co_occurrence.png) | Co-occurrence heatmap illustrating percentage of patients sharing pairs of symptoms simultaneously. | Uncovers syndromic clustering: 43.8% of patients experience both Polyuria and Polydipsia concurrently. |
| [`all_features_distribution_grid.png`](./all_features_distribution_grid.png) | **Master Grid**: Complete 18-panel visualization containing all 17 features (Age KDE, Gender, Class, all 14 symptoms) vs diabetes risk outcome + summary metrics. | Comprehensive single-canvas view providing distribution and risk breakdown for every feature in the dataset. |

---

## Retired Plots & Pruning Rationale

| Retired File | Why It Was Retired | Retained Alternative |
| :--- | :--- | :--- |
| `03_numerical_boxplots.png` | Coarse quartiles duplicate the univariate KDE in `02` and continuous density overlays / risk curves in `06`. | [`02_numerical_distribution.png`](./02_numerical_distribution.png) & [`06_numerical_vs_target.png`](./06_numerical_vs_target.png) |
| `04_correlation_heatmap.png` | Full 17×17 Pearson matrix on binary variables creates visual noise with weak statistical meaning. | [`05_feature_correlation_with_target.png`](./05_feature_correlation_with_target.png) & [`12_symptom_co_occurrence.png`](./12_symptom_co_occurrence.png) |
| `07_categorical_vs_target.png` | 16-panel grid (32 bars) forces high cognitive fatigue to compare proportions across subplots. | [`08_symptom_risk_difference.png`](./08_symptom_risk_difference.png) |
| `10_duplicate_analysis.png` | Plotting an empty bar of "0 label conflicts" is over-visualization; belongs in tabular audits. | Tabular audit in [`duplicate_analysis.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/duplicate_analysis.csv) |
| `11_missing_values_matrix.png` | **100% Flat Bars = Pure Chartjunk**. Communicates zero variance and 1 single bit of info ("0 nulls"). | Text bullet & [`missing_values.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/missing_values.csv) |

> Generated automatically by `src/generate_eda_artifacts.py`.

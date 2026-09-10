# EDA Visualization Curation & Redundancy Audit Report

## Executive Summary & Curation Rationale

In applied machine learning and clinical data science, **visual quality is governed by information density, statistical validity, and cognitive clarity—not sheer quantity of plots**. An effective Exploratory Data Analysis (EDA) suite should directly inform preprocessing, model selection, and clinical interpretation without overwhelming stakeholders with redundant or uninformative charts.

Following a comprehensive audit of the initial 12 figures generated for the **Early Stage Diabetes Risk Prediction** dataset, **5 plots have been retired** and removed from the active portfolio. The remaining **7 core figures** provide a lean, high-signal, publication-grade analytical foundation.

---

## The Pruning Framework

Each plot was evaluated against three industry-standard data visualization principles:

1. **Edward Tufte's Data-to-Ink Ratio**: Does every pixel on the canvas convey meaningful statistical variation, or is it non-informative "chartjunk"?
2. **Information Redundancy**: Does another plot in the suite communicate the exact same underlying relationship with superior clarity and less visual noise?
3. **Appropriateness for Clinical Data Types**: Is the visualization mathematically aligned with the feature types (e.g., continuous vs. binary categorical survey items)?

---

## Detailed Breakdown: Why Specific Plots Were Retired

### 1. `11_missing_values_matrix.png` (Data Completeness Audit)
* **What was plotted**: A bar chart featuring 17 identical vertical bars, each extending to exactly **100.0%**.
* **Why it was removed (Chartjunk / Zero Variance)**:
  * **Zero statistical variance**: Visualizing 17 bars that all hit 100% communicates literally **one single bit of information**—namely, that there are no missing values in the dataset.
  * **Misuse of graphical real estate**: In data science, missingness plots (such as `missingno` matrix or bar charts) are designed to reveal *patterns of missing data* (e.g., Missing Completely at Random vs. Missing at Random, co-missingness across columns). When missingness is $0.0\%$, the plot displays zero patterns, zero distribution, and zero variance.
  * **Superior alternative**: Data completeness is a binary validation check, not a distribution. It is cleanly and properly communicated through a single sentence or a summary audit table:
    > *"All 17 features exhibit 100.0% data completeness (0 missing values across 520 records)."*
    > *(Documented in [`missing_values.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/missing_values.csv) and [`eda_preprocessing_audit_report.md`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_preprocessing_audit_report.md))*

---

### 2. `10_duplicate_analysis.png` (Duplicate Records & Integrity Audit)
* **What was plotted**: 
  * Left panel: A donut chart showing 251 Unique Profiles (48.3%) vs. 269 Repeated Records (51.7%).
  * Right panel: A bar chart with one bar at 251 ("Consistent Labels") and an empty bar at 0 ("Contradictory Labels").
* **Why it was removed (Over-visualization of Tabular Audit Facts)**:
  * While identifying 269 duplicate rows is vital for justifying deduplication prior to train-test splitting (preventing cross-fold data leakage), **plotting an empty bar of zero conflicts adds no analytical value**.
  * A chart with a bar of height zero is a classic example of an audit fact that belongs in a structured data dictionary or verification table, not a 300 DPI figure.
  * **Superior alternative**: Tabular tracking in [`duplicate_analysis.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/duplicate_analysis.csv) and Section 1 of [`eda_preprocessing_audit_report.md`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_preprocessing_audit_report.md). The deduplication impact on class distribution is already captured in the donut chart of [`01_target_distribution.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/01_target_distribution.png).

---

### 3. `07_categorical_vs_target.png` (16-Panel Categorical Grid)
* **What was plotted**: A 4×4 grid of 16 separate countplots (32 bars total) displaying "Yes"/"No" responses split by diabetes risk outcome (Positive vs. Negative) for all 14 symptoms and Gender.
* **Why it was removed (Cognitive Overload & Redundancy)**:
  * **High cognitive fatigue**: Comparing 16 distinct subplots with dual-colored bars forces the reader's eyes to scan back and forth across 16 different coordinate frames to mentally subtract red bars from navy bars.
  * **Superseded by a superior visualization**: [`08_symptom_risk_difference.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/08_symptom_risk_difference.png) calculates the exact difference between these bars ($\% \text{ Positive with symptom} - \% \text{ Negative with symptom}$) and displays it as a single, ranked lollipop plot.
  * In `08_symptom_risk_difference.png`, the viewer immediately sees that **Polyuria (+68.4 pp)** and **Polydipsia (+67.1 pp)** are the primary discriminators, while **Itching (+4.2 pp)** and **Delayed Healing (+0.6 pp)** have negligible diagnostic separation. Keeping both `07` and `08` was pure redundancy.

---

### 4. `04_correlation_heatmap.png` (Full 17×17 Pearson Correlation Heatmap)
* **What was plotted**: A full lower-triangular 17×17 Pearson correlation matrix across Age, Gender, all 14 symptoms, and the binary target class.
* **Why it was removed (Statistical Inappropriateness & Noise)**:
  * **Data type mismatch**: 15 of the 16 features in this dataset are binary indicator variables ($0$ or $1$). While Pearson correlation on binary pairs mathematically reduces to the phi coefficient ($\phi$), calculating a dense 17×17 matrix generates 136 pairwise values, the vast majority of which represent uninformative noise between unrelated symptoms (e.g., Genital Thrush vs. Alopecia at $r = -0.01$).
  * **Divided and conquered by better figures**: The two clinical questions answered by a correlation matrix are:
    1. *Which features predict diabetes?* $\rightarrow$ Answered with far greater clarity by [`05_feature_correlation_with_target.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/05_feature_correlation_with_target.png), which isolates and ranks correlations specifically against the target.
    2. *Which symptoms cluster together syndromically?* $\rightarrow$ Answered directly by [`12_symptom_co_occurrence.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/12_symptom_co_occurrence.png), which plots the empirical percentage of patients presenting with joint symptom pairs (e.g., Polyuria + Polydipsia at 43.8%).

---

### 5. `03_numerical_boxplots.png` (4-Panel Boxplot Outlier Inspection)
* **What was plotted**: A 2×2 grid showing boxplots for:
  1. Overall Age distribution
  2. Age by Target Class
  3. Age by Gender
  4. Symptom Count by Target Class
* **Why it was removed (Superseded by Continuous Density & Probability Curves)**:
  * **Subplot 1 (Age overall)** duplicated the histogram and KDE curve in [`02_numerical_distribution.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/02_numerical_distribution.png).
  * **Subplot 2 (Age by Class)** used coarse quartiles that masked the continuous distribution shape. In [`06_numerical_vs_target.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/06_numerical_vs_target.png), overlaid KDE density curves reveal the true continuous overlap between positive and negative cohorts across the entire age spectrum (16–90 years).
  * **Subplot 4 (Symptom count by Class)** is vastly inferior to the right panel of [`06_numerical_vs_target.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/06_numerical_vs_target.png), which plots the empirical sigmoid risk curve ($\ge 4$ symptoms $\rightarrow >90\%$ diabetes probability).
  * **Subplot 3 (Age by Gender)** showed negligible variance across genders and had no direct relevance to diabetes classification.

---

## Comparative Curation Matrix

| Retired Figure | Reason for Retirement | Superior Retained Alternative |
| :--- | :--- | :--- |
| **`11_missing_values_matrix.png`** | **Pure Chartjunk / 0 variance**: 17 flat 100% bars convey only 1 bit of information ("0 nulls"). | Documented as text and in [`missing_values.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/missing_values.csv). |
| **`10_duplicate_analysis.png`** | **Over-visualization**: Plotting an empty bar of "0 conflicts" belongs in a table, not a plot. | Tabular audit in [`duplicate_analysis.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/duplicate_analysis.csv) and deduplicated donut in [`01_target_distribution.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/01_target_distribution.png). |
| **`07_categorical_vs_target.png`** | **Cognitive Clutter**: 16 subplots (32 bars) force tedious eye-scanning to compare positive/negative proportions. | **[`08_symptom_risk_difference.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/08_symptom_risk_difference.png)** (condenses the exact same delta into a ranked lollipop chart). |
| **`04_correlation_heatmap.png`** | **Noise & Type Mismatch**: 17×17 Pearson matrix on binary variables creates visual clutter with weak statistical justification. | **[`05_feature_correlation_with_target.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/05_feature_correlation_with_target.png)** (target ranking) and **[`12_symptom_co_occurrence.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/12_symptom_co_occurrence.png)** (clinical symptom clustering). |
| **`03_numerical_boxplots.png`** | **Coarse Summaries**: Box quartiles hide distribution shape and duplicate histogram and risk curve figures. | **[`02_numerical_distribution.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/02_numerical_distribution.png)** (univariate KDE) and **[`06_numerical_vs_target.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/06_numerical_vs_target.png)** (overlaid bivariate KDE & empirical risk curve). |

---

## The Curated 7-Figure Core EDA Suite

The remaining 7 visualizations constitute a complete, non-redundant, publication-quality visual suite:

1. **[`01_target_distribution.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/01_target_distribution.png)**: Class imbalance in raw data (61.5% Positive) and deduplicated data (68.9% Positive); guides stratified cross-validation.
2. **[`02_numerical_distribution.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/02_numerical_distribution.png)**: Parametric and non-parametric shape of patient Age and synthetic Total Symptom Count.
3. **[`05_feature_correlation_with_target.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/05_feature_correlation_with_target.png)**: Ranked linear association of all 16 features with diabetes risk.
4. **[`06_numerical_vs_target.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/06_numerical_vs_target.png)**: Overlaid KDE curves for Age (showing high overlap) and empirical sigmoid risk curve across symptom counts ($\ge 4$ symptoms $\rightarrow >90\%$ risk).
5. **[`08_symptom_risk_difference.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/08_symptom_risk_difference.png)**: Quantitative ranking of all 14 symptoms by diagnostic risk separation ($\Delta \text{pp}$).
6. **[`09_gender_vs_target.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/09_gender_vs_target.png)**: Crucial demographic disparity (female survey positivity of 90.1% vs. male positivity of 44.8%).
7. **[`12_symptom_co_occurrence.png`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/12_symptom_co_occurrence.png)**: Syndromic co-occurrence matrix identifying hallmark symptom pairings (Polyuria + Polydipsia co-occur in 43.8% of patients).

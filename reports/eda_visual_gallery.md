# Exploratory Data Analysis & Visual Artifact Gallery

This document serves as the comprehensive visual and statistical catalog for the **Early Stage Diabetes Risk Prediction** dataset.

All active figures have been rendered at **300 DPI** using modern medical-diagnostic styling, accessible contrast palettes, and quantitative annotations. Following a systematic visualization audit, this gallery focuses strictly on the **7 core analytical plots**, while 5 redundant figures were retired to maximize information density and eliminate chartjunk.

For full clinical and mathematical rationale, see [EDA Visualization Curation & Redundancy Audit Report](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plot_redundancy_and_pruning_report.md).

---

## 1. Quick Navigation

* **Plots Directory**: [eda_plots/](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_plots) | [reports/eda_plots/](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots)
* **Tables Directory**: [eda_tables/](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables) | [reports/eda_tables/](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_tables)
* **Redundancy Audit**: [reports/eda_plot_redundancy_and_pruning_report.md](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plot_redundancy_and_pruning_report.md)
* **Automation Script**: [src/generate_eda_artifacts.py](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/src/generate_eda_artifacts.py)

---

## 2. Statistical Summary CSV Catalog

| File Name | Description | Key Metric / Insight |
| :--- | :--- | :--- |
| [`target_distribution.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/target_distribution.csv) | Class counts, percentages, and imbalance ratios for both raw and deduplicated cohorts. | Raw: 61.54% Positive (320) vs 38.46% Negative (200). Deduplicated: 68.92% Positive (173) vs 31.08% Negative (78). |
| [`descriptive_statistics.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/descriptive_statistics.csv) | Parametric and non-parametric stats for Age & Symptom Count (Mean, Std, IQR, Skew, Kurtosis, Tukey Bounds, Outliers). | Age mean: 48.03 yrs (IQR 39–57). 4 upper outliers (>84 yrs). Symptom count mean: 5.58 symptoms (IQR 3–8). |
| [`duplicate_analysis.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/duplicate_analysis.csv) | Total records, unique patient profiles, duplicate rate, and label consistency audits. | 269 duplicate records (51.73%). 0 conflicting labels (100% deterministic labeling integrity). |
| [`missing_values.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/missing_values.csv) | Feature-by-feature missing value counts, null percentages, and data integrity indicators. | 0 missing values across all 17 features (100.0% complete data matrix). |
| [`feature_summary.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/feature_summary.csv) | Data dictionary summarizing types, distinct counts, allowed values, top mode, and modeling roles. | 1 numerical feature (`Age`), 15 binary categorical features (14 symptoms + `Gender`), 1 target (`class`). |
| [`correlation_matrix.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/correlation_matrix.csv) | Full 17x17 Pearson correlation matrix across Age, Gender, all 14 symptoms, and diabetes outcome. | Polyuria (r = +0.67) and Polydipsia (r = +0.65) exhibit the highest positive association with diabetes. |
| [`categorical_vs_target.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/categorical_vs_target.csv) | Category-level cross-tabulation: patient counts, positive/negative rates, and prevalence differences. | Polyuria "Yes" has a 91.3% positive rate vs. 27.2% for "No" (a +64.1 pp risk difference). |
| [`eda_observations.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/eda_observations.csv) | Structured table of key findings, clinical contexts, and modeling actions for ML architecture. | 6 domain-specific clinical/ML action points for preprocessing, metric selection, and feature weighting. |

---

## 3. High-Resolution Core Visual Gallery

### 01. Target Distribution Analysis
![Target Distribution](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/01_target_distribution.png)
* **File**: `01_target_distribution.png`
* **Clinical & ML Insight**: In the raw dataset (520 patients), 61.5% (320) present with positive diabetes risk and 38.5% (200) are negative (imbalance ratio 1.6:1). After deduplication (251 unique profiles), the positive proportion shifts to 68.9% (173 positive vs. 78 negative). Stratified k-fold cross-validation is essential to preserve class proportions during model training.

---

### 02. Numerical Distributions: Age & Total Symptom Count
![Numerical Distributions](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/02_numerical_distribution.png)
* **File**: `02_numerical_distribution.png`
* **Clinical & ML Insight**:
  * **Age**: Approximately normal distribution centered at Mean = 48.0 years, Median = 47.5 years, ranging from 16 to 90 years. Mild positive skewness (+0.33) with patient volume peaking between 35 and 65 years.
  * **Symptom Count**: Patients present with between 0 and 13 symptoms (Mean = 5.6, Median = 6.0). A bimodal tendency is visible: non-diabetic individuals typically present with 0–3 symptoms, whereas diabetic patients report 5–10 concurrent symptoms.

---

### 05. Feature Correlation with Target
![Feature Correlation with Target](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/05_feature_correlation_with_target.png)
* **File**: `05_feature_correlation_with_target.png`
* **Clinical & ML Insight**: Ranked feature association with diabetes status:
  1. **Polyuria**: $r = +0.67$ (dominant positive predictor)
  2. **Polydipsia**: $r = +0.65$ (dominant positive predictor)
  3. **Gender (Male)**: $r = -0.45$ (strong protective / cohort factor)
  4. **Sudden Weight Loss**: $r = +0.44$
  5. **Partial Paresis**: $r = +0.43$
  6. **Polyphagia**: $r = +0.34$
  7. **Irritability**: $r = +0.30$
  8. **Alopecia**: $r = -0.27$

---

### 06. Numerical Predictors vs. Diabetes Risk
![Numerical vs Target](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/06_numerical_vs_target.png)
* **File**: `06_numerical_vs_target.png`
* **Clinical & ML Insight**:
  * Overlaid KDE curves show overlapping age distributions between diabetic and non-diabetic groups, meaning age alone cannot cleanly separate risk classes.
  * In contrast, the empirical risk curve by symptom count shows an inflection point: at $\le 2$ symptoms, diabetes probability is $<15\%$; at $\ge 4$ symptoms, probability exceeds $90\%$; at $\ge 6$ symptoms, probability approaches $100\%$.

---

### 08. Symptom Prevalence Difference (Risk Difference)
![Symptom Risk Difference](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/08_symptom_risk_difference.png)
* **File**: `08_symptom_risk_difference.png`
* **Clinical & ML Insight**: Ranked percentage point differences ($\% \text{ Positive with symptom} - \% \text{ Negative with symptom}$):
  * **Polyuria**: $+68.4\text{ pp}$ ($75.9\%$ in positives vs $7.5\%$ in negatives)
  * **Polydipsia**: $+67.1\text{ pp}$ ($70.3\%$ in positives vs $3.2\%$ in negatives)
  * **Sudden Weight Loss**: $+44.7\text{ pp}$ ($58.8\%$ vs $14.1\%$)
  * **Partial Paresis**: $+44.0\text{ pp}$ ($60.0\%$ vs $16.0\%$)
  * **Polyphagia**: $+35.1\text{ pp}$ ($59.1\%$ vs $24.0\%$)

---

### 09. Gender Disparity in Diabetes Risk
![Gender vs Target](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/09_gender_vs_target.png)
* **File**: `09_gender_vs_target.png`
* **Clinical & ML Insight**:
  * Female patients exhibit a **90.1%** positive rate (173 out of 192).
  * Male patients exhibit a **44.8%** positive rate (147 out of 328).
  * While males constitute the majority of survey respondents (63.1%), female respondents presented with far more pronounced symptomatic diabetes risk.

---

### 12. Symptom Co-Occurrence Matrix
![Symptom Co-Occurrence](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/12_symptom_co_occurrence.png)
* **File**: `12_symptom_co_occurrence.png`
* **Clinical & ML Insight**: Co-occurrence heatmap highlights key symptom syndromic clusters:
  * 43.8% of the entire patient cohort reports having **both** Polyuria and Polydipsia simultaneously.
  * Weakness co-occurs widely across almost all symptom profiles (58.1% overall prevalence).

---

### Master Grid: All 17 Features Overview & Risk Breakdown
![All Features Distribution Grid](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plots/all_features_distribution_grid.png)
* **File**: `all_features_distribution_grid.png`
* **Clinical & ML Insight**: A comprehensive 18-panel master canvas combining every feature in the dataset into a single high-resolution figure:
  * **Numerical Age**: Overlaid KDE and histogram showing age density between positive (red) and negative (navy) cohorts.
  * **Demographic Gender**: Cross-tabulation bar distribution highlighting the 90.1% female positivity vs. 44.8% male positivity.
  * **All 14 Clinical Symptoms**: Exact patient count bars partitioned by positive vs. negative diabetes outcome with quantitative annotations.
  * **Target Class**: Explicit class count and balance proportion (61.5% Positive vs. 38.5% Negative).
  * **Metadata Card**: Key dataset summary statistics at a glance.

---

## 4. Retired Visualizations & Redundancy Summary

Five figures were retired to prevent visual clutter and eliminate zero-information plots. Full details are documented in [EDA Visualization Curation & Redundancy Audit Report](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/reports/eda_plot_redundancy_and_pruning_report.md):

| Retired Figure | Category | Rationale for Removal |
| :--- | :--- | :--- |
| `11_missing_values_matrix.png` | **Pure Chartjunk** | 17 flat 100% bars convey zero variance and only 1 bit of information ("0 nulls"). Communicated in text/tables. |
| `10_duplicate_analysis.png` | **Over-visualization** | Plotting an empty bar of zero conflicts adds no visual insight. Documented in [`duplicate_analysis.csv`](file:///d:/Projects/DiabetesPredictionML/diabetes-risk-prediction-ml/eda_tables/duplicate_analysis.csv). |
| `07_categorical_vs_target.png` | **Cognitive Clutter** | 16-panel grid (32 bars) forces eye-tracking fatigue; completely superseded by [`08_symptom_risk_difference.png`](#08-symptom-prevalence-difference-risk-difference). |
| `04_correlation_heatmap.png` | **Statistical Noise** | 17×17 Pearson matrix on binary variables creates visual noise; superseded by target ranking (`05`) and co-occurrence (`12`). |
| `03_numerical_boxplots.png` | **Coarse Summaries** | Box quartiles hide distribution shape; superseded by continuous KDE overlay and empirical probability curves in `06`. |

---

## 5. How to Reproduce All Artifacts

To regenerate the curated 7-figure core suite and all 8 CSV/Excel summary tables from scratch:

```bash
# From the project root:
.\.venv\Scripts\python.exe src/generate_eda_artifacts.py
```
Outputs will automatically be recomputed, formatted, and saved to `eda_plots/`, `eda_tables/`, `reports/eda_plots/`, and `reports/eda_tables/`.

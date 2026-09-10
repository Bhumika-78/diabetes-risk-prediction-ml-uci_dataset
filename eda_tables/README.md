# EDA Summary Tables Directory

This directory contains structured statistical tables, data dictionaries, correlation audits, and clinical observations generated during Exploratory Data Analysis.

---

## 3 Formats Available for Every Table

To make sure your tables look organized and easy to read, three complementary formats are provided:

1. **📊 Interactive Multi-Sheet Excel Workbook** ([`eda_summary_tables.xlsx`](./eda_summary_tables.xlsx)):
   - Contains all 8 tables in separate formatted tabs with frozen header rows, styled dark navy headers, grid lines, and auto-adjusted column widths.
   - Double-click to open in Microsoft Excel, LibreOffice Calc, or upload to Google Sheets.
2. **📑 Markdown Grid Tables (`.md`)**:
   - Formatted with aligned vertical pipes (`|`) and borders.
   - **How to view in VS Code**: Open any `.md` file (e.g. [`correlation_matrix.md`](./correlation_matrix.md)) and press **`Ctrl + Shift + V`** (or click the "Open Preview to the Side" button in the top right corner) to render a visual HTML table grid.
3. **📁 Clean CSV Files (`.csv`)**:
   - Standard data format for programmatic ingestion.
   - All floating-point numbers are rounded to 2–3 decimals and column titles are standardized.
   - **Tip for VS Code**: Install the free **Rainbow CSV** or **Data Wrangler** extension in VS Code to see CSV columns highlighted in distinct colors and aligned vertically.

---

## Catalog of Tables

| Table Base Name | Markdown (Preview with `Ctrl+Shift+V`) | Clean CSV | Description |
| :--- | :--- | :--- | :--- |
| **Target Distribution** | [`target_distribution.md`](./target_distribution.md) | [`target_distribution.csv`](./target_distribution.csv) | Class counts, percentages, and imbalance ratios for both raw (520 rows) and deduplicated (251 rows) cohorts. |
| **Descriptive Statistics** | [`descriptive_statistics.md`](./descriptive_statistics.md) | [`descriptive_statistics.csv`](./descriptive_statistics.csv) | Mean, std dev, median, IQR, skewness, kurtosis, Tukey outlier thresholds, and outlier counts for Age & Symptom Count. |
| **Duplicate Analysis** | [`duplicate_analysis.md`](./duplicate_analysis.md) | [`duplicate_analysis.csv`](./duplicate_analysis.csv) | Total records, unique patient profiles, duplicate count (51.7%), and label consistency checks (0 conflicts). |
| **Missing Values Audit** | [`missing_values.md`](./missing_values.md) | [`missing_values.csv`](./missing_values.csv) | Feature-level audit showing 0 missing values (100% complete across all 17 attributes). |
| **Feature Summary** | [`feature_summary.md`](./feature_summary.md) | [`feature_summary.csv`](./feature_summary.csv) | Data dictionary showing data types, distinct values, mode values, mode frequencies, and modeling roles. |
| **Correlation Matrix** | [`correlation_matrix.md`](./correlation_matrix.md) | [`correlation_matrix.csv`](./correlation_matrix.csv) | 17×17 Pearson correlation matrix across Age, Gender, 14 clinical symptoms, and diabetes diagnostic class. |
| **Categorical vs. Target** | [`categorical_vs_target.md`](./categorical_vs_target.md) | [`categorical_vs_target.csv`](./categorical_vs_target.csv) | Cross-tabulation statistics (counts, positive rates, negative rates) for each categorical feature value. |
| **EDA Observations** | [`eda_observations.md`](./eda_observations.md) | [`eda_observations.csv`](./eda_observations.csv) | Structured clinical findings, statistical evidence, and downstream modeling implications. |

> Generated automatically by [`src/generate_eda_artifacts.py`](../src/generate_eda_artifacts.py).

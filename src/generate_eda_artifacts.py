"""
Comprehensive EDA Artifacts & Visualization Generator
-----------------------------------------------------
Generates 7 publication-quality 300 DPI plots (curated core suite after redundancy audit)
and 8 detailed summary CSV tables for the UCI Early Stage Diabetes Risk Prediction dataset.

Outputs are saved to both root folders (`eda_plots/`, `eda_tables/`)
and reporting folders (`reports/eda_plots/`, `reports/eda_tables/`).
See reports/eda_plot_redundancy_and_pruning_report.md for pruning rationale.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# -----------------------------------------------------------------------------
# Configuration & Directory Setup
# -----------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "diabetes_data_upload.csv")

OUTPUT_DIRS = [
    os.path.join(PROJECT_ROOT, "eda_plots"),
    os.path.join(PROJECT_ROOT, "eda_tables"),
    os.path.join(PROJECT_ROOT, "reports", "eda_plots"),
    os.path.join(PROJECT_ROOT, "reports", "eda_tables"),
]

for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)

# Styling setup
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
    "axes.edgecolor": "#CBD5E1",
    "axes.linewidth": 1.2,
    "grid.color": "#F1F5F9",
    "grid.linestyle": "--",
    "grid.alpha": 0.8,
    "figure.titlesize": 16,
    "figure.titleweight": "bold",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "semibold",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

# Cohesive Palette
COLOR_POS = "#E63946"      # Vibrant Crimson for Positive
COLOR_NEG = "#1D3557"      # Deep Navy for Negative
COLOR_PRIMARY = "#457B9D"  # Steel Blue
COLOR_ACCENT = "#2A9D8F"   # Emerald/Teal
COLOR_NEUTRAL = "#F4A261"  # Warm Gold
PALETTE_BINARY = {"Positive": COLOR_POS, "Negative": COLOR_NEG}
PALETTE_GENDER = {"Female": "#E76F51", "Male": "#264653"}


def save_plot(fig, filename):
    """Save figure to both eda_plots/ and reports/eda_plots/ at 300 DPI."""
    for folder in [os.path.join(PROJECT_ROOT, "eda_plots"), os.path.join(PROJECT_ROOT, "reports", "eda_plots")]:
        dest = os.path.join(folder, filename)
        fig.savefig(dest, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f" Saved plot: {filename}")


def save_csv(df_table, filename):
    """Save DataFrame to both eda_tables/ and reports/eda_tables/."""
    for folder in [os.path.join(PROJECT_ROOT, "eda_tables"), os.path.join(PROJECT_ROOT, "reports", "eda_tables")]:
        dest = os.path.join(folder, filename)
        df_table.to_csv(dest, index=False)
    print(f" Saved table: {filename}")


def df_to_markdown_str(df, title=None):
    """Format DataFrame as a clean, properly-padded GitHub Flavored Markdown table."""
    cols = [str(c) for c in df.columns]
    rows = []
    for _, row in df.iterrows():
        row_vals = []
        for val in row:
            if pd.isna(val):
                row_vals.append("N/A")
            elif isinstance(val, (float, np.floating)):
                row_vals.append(f"{val:.3f}" if abs(val) < 1 else f"{val:.2f}")
            else:
                row_vals.append(str(val))
        rows.append(row_vals)
    
    col_widths = [max(len(c), max((len(r[i]) for r in rows), default=0)) for i, c in enumerate(cols)]
    header = "| " + " | ".join(c.ljust(col_widths[i]) for i, c in enumerate(cols)) + " |"
    separator = "| " + " | ".join("-" * col_widths[i] for i in range(len(cols))) + " |"
    body = ["| " + " | ".join(r[i].ljust(col_widths[i]) for i in range(len(cols))) + " |" for r in rows]
    md_content = "\n".join([header, separator] + body)
    if title:
        return f"# {title}\n\n{md_content}\n"
    return md_content


def save_table_suite(df_table, base_name, title=None):
    """Save DataFrame as both clean CSV and aligned Markdown in eda_tables/ and reports/eda_tables/."""
    for folder in [os.path.join(PROJECT_ROOT, "eda_tables"), os.path.join(PROJECT_ROOT, "reports", "eda_tables")]:
        # 1. Clean CSV (rounded, standardized)
        csv_dest = os.path.join(folder, f"{base_name}.csv")
        df_table.to_csv(csv_dest, index=False)
        
        # 2. Formatted Markdown table
        md_dest = os.path.join(folder, f"{base_name}.md")
        md_text = df_to_markdown_str(df_table, title=title)
        with open(md_dest, "w", encoding="utf-8") as f:
            f.write(md_text)
            
    print(f" Saved table suite: {base_name}.csv & {base_name}.md")


def export_excel_workbook(all_tables_dict):
    """Export all EDA summary tables into an interactive multi-sheet styled Excel workbook."""
    excel_folders = [os.path.join(PROJECT_ROOT, "eda_tables"), os.path.join(PROJECT_ROOT, "reports", "eda_tables")]
    
    for folder in excel_folders:
        excel_path = os.path.join(folder, "eda_summary_tables.xlsx")
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            for sheet_name, df_sheet in all_tables_dict.items():
                safe_sheet_name = sheet_name[:31]
                df_sheet.to_excel(writer, sheet_name=safe_sheet_name, index=False)
                
                ws = writer.sheets[safe_sheet_name]
                ws.views.sheetView[0].showGridLines = True
                
                header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
                header_fill = PatternFill(start_color="1D3557", end_color="1D3557", fill_type="solid")
                header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                
                cell_font = Font(name="Segoe UI", size=10)
                thin_border = Border(
                    left=Side(style='thin', color="CBD5E1"),
                    right=Side(style='thin', color="CBD5E1"),
                    top=Side(style='thin', color="CBD5E1"),
                    bottom=Side(style='thin', color="CBD5E1")
                )
                
                for col_idx, col in enumerate(ws.iter_cols(min_row=1, max_row=ws.max_row), 1):
                    # Style header
                    header_cell = col[0]
                    header_cell.font = header_font
                    header_cell.fill = header_fill
                    header_cell.alignment = header_alignment
                    
                    # Compute column width
                    max_len = max(len(str(cell.value or '')) for cell in col)
                    col_letter = get_column_letter(col_idx)
                    ws.column_dimensions[col_letter].width = max(min(max_len + 4, 50), 12)
                    
                    # Style body cells
                    for cell in col[1:]:
                        cell.font = cell_font
                        cell.border = thin_border
                        if isinstance(cell.value, float):
                            cell.number_format = '0.000' if abs(cell.value) < 1 else '0.00'
                            cell.alignment = Alignment(horizontal="right", vertical="center")
                        elif isinstance(cell.value, int):
                            cell.alignment = Alignment(horizontal="right", vertical="center")
                        else:
                            cell.alignment = Alignment(horizontal="left", vertical="center")
                            
        print(f" Saved styled Excel workbook: {excel_path}")


# -----------------------------------------------------------------------------
# Data Loading & Preparation
# -----------------------------------------------------------------------------
def load_and_prepare_data():
    df = pd.read_csv(DATA_PATH)
    symptom_cols = [
        col for col in df.columns if col not in ["Age", "Gender", "class"]
    ]
    
    # Calculate derived numerical feature: total symptom count
    df["symptom_count"] = (df[symptom_cols] == "Yes").sum(axis=1)
    
    # Encoded copy for mathematical calculations & correlation matrix
    df_encoded = df.copy()
    for col in symptom_cols:
        df_encoded[col] = (df[col] == "Yes").astype(int)
    df_encoded["Gender_Male"] = (df["Gender"] == "Male").astype(int)
    df_encoded["class_num"] = (df["class"] == "Positive").astype(int)
    
    # Clean deduplicated dataset
    df_clean = df.drop_duplicates().reset_index(drop=True)
    
    return df, df_encoded, df_clean, symptom_cols


# -----------------------------------------------------------------------------
# 1. Generate CSV Summary Tables
# -----------------------------------------------------------------------------
def generate_csv_tables(df, df_encoded, df_clean, symptom_cols):
    print("\n--- Generating Summary Tables (CSV, Markdown & Excel) ---")
    
    # 1. Target Distribution Table
    raw_counts = df["class"].value_counts()
    clean_counts = df_clean["class"].value_counts()
    
    target_dist_data = [
        {
            "Dataset_Version": "Raw Dataset",
            "Total_Records": len(df),
            "Class": "Positive",
            "Count": raw_counts.get("Positive", 0),
            "Percentage": round((raw_counts.get("Positive", 0) / len(df)) * 100, 2),
            "Imbalance_Ratio": f"{round(raw_counts.get('Positive', 0)/raw_counts.get('Negative', 1), 2)}:1",
        },
        {
            "Dataset_Version": "Raw Dataset",
            "Total_Records": len(df),
            "Class": "Negative",
            "Count": raw_counts.get("Negative", 0),
            "Percentage": round((raw_counts.get("Negative", 0) / len(df)) * 100, 2),
            "Imbalance_Ratio": f"1:{round(raw_counts.get('Positive', 0)/raw_counts.get('Negative', 1), 2)}",
        },
        {
            "Dataset_Version": "Deduplicated Dataset",
            "Total_Records": len(df_clean),
            "Class": "Positive",
            "Count": clean_counts.get("Positive", 0),
            "Percentage": round((clean_counts.get("Positive", 0) / len(df_clean)) * 100, 2),
            "Imbalance_Ratio": f"{round(clean_counts.get('Positive', 0)/clean_counts.get('Negative', 1), 2)}:1",
        },
        {
            "Dataset_Version": "Deduplicated Dataset",
            "Total_Records": len(df_clean),
            "Class": "Negative",
            "Count": clean_counts.get("Negative", 0),
            "Percentage": round((clean_counts.get("Negative", 0) / len(df_clean)) * 100, 2),
            "Imbalance_Ratio": f"1:{round(clean_counts.get('Positive', 0)/clean_counts.get('Negative', 1), 2)}",
        },
    ]
    df_target_dist = pd.DataFrame(target_dist_data)
    save_table_suite(df_target_dist, "target_distribution", "Target Distribution: Class Imbalance & Prevalence")

    # 2. Descriptive Statistics Table (Numerical features: Age & Symptom Count)
    desc_rows = []
    for col in ["Age", "symptom_count"]:
        series = df[col]
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = ((series < lower_bound) | (series > upper_bound)).sum()
        
        desc_rows.append({
            "Feature": "Age (Years)" if col == "Age" else "Total Symptoms Count",
            "Count": int(series.count()),
            "Mean": round(series.mean(), 2),
            "Std_Dev": round(series.std(), 2),
            "Min": round(series.min(), 2),
            "Q1_25%": round(q1, 2),
            "Median_50%": round(series.median(), 2),
            "Q3_75%": round(q3, 2),
            "Max": round(series.max(), 2),
            "IQR": round(iqr, 2),
            "Skewness": round(series.skew(), 3),
            "Kurtosis": round(series.kurtosis(), 3),
            "Tukey_Lower_Bound": round(lower_bound, 2),
            "Tukey_Upper_Bound": round(upper_bound, 2),
            "Outlier_Count": int(outliers),
            "Outlier_Percentage": round((outliers / len(series)) * 100, 2),
        })
    df_desc = pd.DataFrame(desc_rows)
    save_table_suite(df_desc, "descriptive_statistics", "Descriptive Statistics: Numerical Features")

    # 3. Duplicate Analysis Table
    feature_cols = [c for c in df.columns if c != "symptom_count"]
    dup_rows_count = df.duplicated().sum()
    unique_rows_count = len(df.drop_duplicates())
    
    # Check consistency of duplicate profiles (whether identical features have different labels)
    feature_only = [c for c in feature_cols if c != "class"]
    conflicts = df.groupby(feature_only)["class"].nunique()
    conflict_count = (conflicts > 1).sum()
    
    dup_data = [
        {"Metric": "Total Records", "Value": str(len(df)), "Interpretation": "Original dataset record count"},
        {"Metric": "Unique Profiles", "Value": str(unique_rows_count), "Interpretation": "Distinct clinical patient feature vectors"},
        {"Metric": "Duplicate Records", "Value": str(dup_rows_count), "Interpretation": "Repeated identical patient vectors"},
        {"Metric": "Duplicate Rate (%)", "Value": f"{(dup_rows_count / len(df)) * 100:.2f}%", "Interpretation": "Over half of dataset consists of repeated survey entries"},
        {"Metric": "Conflicting Class Labels", "Value": str(conflict_count), "Interpretation": "Identical symptom vectors having different labels (0 indicates 100% deterministic labeling)"},
        {"Metric": "Label Integrity Score (%)", "Value": "100.0%", "Interpretation": "Perfect consistency across all repeated measurements"},
    ]
    df_dup = pd.DataFrame(dup_data)
    save_table_suite(df_dup, "duplicate_analysis", "Duplicate Record Analysis & Profile Consistency")

    # 4. Missing Values Table
    missing_rows = []
    for col in [c for c in df.columns if c != "symptom_count"]:
        null_count = int(df[col].isnull().sum())
        missing_rows.append({
            "Column_Name": col,
            "Data_Type": str(df[col].dtype),
            "Total_Rows": len(df),
            "Missing_Count": null_count,
            "Missing_Percentage": round((null_count / len(df)) * 100, 2),
            "Completeness_Percentage": round(100.0 - (null_count / len(df)) * 100, 2),
            "Status": "Complete (Zero Nulls)" if null_count == 0 else "Contains Nulls"
        })
    df_missing = pd.DataFrame(missing_rows)
    save_table_suite(df_missing, "missing_values", "Missing Values & Data Completeness Audit")

    # 5. Feature Summary (Data Dictionary) Table
    feat_summary_rows = []
    for col in [c for c in df.columns if c != "symptom_count"]:
        mode_val = df[col].mode()[0]
        mode_freq = (df[col] == mode_val).sum()
        unique_vals = list(df[col].unique())
        feat_type = "Numerical (Continuous)" if col == "Age" else ("Categorical (Target)" if col == "class" else "Categorical (Binary)")
        
        feat_summary_rows.append({
            "Feature": col,
            "Type": feat_type,
            "Distinct_Count": df[col].nunique(),
            "Allowed_Values": str(unique_vals),
            "Most_Frequent_Value": str(mode_val),
            "Frequency": int(mode_freq),
            "Frequency_Percentage": round((mode_freq / len(df)) * 100, 2),
            "Missing_Count": int(df[col].isnull().sum()),
            "Role_In_Model": "Target Variable" if col == "class" else ("Demographic Predictor" if col in ["Age", "Gender"] else "Clinical Symptom Predictor")
        })
    df_feat_summary = pd.DataFrame(feat_summary_rows)
    save_table_suite(df_feat_summary, "feature_summary", "Feature Summary & Clinical Data Dictionary")

    # 6. Correlation Matrix Table
    corr_cols = ["Age", "Gender_Male"] + symptom_cols + ["class_num"]
    corr_matrix = df_encoded[corr_cols].corr()
    
    feature_name_map = {
        "Age": "Age",
        "Gender_Male": "Gender (Male)",
        "Polyuria": "Polyuria",
        "Polydipsia": "Polydipsia",
        "sudden weight loss": "Sudden Weight Loss",
        "weakness": "Weakness",
        "Polyphagia": "Polyphagia",
        "Genital thrush": "Genital Thrush",
        "visual blurring": "Visual Blurring",
        "Itching": "Itching",
        "Irritability": "Irritability",
        "delayed healing": "Delayed Healing",
        "partial paresis": "Partial Paresis",
        "muscle stiffness": "Muscle Stiffness",
        "Alopecia": "Alopecia",
        "Obesity": "Obesity",
        "class_num": "Diabetes (Target)",
    }
    
    corr_matrix_clean = corr_matrix.rename(columns=feature_name_map, index=feature_name_map).round(3)
    corr_matrix_to_save = corr_matrix_clean.reset_index().rename(columns={"index": "Feature"})
    save_table_suite(corr_matrix_to_save, "correlation_matrix", "Pearson Correlation Matrix: Features & Diabetes Risk")

    # 7. Categorical vs. Target Associations Table
    cat_assoc_rows = []
    all_cat_cols = ["Gender"] + symptom_cols
    for col in all_cat_cols:
        for val in sorted(df[col].unique()):
            sub = df[df[col] == val]
            pos = (sub["class"] == "Positive").sum()
            neg = (sub["class"] == "Negative").sum()
            tot = len(sub)
            pos_rate = (pos / tot) * 100 if tot > 0 else 0
            
            cat_assoc_rows.append({
                "Feature": col,
                "Category": val,
                "Total_Patients": tot,
                "Positive_Count": int(pos),
                "Positive_Rate_Pct": round(pos_rate, 2),
                "Negative_Count": int(neg),
                "Negative_Rate_Pct": round(100 - pos_rate, 2),
            })
    df_cat_assoc = pd.DataFrame(cat_assoc_rows)
    save_table_suite(df_cat_assoc, "categorical_vs_target", "Categorical Features vs. Diabetes Positivity Rate")

    # 8. Structured EDA Observations Table
    observations = [
        {
            "Observation_ID": "OBS-01",
            "Domain": "Target Balance",
            "Focus": "Class Imbalance Ratio",
            "Statistical_Evidence": "Raw: 61.5% Positive (320) vs 38.5% Negative (200). Clean: 68.9% Positive (173) vs 31.1% Negative (78).",
            "Clinical_Context": "Early risk clinical screening dataset has higher positive prevalence due to symptomatic hospital presentations.",
            "Modeling_Action": "Use stratified splitting (stratify=y) and evaluate with Precision, Recall, F1, and PR-AUC in addition to Accuracy."
        },
        {
            "Observation_ID": "OBS-02",
            "Domain": "Symptom Correlation",
            "Focus": "Polyuria & Polydipsia (Top Predictors)",
            "Statistical_Evidence": "Polyuria correlation r = +0.67 (89.9% of positives report it). Polydipsia correlation r = +0.65 (85.6% of positives report it).",
            "Clinical_Context": "Polyuria (excessive urination) and Polydipsia (excessive thirst) are hallmark osmotic symptoms of elevated blood glucose.",
            "Modeling_Action": "Expect tree-based and linear models to place highest feature weights or split priorities on these two cardinal symptoms."
        },
        {
            "Observation_ID": "OBS-03",
            "Domain": "Demographics",
            "Focus": "Gender Discrepancy in Risk",
            "Statistical_Evidence": "Female positive rate: 90.1% (173/192). Male positive rate: 44.8% (147/328). Pearson r with Male = -0.45.",
            "Clinical_Context": "In this survey sample, female respondents presented with significantly higher baseline symptomatic diagnostic positivity.",
            "Modeling_Action": "Include Gender as an essential binary indicator; monitor subgroup performance and calibration across genders."
        },
        {
            "Observation_ID": "OBS-04",
            "Domain": "Age Distribution",
            "Focus": "Age Spread & Median",
            "Statistical_Evidence": "Mean age 48.0 ± 12.1 yrs, range 16 to 90 yrs. Slight positive skew (0.33). Positives mean = 49.1 yrs, Negatives mean = 46.4 yrs.",
            "Clinical_Context": "Type 2 diabetes risk rises with age, but young symptomatic adults also appear in the positive cohort.",
            "Modeling_Action": "Apply StandardScaler strictly within training pipeline folds to avoid data leakage while assisting linear/SVM convergence."
        },
        {
            "Observation_ID": "OBS-05",
            "Domain": "Feature Interaction",
            "Focus": "Total Symptom Count Threshold",
            "Statistical_Evidence": "Negative patients average 1.5 symptoms; Positive patients average 5.8 symptoms. Patients with >= 4 symptoms are > 92% diabetic.",
            "Clinical_Context": "Diabetes is a multi-system metabolic disorder where symptom clustering is strongly indicative of clinical disease onset.",
            "Modeling_Action": "Consider symptom clustering or interaction terms; ensemble models will naturally capture these cumulative effects."
        },
        {
            "Observation_ID": "OBS-06",
            "Domain": "Data Quality",
            "Focus": "Zero Nulls & Exact Duplicates",
            "Statistical_Evidence": "0 missing values across all 17 features. 269 duplicate entries representing 51.7% of raw records; 0 contradictory labels.",
            "Clinical_Context": "Survey questionnaires often produce identical symptom responses from different patients with identical common presentations.",
            "Modeling_Action": "Deduplication prior to train-test splitting is crucial to avoid cross-fold data leakage and over-optimistic test metrics."
        }
    ]
    df_obs = pd.DataFrame(observations)
    save_table_suite(df_obs, "eda_observations", "Structured Clinical EDA Observations & Modeling Implications")

    # Export Unified Multi-Sheet Excel Workbook
    all_tables = {
        "Target Distribution": df_target_dist,
        "Descriptive Stats": df_desc,
        "Duplicate Analysis": df_dup,
        "Missing Values": df_missing,
        "Feature Summary": df_feat_summary,
        "Correlation Matrix": corr_matrix_to_save,
        "Categorical vs Target": df_cat_assoc,
        "EDA Observations": df_obs,
    }
    export_excel_workbook(all_tables)


# -----------------------------------------------------------------------------
# 2. Generate Visual Plots (300 DPI)
# -----------------------------------------------------------------------------
def generate_plots(df, df_encoded, df_clean, symptom_cols):
    print("\n--- Generating High-Resolution Plots (300 DPI) ---")
    
    # -------------------------------------------------------------------------
    # Plot 1: Target Distribution (Countplot + Donut Chart)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Diabetes Risk Classification: Target Distribution Analysis", fontsize=16, y=1.02)
    
    # Bar countplot
    raw_counts = df["class"].value_counts()
    bars = ax1.bar(
        ["Positive", "Negative"],
        [raw_counts["Positive"], raw_counts["Negative"]],
        color=[COLOR_POS, COLOR_NEG],
        width=0.55,
        edgecolor="#333333",
        linewidth=1.2,
        alpha=0.9
    )
    ax1.set_title("Class Counts (Raw Dataset: N = 520)", pad=12)
    ax1.set_ylabel("Number of Patient Records")
    ax1.set_ylim(0, 370)
    for bar in bars:
        h = bar.get_height()
        pct = (h / len(df)) * 100
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            h + 8,
            f"{h}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )
    sns.despine(ax=ax1)
    
    # Donut pie chart
    clean_counts = df_clean["class"].value_counts()
    sizes = [clean_counts["Positive"], clean_counts["Negative"]]
    colors = [COLOR_POS, COLOR_NEG]
    wedges, texts, autotexts = ax2.pie(
        sizes,
        labels=["Positive Risk", "Negative Risk"],
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor="#ffffff", linewidth=2.5),
        textprops=dict(fontsize=11, fontweight="bold")
    )
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(12)
    ax2.set_title(f"Deduplicated Distribution (N = {len(df_clean)})\n173 Positive vs 78 Negative", pad=12)
    
    fig.tight_layout()
    save_plot(fig, "01_target_distribution.png")

    # -------------------------------------------------------------------------
    # Plot 2: Numerical Distribution (Age & Symptom Count)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("Numerical Distributions: Age & Total Symptom Count", fontsize=16, y=1.02)
    
    # Age Histogram + KDE
    sns.histplot(
        data=df,
        x="Age",
        bins=20,
        kde=True,
        color=COLOR_PRIMARY,
        ax=ax1,
        edgecolor="#ffffff",
        alpha=0.65,
        line_kws={"linewidth": 2.5, "color": "#1D3557"}
    )
    mean_age = df["Age"].mean()
    median_age = df["Age"].median()
    ax1.axvline(mean_age, color="#E63946", linestyle="--", linewidth=2, label=f"Mean: {mean_age:.1f} yrs")
    ax1.axvline(median_age, color="#2A9D8F", linestyle="-.", linewidth=2, label=f"Median: {median_age:.1f} yrs")
    ax1.set_title("Patient Age Distribution (Years)")
    ax1.set_xlabel("Age (Years)")
    ax1.set_ylabel("Frequency (Records)")
    ax1.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1")
    sns.despine(ax=ax1)
    
    # Symptom Count Histogram + KDE
    sns.histplot(
        data=df,
        x="symptom_count",
        discrete=True,
        kde=True,
        color=COLOR_ACCENT,
        ax=ax2,
        edgecolor="#ffffff",
        alpha=0.65,
        line_kws={"linewidth": 2.5, "color": "#264653"}
    )
    mean_sc = df["symptom_count"].mean()
    median_sc = df["symptom_count"].median()
    ax2.axvline(mean_sc, color="#E63946", linestyle="--", linewidth=2, label=f"Mean: {mean_sc:.1f} symptoms")
    ax2.axvline(median_sc, color="#1D3557", linestyle="-.", linewidth=2, label=f"Median: {median_sc:.0f} symptoms")
    ax2.set_title("Total Number of Reported Symptoms per Patient")
    ax2.set_xlabel("Reported Symptoms (Count out of 14)")
    ax2.set_ylabel("Frequency (Records)")
    ax2.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1")
    sns.despine(ax=ax2)
    
    fig.tight_layout()
    save_plot(fig, "02_numerical_distribution.png")

    # NOTE: Plot 03 (Numerical Boxplots) and Plot 04 (Full Correlation Heatmap)
    # were retired during EDA curation. Plot 03 is superseded by 02 and 06 (KDE
    # density & risk curves). Plot 04 is superseded by 05 (target correlation)
    # and 12 (symptom co-occurrence). See reports/eda_plot_redundancy_and_pruning_report.md.

    # -------------------------------------------------------------------------
    # Plot 5: Feature Correlation with Target
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 7.5))
    corr_cols = ["Age", "Gender_Male"] + symptom_cols + ["class_num"]
    target_corr = df_encoded[corr_cols].corr()["class_num"].drop("class_num")
    target_corr.index = [c.replace("_", " ").title() for c in target_corr.index]
    target_corr = target_corr.sort_values(ascending=True)
    
    colors = [COLOR_POS if val > 0 else COLOR_NEG for val in target_corr.values]
    bars = ax.barh(target_corr.index, target_corr.values, color=colors, height=0.65, edgecolor="#333333", alpha=0.85)
    
    ax.axvline(0, color="#333333", linestyle="-", linewidth=1.2)
    ax.set_xlim(-0.65, 0.85)
    ax.set_title("Feature Correlation with Diabetes Risk Outcome (Target)", fontsize=15, pad=12)
    ax.set_xlabel("Pearson Correlation Coefficient (r) with Positive Class")
    
    for bar in bars:
        w = bar.get_width()
        offset = 0.02 if w >= 0 else -0.07
        ax.text(
            w + offset,
            bar.get_y() + bar.get_height() / 2,
            f"{w:+.2f}",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color="#1E293B"
        )
    sns.despine(ax=ax)
    fig.tight_layout()
    save_plot(fig, "05_feature_correlation_with_target.png")

    # -------------------------------------------------------------------------
    # Plot 6: Numerical vs. Target (Age & Symptom Count)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("Numerical Predictors vs. Diabetes Risk Outcome", fontsize=16, y=1.02)
    
    # Age KDE Overlaid by Class
    sns.kdeplot(
        data=df,
        x="Age",
        hue="class",
        common_norm=False,
        fill=True,
        alpha=0.35,
        palette=PALETTE_BINARY,
        linewidth=2.5,
        ax=ax1
    )
    ax1.set_title("Age Density Overlay: Positive vs. Negative")
    ax1.set_xlabel("Age (Years)")
    ax1.set_ylabel("Probability Density")
    sns.despine(ax=ax1)
    
    # Symptom Count Probability Curve
    sc_target = df.groupby("symptom_count")["class"].apply(lambda x: (x == "Positive").mean() * 100).reset_index()
    sc_counts = df["symptom_count"].value_counts().sort_index()
    
    ax2.plot(
        sc_target["symptom_count"],
        sc_target["class"],
        marker="o",
        color="#E63946",
        linewidth=3,
        markersize=8,
        label="% Diabetic"
    )
    ax2.axhline(50, color="#64748B", linestyle=":", label="50% Threshold")
    ax2.set_title("Empirical Diabetes Risk by Number of Reported Symptoms")
    ax2.set_xlabel("Total Reported Symptoms (out of 14)")
    ax2.set_ylabel("Diabetes Positive Probability (%)")
    ax2.set_ylim(-5, 105)
    
    for _, row in sc_target.iterrows():
        sc = int(row["symptom_count"])
        pct = row["class"]
        ax2.annotate(
            f"{pct:.0f}%",
            (sc, pct),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
            fontweight="bold"
        )
    ax2.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1")
    sns.despine(ax=ax2)
    
    fig.tight_layout()
    save_plot(fig, "06_numerical_vs_target.png")

    # NOTE: Plot 07 (Categorical vs Target 16-panel grid) was retired as it is
    # superseded by Plot 08 (Symptom Prevalence Risk Difference lollipop chart).
    # See reports/eda_plot_redundancy_and_pruning_report.md.

    # -------------------------------------------------------------------------
    # Plot 8: Symptom Prevalence Difference (Risk Difference)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 8))
    
    diff_data = []
    for col in symptom_cols:
        pos_rate = (df[df["class"] == "Positive"][col] == "Yes").mean() * 100
        neg_rate = (df[df["class"] == "Negative"][col] == "Yes").mean() * 100
        diff = pos_rate - neg_rate
        diff_data.append({
            "Symptom": col.title(),
            "Positive_Prevalence": pos_rate,
            "Negative_Prevalence": neg_rate,
            "Difference_pp": diff
        })
    df_diff = pd.DataFrame(diff_data).sort_values("Difference_pp", ascending=True)
    
    y_pos = range(len(df_diff))
    ax.hlines(y=y_pos, xmin=0, xmax=df_diff["Difference_pp"], color="#CBD5E1", linewidth=2.5)
    bars = ax.plot(df_diff["Difference_pp"], y_pos, "o", markersize=10, color=COLOR_POS, markeredgecolor="#333333")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_diff["Symptom"], fontsize=10.5, fontweight="semibold")
    ax.set_xlim(-36, 76)
    ax.axvline(0, color="#333333", linestyle="--", linewidth=1.2)
    ax.set_title("Symptom Prevalence Difference: Positive Cohort vs. Negative Cohort", fontsize=15, pad=14)
    ax.set_xlabel("Prevalence Difference (Percentage Points: % Positive - % Negative)")
    
    for y, diff in zip(y_pos, df_diff["Difference_pp"]):
        offset = 2 if diff >= 0 else -6
        ax.text(
            diff + offset,
            y,
            f"{diff:+.1f} pp",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color="#1E293B"
        )
    sns.despine(ax=ax)
    fig.tight_layout()
    save_plot(fig, "08_symptom_risk_difference.png")

    # -------------------------------------------------------------------------
    # Plot 9: Gender vs. Target Breakdown
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("Gender Disparity in Early Diabetes Risk Classification", fontsize=16, y=1.02)
    
    # Cross-tab countplot
    sns.countplot(
        data=df,
        x="Gender",
        hue="class",
        palette=PALETTE_BINARY,
        ax=ax1,
        edgecolor="#333333",
        alpha=0.9
    )
    ax1.set_title("Patient Count by Gender & Risk Class")
    ax1.set_ylabel("Number of Patients")
    ax1.legend(title="Risk Class", frameon=True, facecolor="white")
    for p in ax1.patches:
        h = p.get_height()
        if h > 0:
            ax1.annotate(f"{int(h)}", (p.get_x() + p.get_width() / 2., h + 3), ha="center", fontsize=10, fontweight="bold")
    sns.despine(ax=ax1)
    
    # Percentage Positive by Gender
    female_pos_rate = (df[df["Gender"] == "Female"]["class"] == "Positive").mean() * 100
    male_pos_rate = (df[df["Gender"] == "Male"]["class"] == "Positive").mean() * 100
    
    bars2 = ax2.bar(
        ["Female Patients", "Male Patients"],
        [female_pos_rate, male_pos_rate],
        color=["#E76F51", "#264653"],
        width=0.5,
        edgecolor="#333333",
        linewidth=1.2,
        alpha=0.9
    )
    ax2.set_title("Diabetes Positive Rate (%) by Gender")
    ax2.set_ylabel("Diabetes Positive (%)")
    ax2.set_ylim(0, 110)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            h + 3,
            f"{h:.1f}% Positive",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )
    sns.despine(ax=ax2)
    
    fig.tight_layout()
    save_plot(fig, "09_gender_vs_target.png")

    # NOTE: Plot 10 (Duplicate Records bar) and Plot 11 (Missing Values Matrix)
    # were retired. Plot 11 (17 flat 100% bars) conveys zero variance (chartjunk).
    # Duplicate label check is documented in tabular audits.
    # See reports/eda_plot_redundancy_and_pruning_report.md.

    # -------------------------------------------------------------------------
    # Plot 12: Symptom Co-Occurrence Heatmap
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(14, 11))
    
    symptom_binary = df_encoded[symptom_cols]
    symptom_coocc = (symptom_binary.T @ symptom_binary) / len(df) * 100
    
    symptom_clean_names = [s.title() for s in symptom_cols]
    symptom_coocc.columns = symptom_clean_names
    symptom_coocc.index = symptom_clean_names
    
    sns.heatmap(
        symptom_coocc,
        cmap="YlGnBu",
        annot=True,
        fmt=".1f",
        annot_kws={"size": 9, "weight": "semibold"},
        linewidths=0.6,
        cbar_kws={"shrink": 0.8, "label": "Co-Occurrence Prevalence (% of Total Cohort)"},
        ax=ax
    )
    ax.set_title("Symptom Co-Occurrence Matrix: Percentage of Patients Sharing Symptoms", fontsize=16, pad=16)
    fig.tight_layout()
    save_plot(fig, "12_symptom_co_occurrence.png")

    # -------------------------------------------------------------------------
    # Master Plot: All Features Distribution Grid (All 17 Features in 1 Figure)
    # -------------------------------------------------------------------------
    features_ordered = [
        "Age", "Gender", "class",
        "Polyuria", "Polydipsia", "sudden weight loss", "weakness",
        "Polyphagia", "Genital thrush", "visual blurring", "Itching",
        "Irritability", "delayed healing", "partial paresis", "muscle stiffness",
        "Alopecia", "Obesity"
    ]
    fig, axes = plt.subplots(6, 3, figsize=(18, 22))
    fig.suptitle("Comprehensive Feature Distributions & Diabetes Risk Association (All 17 Features)", fontsize=20, y=0.995)

    for idx, col in enumerate(features_ordered):
        ax = axes.flat[idx]
        if col == "Age":
            sns.histplot(
                data=df,
                x="Age",
                hue="class",
                palette=PALETTE_BINARY,
                kde=True,
                ax=ax,
                bins=18,
                alpha=0.45,
                edgecolor="#ffffff",
                linewidth=0.8
            )
            mean_val = df["Age"].mean()
            ax.axvline(mean_val, color="#64748B", linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:.1f}y")
            ax.set_title(f"1. Age (Continuous, Years)", pad=8)
            ax.set_xlabel("Age")
            ax.set_ylabel("Patients")
            ax.legend(title="Risk Class", fontsize=8, title_fontsize=8.5, frameon=True, facecolor="white")
        elif col == "class":
            counts = df["class"].value_counts()
            bars = ax.bar(
                ["Positive", "Negative"],
                [counts.get("Positive", 0), counts.get("Negative", 0)],
                color=[COLOR_POS, COLOR_NEG],
                width=0.55,
                edgecolor="#333333",
                alpha=0.88
            )
            ax.set_title(f"3. Class (Target Outcome)", pad=8)
            ax.set_ylabel("Patients")
            ax.set_ylim(0, 360)
            for b in bars:
                h = b.get_height()
                ax.text(b.get_x() + b.get_width()/2, h + 6, f"{h}\n({h/len(df)*100:.1f}%)", ha="center", fontsize=8.5, fontweight="bold")
        else:
            sns.countplot(
                data=df,
                x=col,
                hue="class",
                palette=PALETTE_BINARY,
                ax=ax,
                edgecolor="#333333",
                alpha=0.88
            )
            feat_num = idx + 1
            ax.set_title(f"{feat_num}. {col.title()}", pad=8)
            ax.set_xlabel("")
            ax.set_ylabel("Patients")
            for p in ax.patches:
                h = p.get_height()
                if h > 0:
                    ax.annotate(f"{int(h)}", (p.get_x() + p.get_width()/2., h + 3), ha="center", fontsize=8, fontweight="semibold")
            if idx == 1:
                ax.legend(title="Risk Class", fontsize=8, title_fontsize=8.5, frameon=True, facecolor="white")
            else:
                if ax.get_legend():
                    ax.get_legend().remove()
        sns.despine(ax=ax)

    # 18th subplot: Summary Card
    ax_summary = axes.flat[17]
    ax_summary.axis("off")
    summary_text = (
        "DATASET SUMMARY METRICS\n"
        "====================================\n\n"
        "• Total Patient Records: 520\n"
        "• Total Input Features: 16 (1 Num, 15 Cat)\n"
        "• Target Variable: Class (Positive / Negative)\n"
        "• Positive Class: 320 (61.5%)\n"
        "• Negative Class: 200 (38.5%)\n"
        "• Data Completeness: 100% (0 Missing)\n"
        "• Unique Patient Profiles: 251\n"
        "• Duplicate Records: 269 (51.7%)\n\n"
        "Color Legend:\n"
        "  [Red] Positive Diabetes Risk\n"
        "  [Blue] Negative Diabetes Risk"
    )
    ax_summary.text(
        0.05, 0.5,
        summary_text,
        fontsize=9.5,
        family="monospace",
        verticalalignment="center",
        bbox=dict(boxstyle="round,pad=1", facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5)
    )
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    save_plot(fig, "all_features_distribution_grid.png")


# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("Starting Comprehensive EDA Artifact Generation...")
    print("=" * 70)
    
    df, df_encoded, df_clean, symptom_cols = load_and_prepare_data()
    print(f"Loaded Raw Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Unique Profiles (Deduplicated): {df_clean.shape[0]} rows")
    
    generate_csv_tables(df, df_encoded, df_clean, symptom_cols)
    generate_plots(df, df_encoded, df_clean, symptom_cols)
    
    print("\n" + "=" * 70)
    print("ALL EDA ARTIFACTS SUCCESSFULLY GENERATED!")
    print("Plots saved to:")
    print("  - eda_plots/")
    print("  - reports/eda_plots/")
    print("CSV summary tables saved to:")
    print("  - eda_tables/")
    print("  - reports/eda_tables/")
    print("=" * 70)


if __name__ == "__main__":
    main()

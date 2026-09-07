# Exploratory Data Analysis & Preprocessing Audit Report

## Verdict & Overview

**Status**: **Verified & Approved**

The [01_exploratory_data_analysis.ipynb](../notebooks/01_exploratory_data_analysis.ipynb) notebook is **completely fine, clean, properly structured, and mathematically accurate**.

Every stage—from initial exploratory data analysis and data-quality audits to train-test splitting and the transformation pipeline—has been verified by executing the notebook end-to-end and validating all intermediate tensors, shapes, distributions, and statistics.

---

## Part 1: Audit of Everything Before Preprocessing (Cells 0–40: EDA & Validation)

| Stage | Verification Check | Status | Details |
| :--- | :--- | :---: | :--- |
| **Data Loading & Baseline** (Cells 1–6) | Raw dimensions & types | **Accurate** | Loaded 520 rows, 17 columns (16 string/categorical, 1 numerical `Age`). |
| **Target Distribution** (Cells 7–9) | Class breakdown | **Accurate** | Correctly computes 320 Positive (61.54%) and 200 Negative (38.46%). Markdown accurately addresses class balance and implications for evaluation metrics. |
| **Categorical Distributions** (Cells 10–14) | Symptom frequency & grid plot | **Neat & Proper** | Isolates symptom columns dynamically; visualizes all 14 symptoms in a 4x4 subplot grid cleanly with unused subplots hidden. |
| **Age Distribution** (Cells 15–16) | Histogram & KDE | **Accurate** | Correctly measures mean (48.03) and median (47.5) with bounds 16–90 years. |
| **Bivariate Association** (Cells 17–27) | Cross-tabulations & feature diffs | **Accurate** | Computes percentage point differences between positive and negative classes for all symptoms. Polyuria (+68.44 pp) and Polydipsia (+67.14 pp) are correctly highlighted. |
| **Duplicate Audit** (Cells 28–30) | Duplicate identification & label check | **Proper & Rigorous** | Discovers 269 duplicate rows across 251 unique combinations. Groupby check verifies that zero duplicate feature vectors have conflicting target labels. |
| **Data Quality Validation** (Cells 31–36) | Nulls, out-of-bounds, whitespace | **Thorough** | 0 nulls, 0 records outside [0, 120] years, 0 trailing/leading whitespace issues across all string columns. |
| **Gender vs. Class** (Cells 37–40) | Cross-tabulation & uniqueness | **Accurate** | 90.5% of negatives are male vs. 45.9% of positives. Cardinality check confirms all 15 categorical features are binary. |

---

## Part 2: Audit of the Preprocessing Stage (Cells 41–61)

The preprocessing workflow is streamlined, reproducible, and leak-free:

### 1. Deduplication Strategy & Execution (Cells 42–47)
* **Logic:** Duplicates are removed before splitting (`df = df.drop_duplicates().reset_index(drop=True)`).
* **Rationale:** Because identical feature rows represent the same patient profile, allowing duplicates across train and test sets would lead to severe data leakage and artificially inflated evaluation metrics.
* **Accuracy:** Reduces the dataset from 520 to 251 unique rows. The documentation explicitly details the resulting class shift from 61.5% Positive to **68.92% Positive (173 rows) / 31.08% Negative (78 rows)**.

### 2. Feature & Target Separation (Cells 48–49)
* $X = \text{df.drop}("class", \text{axis}=1) \rightarrow \text{Shape: } (251, 16)$
* $y = \text{df}["class"].\text{map}(\{"Negative": 0, "Positive": 1\}) \rightarrow \text{Shape: } (251,)$
* Deterministic mapping correctly assigns `0 = Negative`, `1 = Positive` (aligned with medical and diagnostic convention). No `NaN` values generated.

### 3. Train-Test Split (Cells 50–52)
* **Configuration:** `test_size=0.20`, `stratify=y`, `random_state=42`.
* **Shapes:**
  * `X_train`: $(200, 16)$, `y_train`: $(200,)$
  * `X_test`: $(51, 16)$, `y_test`: $(51,)$
* **Stratification Integrity:**
  * Training Positive rate: **69.00%** (138 Positive, 62 Negative)
  * Test Positive rate: **68.63%** (35 Positive, 16 Negative)
  * The class balance is proportionally preserved across both partitions.

### 4. Preprocessing Pipeline & Leakage Prevention (Cells 53–58)
* **Feature Separation:**
  * Numerical: `['Age']` (1 feature)
  * Categorical: 15 binary features dynamically identified.
* **Transformer Architecture:**
  ```python
  preprocessor = ColumnTransformer(
      transformers=[
          (
              "categorical",
              OneHotEncoder(drop="if_binary", handle_unknown="ignore"),
              categorical_features,
          ),
          ("numerical", StandardScaler(), numerical_features),
      ]
  )
  ```
  * `drop="if_binary"` drops the first category alphabetically (`Female` $\rightarrow$ 0, `Male` $\rightarrow$ 1; `No` $\rightarrow$ 0, `Yes` $\rightarrow$ 1), producing exactly 1 binary indicator per symptom/demographic feature.
  * **Strict Data Leakage Prevention:** `preprocessor.fit(X_train)` is fitted **strictly on `X_train`**. `X_test` is strictly transformed (`preprocessor.transform(X_test)`), ensuring no test distribution statistics leak into the training process.

### 5. Output Verification & Sanity Checks (Cells 59–60)
* **Processed Dimensions:**
  * `X_train_processed`: $(200, 16)$
  * `X_test_processed`: $(51, 16)$
* **Feature Values:**
  * Categorical encoded values: cleanly binary $[0., 1.]$.
  * Scaled training Age: $\mu = -0.0$, $\sigma = 1.0$.
  * Scaled test Age: $\mu \approx 0.0117$, $\sigma \approx 1.0326$ (confirms test statistics were transformed purely using training parameters).
* **Data Integrity:** 0 missing values and 0 duplicate rows in both partitions.

---

## Observations & Pro-Tips

1. **State Mutation During Notebook Execution:**
   * Cell 44 reassigns `df = df.drop_duplicates().reset_index(drop=True)`. When executing linearly from top-to-bottom, this is completely fine. For interactive cell execution where cells might be re-run out of order, assigning to a new variable (e.g. `df_clean`) provides complete immutability.
2. **DataFrame Output Option (Optional):**
   * Currently, `preprocessor.transform()` returns a 2D NumPy array, which is standard for Scikit-Learn estimators. To retain explicit column names (e.g., `categorical__Gender_Male`, `numerical__Age`) in a Pandas DataFrame, `preprocessor.set_output(transform="pandas")` can be enabled before transformation.

---

## Conclusion

Everything up to and including the preprocessing step is executed **neatly, properly, completely, and accurately**. The dataset, train/test splits, and preprocessing transformer are fully validated and ready for model training and evaluation.

# Dataset Documentation

## 1. Dataset Source

The dataset used in this project is the **Early Stage Diabetes Risk Prediction** dataset obtained from the UCI Machine Learning Repository.

**Source:** UCI Machine Learning Repository  
**Dataset:** Early Stage Diabetes Risk Prediction  
**Dataset ID:** 529

The original dataset file is preserved without modification in:

`data/raw/diabetes_data_upload.csv`

---

## 2. Dataset Overview

The dataset contains demographic and symptom-related information associated with diabetes risk.

Our downloaded CSV contains:

- **520 observations**
- **17 columns**
- **16 input features**
- **1 binary target variable**

The target variable is `class`.

According to the UCI dataset documentation, the target is binary:

- `Positive`
- `Negative`

The dataset contains one numerical feature, `Age`, and categorical demographic/symptom features.

---

## 3. Features

The 16 input features are:

| Feature | Type | Description |
|---|---|---|
| Age | Numerical | Age of the individual |
| Gender | Categorical | Gender |
| Polyuria | Categorical | Presence of excessive urination |
| Polydipsia | Categorical | Presence of excessive thirst |
| sudden weight loss | Categorical | Presence of sudden weight loss |
| weakness | Categorical | Presence of weakness |
| Polyphagia | Categorical | Presence of excessive hunger |
| Genital thrush | Categorical | Presence of genital thrush |
| visual blurring | Categorical | Presence of visual blurring |
| Itching | Categorical | Presence of itching |
| Irritability | Categorical | Presence of irritability |
| delayed healing | Categorical | Presence of delayed healing |
| partial paresis | Categorical | Presence of partial paresis |
| muscle stiffness | Categorical | Presence of muscle stiffness |
| Alopecia | Categorical | Presence of alopecia |
| Obesity | Categorical | Presence of obesity |

---

## 4. Target Variable

The target variable is:

`class`

It is a binary categorical variable with two possible values:

- `Positive`
- `Negative`

The target will be used as the output that the supervised machine learning models learn to predict.

---

## 5. Raw Dataset Quality Audit

The original CSV was inspected before performing any modifications.

### Dataset dimensions

- Rows: **520**
- Columns: **17**

### Missing values

No missing values were found in any column.

### Duplicate observations

A total of **269 exact repeated observations** were identified, resulting in **251 unique feature combinations**.

Because the dataset does not contain a patient identifier, these repeated observations cannot be confirmed to represent repeated records of the same individuals. Therefore, they should not automatically be described as duplicate patients.

No conflicting target labels were found for identical combinations of the 16 input features.

### Target distribution

| Class | Count | Percentage |
|---|---:|---:|
| Positive | 320 | 61.54% |
| Negative | 200 | 38.46% |

### Age statistics

| Statistic | Value |
|---|---:|
| Mean | 48.03 |
| Median | 47.50 |
| Standard deviation | 12.15 |
| Minimum | 16 |
| Maximum | 90 |

No missing age values were found.

No age values below 0 or above 120 were found.

### Categorical value consistency

The categorical columns were checked for unexpected values and leading/trailing whitespace.

No leading/trailing whitespace issues were found.

The categorical variables contained the expected binary values:

- Gender: `Male`, `Female`
- Symptom/condition features: `Yes`, `No`
- Target: `Positive`, `Negative`

### Column names

No duplicate column names were found.

---

## 6. Important Dataset Metadata Note

The UCI metadata lists an age range of 1–65 for the `Age` variable. However, the downloaded CSV used in this project contains observed ages ranging from **16 to 90**.

This discrepancy has been recorded rather than modifying or removing observations solely to match the metadata.

The analysis and modeling stages will be based on the actual downloaded dataset, while this metadata discrepancy will remain documented as a dataset limitation.

---

## 7. Data Handling Policy

The original dataset in `data/raw/` will remain unchanged.

Any cleaning, encoding, transformation, duplicate-handling, or preprocessing operations will be performed on a separate working copy or through reproducible preprocessing code.

This ensures that the original source data remains available for verification and reproducibility.
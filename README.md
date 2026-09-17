# Titanic Passenger Manifest: Data Science Coursework

## Week 1: Data Acquisition and Preprocessing

Loads the Titanic passenger manifest (OpenML dataset ID 40945, 1309 rows, 14 columns), performs
missing-value imputation, drops identifier and target-leaking columns, and engineers `family_size`
and `is_alone`.

Run:

```bash
python src/week1_data_prep.py
```

Outputs: `data/raw/titanic_raw.csv`, `data/processed/titanic_processed.csv`

## Week 2: Exploratory Data Analysis and Visualization

Performs univariate, bivariate, multivariate, and correlation analysis on the processed dataset,
with a focus on survival distribution and the factors associated with it (class, sex, age, fare,
family size, and embarkation port).

Run:

```bash
python src/week2_eda.py
python src/generate_report.py
```

Outputs:

- Figures: `outputs/week2_figures/`
- Summary statistics: `outputs/week2_summary.json`
- Analysis log: `outputs/week2_analysis_log.txt`
- Report: `outputs/Week_2_Exploratory_Data_Analysis_and_Visualization_Report.docx`

## Requirements

```bash
pip install -r requirements.txt
```

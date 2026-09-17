# 1. Imports
import pandas as pd
from sklearn.datasets import fetch_openml

# 2. Paths and configuration
RAW_PATH = "data/raw/titanic_raw.csv"
PROCESSED_PATH = "data/processed/titanic_processed.csv"

# 3. Load data (OpenML dataset id 40945 - Titanic passenger manifest)
titanic = fetch_openml(data_id=40945, as_frame=True, parser="auto")
df = titanic.frame

# 4. Save raw dataset exactly as retrieved
df.to_csv(RAW_PATH, index=False)

# 5. Basic cleaning and preprocessing
df["survived"] = df["survived"].astype(int)

# Median imputation for age (numeric, moderately skewed but median is robust)
df["age"] = df["age"].fillna(df["age"].median())

# Fare has a single missing value in this dataset; median imputation by class
df["fare"] = df.groupby("pclass")["fare"].transform(lambda s: s.fillna(s.median()))

# Embarked has two missing values; fill with the most frequent port
df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])

# Cabin is mostly missing; keep only a deck indicator, drop the raw column
df["deck"] = df["cabin"].astype(str).str[0]
df.loc[df["cabin"].isna(), "deck"] = "Unknown"

# Drop columns not usable for analysis (identifiers, free text, target leakage)
df = df.drop(columns=["cabin", "boat", "body", "home.dest", "ticket", "name"])

# Feature engineering used downstream in EDA
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["is_alone"] = (df["family_size"] == 1).astype(int)

# 6. Save processed dataset
df.to_csv(PROCESSED_PATH, index=False)

print(f"Raw shape: {pd.read_csv(RAW_PATH).shape}")
print(f"Processed shape: {df.shape}")
print(f"Missing values remaining:\n{df.isna().sum()[df.isna().sum() > 0]}")

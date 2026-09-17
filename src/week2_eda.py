# 1. Imports
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Paths and configuration
RAW_PATH = "data/raw/titanic_raw.csv"
PROCESSED_PATH = "data/processed/titanic_processed.csv"
FIG_DIR = "outputs/week2_figures"
SUMMARY_PATH = "outputs/week2_summary.json"
LOG_PATH = "outputs/week2_analysis_log.txt"

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 110

log_lines = []


def log(msg):
    print(msg)
    log_lines.append(str(msg))


# 3. Load data
raw_df = pd.read_csv(RAW_PATH)
df = pd.read_csv(PROCESSED_PATH)

# 4. Initial exploration
log("=== DATASET DIMENSIONS ===")
log(f"Raw dataset: {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")
log(f"Processed dataset: {df.shape[0]} rows, {df.shape[1]} columns")
log(f"Columns (processed): {list(df.columns)}")
log(f"Missing values after Week 1 preprocessing: {int(df.isna().sum().sum())}")

# 5. Descriptive statistics
numeric_summary = df[["age", "fare", "family_size", "sibsp", "parch"]].describe().round(2)
log("\n=== NUMERICAL SUMMARY ===")
log(numeric_summary.to_string())

categorical_summary = {
    "sex": df["sex"].value_counts().to_dict(),
    "pclass": df["pclass"].value_counts().sort_index().to_dict(),
    "embarked": df["embarked"].value_counts().to_dict(),
    "is_alone": df["is_alone"].value_counts().to_dict(),
}
log("\n=== CATEGORICAL SUMMARY ===")
log(json.dumps(categorical_summary, indent=2))

survival_rate_overall = df["survived"].mean() * 100
log(f"\nOverall survival rate: {survival_rate_overall:.2f}%")

# 6. Univariate analysis

# A. Survival distribution
fig, ax = plt.subplots(figsize=(6, 5))
counts = df["survived"].value_counts().sort_index()
ax.bar(["Did not survive", "Survived"], counts.values, color=["#c0392b", "#27ae60"])
ax.set_title("Overall Survival Distribution")
ax.set_xlabel("Outcome")
ax.set_ylabel("Number of Passengers")
for i, v in enumerate(counts.values):
    ax.text(i, v + 10, str(v), ha="center")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/01_survival_distribution.png")
plt.close(fig)

# D. Age distribution
fig, ax = plt.subplots(figsize=(7, 5))
sns.histplot(df["age"], bins=30, kde=True, ax=ax, color="#2980b9")
ax.set_title("Distribution of Passenger Age")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Frequency")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/04_age_distribution.png")
plt.close(fig)

# F. Fare distribution (raw and log-transformed, since fare is highly skewed)
df["fare_log"] = np.log1p(df["fare"])
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
sns.histplot(df["fare"], bins=40, ax=axes[0], color="#8e44ad")
axes[0].set_title("Fare Distribution (Original Scale)")
axes[0].set_xlabel("Fare")
axes[0].set_ylabel("Frequency")
sns.histplot(df["fare_log"], bins=40, ax=axes[1], color="#8e44ad")
axes[1].set_title("Fare Distribution (Log-Transformed)")
axes[1].set_xlabel("log(1 + Fare)")
axes[1].set_ylabel("Frequency")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/06_fare_distribution.png")
plt.close(fig)

fare_skew = df["fare"].skew()
fare_log_skew = df["fare_log"].skew()
log(f"\nFare skewness (original): {fare_skew:.2f}")
log(f"Fare skewness (log-transformed): {fare_log_skew:.2f}")

# 7. Bivariate analysis

# B. Survival by passenger class
survival_by_class = (df.groupby("pclass")["survived"].mean() * 100).round(2)
fig, ax = plt.subplots(figsize=(6, 5))
sns.barplot(x=survival_by_class.index, y=survival_by_class.values, ax=ax, color="#2980b9")
ax.set_title("Survival Rate by Passenger Class")
ax.set_xlabel("Passenger Class")
ax.set_ylabel("Survival Rate (%)")
ax.set_ylim(0, 100)
for i, v in enumerate(survival_by_class.values):
    ax.text(i, v + 2, f"{v:.1f}%", ha="center")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/02_survival_by_class.png")
plt.close(fig)

# C. Survival by sex
survival_by_sex = (df.groupby("sex")["survived"].mean() * 100).round(2)
fig, ax = plt.subplots(figsize=(6, 5))
sns.barplot(x=survival_by_sex.index, y=survival_by_sex.values, ax=ax, color="#e67e22")
ax.set_title("Survival Rate by Sex")
ax.set_xlabel("Sex")
ax.set_ylabel("Survival Rate (%)")
ax.set_ylim(0, 100)
for i, v in enumerate(survival_by_sex.values):
    ax.text(i, v + 2, f"{v:.1f}%", ha="center")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/03_survival_by_sex.png")
plt.close(fig)

# E. Age and survival
fig, ax = plt.subplots(figsize=(7, 5))
sns.kdeplot(data=df, x="age", hue="survived", fill=True, common_norm=False,
            palette={0: "#c0392b", 1: "#27ae60"}, ax=ax)
ax.set_title("Age Distribution by Survival Status")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Density")
handles = [plt.Rectangle((0, 0), 1, 1, color="#c0392b"), plt.Rectangle((0, 0), 1, 1, color="#27ae60")]
ax.legend(handles, ["Did not survive", "Survived"], title="Outcome")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/05_age_survival.png")
plt.close(fig)

median_age_by_survival = df.groupby("survived")["age"].median().round(2)

# G. Fare and passenger class
fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(data=df, x="pclass", y="fare", ax=ax, color="#8e44ad")
ax.set_title("Fare Distribution by Passenger Class")
ax.set_xlabel("Passenger Class")
ax.set_ylabel("Fare")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/07_fare_by_class.png")
plt.close(fig)

median_fare_by_class = df.groupby("pclass")["fare"].median().round(2)

# H & I. Family size and alone status vs survival
df["family_category"] = pd.cut(
    df["family_size"], bins=[0, 1, 4, 11],
    labels=["Alone (1)", "Small family (2-4)", "Large family (5+)"]
)
survival_by_family = (df.groupby("family_category", observed=True)["survived"].mean() * 100).round(2)
fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(x=survival_by_family.index, y=survival_by_family.values, ax=ax, color="#16a085")
ax.set_title("Survival Rate by Family Size Category")
ax.set_xlabel("Family Size Category")
ax.set_ylabel("Survival Rate (%)")
ax.set_ylim(0, 100)
for i, v in enumerate(survival_by_family.values):
    ax.text(i, v + 2, f"{v:.1f}%", ha="center")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/08_family_size_survival.png")
plt.close(fig)

survival_by_alone = (df.groupby("is_alone")["survived"].mean() * 100).round(2)

# J. Embarkation port
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
embark_counts = df["embarked"].value_counts()
axes[0].bar(embark_counts.index, embark_counts.values, color="#2c3e50")
axes[0].set_title("Passenger Count by Embarkation Port")
axes[0].set_xlabel("Embarkation Port")
axes[0].set_ylabel("Number of Passengers")

survival_by_embarked = (df.groupby("embarked")["survived"].mean() * 100).round(2)
axes[1].bar(survival_by_embarked.index, survival_by_embarked.values, color="#2980b9")
axes[1].set_title("Survival Rate by Embarkation Port")
axes[1].set_xlabel("Embarkation Port")
axes[1].set_ylabel("Survival Rate (%)")
axes[1].set_ylim(0, 100)
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/09_embarkation_survival.png")
plt.close(fig)

# 8. Multivariate analysis: sex + pclass + survival
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=df, x="pclass", y="survived", hue="sex", ax=ax,
            palette={"male": "#2980b9", "female": "#e67e22"}, errorbar=None)
ax.set_title("Survival Rate by Passenger Class and Sex")
ax.set_xlabel("Passenger Class")
ax.set_ylabel("Survival Rate (proportion)")
ax.legend(title="Sex")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/11_survival_by_class_and_sex.png")
plt.close(fig)

# 9. Correlation analysis
corr_cols = ["survived", "pclass", "age", "fare", "sibsp", "parch", "family_size"]
corr_matrix = df[corr_cols].corr().round(2)
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, ax=ax, vmin=-1, vmax=1)
ax.set_title("Correlation Matrix of Numerical Variables")
fig.tight_layout()
fig.savefig(f"{FIG_DIR}/10_correlation_heatmap.png")
plt.close(fig)

# 10. Save outputs
summary = {
    "raw_shape": list(raw_df.shape),
    "processed_shape": list(df.shape),
    "overall_survival_rate_pct": round(survival_rate_overall, 2),
    "survival_rate_by_class_pct": survival_by_class.to_dict(),
    "survival_rate_by_sex_pct": survival_by_sex.to_dict(),
    "median_age_by_survival": median_age_by_survival.to_dict(),
    "median_fare_by_class": median_fare_by_class.to_dict(),
    "survival_rate_by_family_category_pct": survival_by_family.to_dict(),
    "survival_rate_by_alone_status_pct": survival_by_alone.to_dict(),
    "survival_rate_by_embarked_pct": survival_by_embarked.to_dict(),
    "fare_skewness_original": round(float(fare_skew), 2),
    "fare_skewness_log": round(float(fare_log_skew), 2),
    "correlation_matrix": corr_matrix.to_dict(),
}

with open(SUMMARY_PATH, "w") as f:
    json.dump(summary, f, indent=2)

with open(LOG_PATH, "w") as f:
    f.write("\n".join(log_lines))

log("\nWeek 2 EDA complete. Figures, summary, and log saved to outputs/.")

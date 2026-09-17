"""Builds the Week 2 EDA report from the outputs of week2_eda.py."""
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

FIG = "outputs/week2_figures"
OUT_PATH = "outputs/Week_2_Exploratory_Data_Analysis_and_Visualization_Report.docx"

with open("outputs/week2_summary.json") as f:
    S = json.load(f)

doc = Document()

for name in ["Normal", "Heading 1", "Heading 2", "Heading 3"]:
    style = doc.styles[name]
    style.font.name = "Calibri"

doc.styles["Normal"].font.size = Pt(11)


def h1(text):
    doc.add_heading(text, level=1)


def h2(text):
    doc.add_heading(text, level=2)


def p(text):
    doc.add_paragraph(text)


def bullet(text):
    doc.add_paragraph(text, style="List Bullet")


def figure(path, caption, width=5.8):
    doc.add_picture(f"{FIG}/{path}", width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cap.add_run(caption)
    run.italic = True
    run.font.size = Pt(10)


def table_from_dict(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, htext in enumerate(headers):
        hdr[i].text = str(htext)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
    doc.add_paragraph()


# ---------------- TITLE PAGE ----------------
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("Week 2 Task")
run.font.size = Pt(16)
run.bold = True

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("Exploratory Data Analysis and Visualization")
run.font.size = Pt(22)
run.bold = True

for _ in range(2):
    doc.add_paragraph()

ds = doc.add_paragraph()
ds.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = ds.add_run("Dataset: Titanic Passenger Manifest\n(OpenML Dataset ID 40945)")
run.font.size = Pt(13)

doc.add_page_break()

# ---------------- 1. INTRODUCTION ----------------
h1("1. Introduction")
p(
    "Exploratory Data Analysis (EDA) is the process of examining a dataset to understand its "
    "structure, distributions, and relationships before drawing conclusions or building models. "
    "It relies on descriptive statistics and visualization to surface patterns, group differences, "
    "and anomalies that are not obvious from raw tabular data alone."
)
p(
    "Visualization plays a central role in EDA because it allows numerical relationships to be "
    "assessed intuitively and communicated clearly. Charts make it possible to compare "
    "distributions across groups, identify skewness or outliers, and evaluate whether relationships "
    "between variables are worth investigating further."
)
p(
    "The purpose of this analysis is to explore the Titanic passenger manifest, building on the "
    "dataset acquisition and preprocessing completed in Week 1, in order to understand how passenger "
    "characteristics relate to survival outcomes. This report does not repeat the data-cleaning work "
    "from Week 1; it focuses on univariate, bivariate, and multivariate exploration of the cleaned dataset."
)

# ---------------- 2. DATASET OVERVIEW ----------------
h1("2. Dataset Overview")
table_from_dict(
    ["Attribute", "Value"],
    [
        ["Dataset name", "Titanic Passenger Manifest"],
        ["Source", "OpenML, dataset ID 40945"],
        ["Raw dataset dimensions", f"{S['raw_shape'][0]} rows x {S['raw_shape'][1]} columns"],
        ["Processed dataset dimensions", f"{S['processed_shape'][0]} rows x {S['processed_shape'][1]} columns"],
        ["Target variable", "survived (0 = did not survive, 1 = survived)"],
        ["Key variables", "pclass, sex, age, fare, sibsp, parch, embarked, family_size, is_alone"],
    ],
)
p(
    "The processed dataset used in this report is the output of Week 1 preprocessing: missing age and "
    "fare values were imputed, missing embarkation values were filled with the most frequent port, and "
    "identifier or free-text columns (name, ticket, cabin, home.dest) were removed. Variables that would "
    "leak the outcome (boat, body) were excluded from the analysis. Two engineered features carried over "
    "from Week 1, family_size and is_alone, are used throughout this report."
)

# ---------------- 3. EDA METHODOLOGY ----------------
h1("3. EDA Methodology")
p("The analysis followed a structured workflow:")
for step in [
    "Dataset loading (raw and processed versions)",
    "Initial inspection of dimensions, data types, and missing values",
    "Descriptive statistics for numerical and categorical variables",
    "Univariate analysis of individual variables",
    "Bivariate analysis of variable pairs, primarily against the survival outcome",
    "Multivariate analysis combining three or more variables",
    "Correlation analysis among numerical variables",
    "Interpretation of results, separating direct observations from possible explanations",
]:
    bullet(step)

# ---------------- 4. INITIAL EXPLORATION ----------------
h1("4. Initial Exploration")
p(f"The processed dataset contains {S['processed_shape'][0]} rows and {S['processed_shape'][1]} columns, "
  "with no remaining missing values following Week 1 preprocessing.")

h2("Numerical Summary")
table_from_dict(
    ["Statistic", "Age", "Fare", "Family Size"],
    [
        ["Mean", "29.50", "33.28", "1.88"],
        ["Median", "28.00", "14.45", "1.00"],
        ["Std. Deviation", "12.91", "51.74", "1.58"],
        ["Minimum", "0.17", "0.00", "1.00"],
        ["Maximum", "80.00", "512.33", "11.00"],
    ],
)

h2("Categorical Summary")
table_from_dict(
    ["Variable", "Category", "Count"],
    [
        ["Sex", "Male", 843],
        ["Sex", "Female", 466],
        ["Passenger Class", "1", 323],
        ["Passenger Class", "2", 277],
        ["Passenger Class", "3", 709],
        ["Embarked", "Southampton (S)", 916],
        ["Embarked", "Cherbourg (C)", 270],
        ["Embarked", "Queenstown (Q)", 123],
    ],
)

p(f"Overall survival rate: {S['overall_survival_rate_pct']}% of the {S['processed_shape'][0]} passengers survived, "
  "confirming that the dataset is moderately imbalanced toward non-survivors.")

figure("01_survival_distribution.png",
       "Figure 1. Overall counts of surviving and non-surviving passengers.")
p("OBSERVATION: Non-survivors outnumber survivors, consistent with the 38.2% overall survival rate.")

# ---------------- 5. UNIVARIATE ANALYSIS ----------------
h1("5. Univariate Analysis")

h2("Age Distribution")
figure("04_age_distribution.png", "Figure 2. Distribution of passenger age.")
p("OBSERVATION: The age distribution is concentrated between roughly 20 and 40 years, with a median of "
  "28 years, and a smaller peak near very young ages. The right tail extends to 80 years.")
p("POSSIBLE EXPLANATION: The concentration around young-to-middle adulthood is consistent with typical "
  "passenger demographics of ocean liner travel in this period, though the dataset alone does not "
  "establish the underlying cause of this shape.")

h2("Fare Distribution")
figure("06_fare_distribution.png",
       "Figure 3. Fare distribution on the original scale (left) and after a log(1 + fare) transformation (right).")
p(f"OBSERVATION: The fare distribution is strongly right-skewed (skewness = {S['fare_skewness_original']}), "
  "with most fares below 35 and a small number of very high fares extending to over 500. Applying a "
  f"log(1 + fare) transformation reduces the skewness to {S['fare_skewness_log']}, producing a more "
  "symmetric distribution suitable for visual comparison across groups.")
p("POSSIBLE EXPLANATION: The long right tail likely reflects a small number of passengers who purchased "
  "premium accommodations, but the dataset does not provide direct evidence of cabin quality beyond "
  "class and fare.")

# ---------------- 6. BIVARIATE ANALYSIS ----------------
h1("6. Bivariate Analysis")

h2("Survival by Passenger Class")
figure("02_survival_by_class.png", "Figure 4. Survival rate by passenger class.")
p(f"OBSERVATION: Survival rate decreases from {S['survival_rate_by_class_pct']['1']}% in first class to "
  f"{S['survival_rate_by_class_pct']['2']}% in second class and {S['survival_rate_by_class_pct']['3']}% in "
  "third class. This is a clear, monotonic difference across the three groups.")
p("POSSIBLE EXPLANATION: Passenger class may reflect differences in cabin location, proximity to lifeboats, "
  "or boarding priority. This dataset does not directly measure any of these factors, so the explanation "
  "remains plausible rather than confirmed.")

h2("Survival by Sex")
figure("03_survival_by_sex.png", "Figure 5. Survival rate by sex.")
p(f"OBSERVATION: Female passengers show a survival rate of {S['survival_rate_by_sex_pct']['female']}%, "
  f"compared to {S['survival_rate_by_sex_pct']['male']}% for male passengers. This is the largest group "
  "difference found in the dataset.")
p("POSSIBLE EXPLANATION: This pattern is consistent with an evacuation procedure that prioritized women, "
  "although the dataset itself only records the outcome, not the evacuation process.")

h2("Age and Survival")
figure("05_age_survival.png", "Figure 6. Age distribution split by survival status.")
p(f"OBSERVATION: The median age is {S['median_age_by_survival']['1']} years for survivors and "
  f"{S['median_age_by_survival']['0']} years for non-survivors, nearly identical. The two density curves "
  "overlap substantially, with a modest excess of survivors at very young ages.")
p("POSSIBLE EXPLANATION: Age alone does not appear to strongly separate survivors from non-survivors in "
  "this dataset; any age-related effect is likely secondary to other factors such as sex or class.")

h2("Fare and Passenger Class")
figure("07_fare_by_class.png", "Figure 7. Fare distribution across passenger classes.")
p(f"OBSERVATION: Median fare declines sharply from {S['median_fare_by_class']['1']} in first class to "
  f"{S['median_fare_by_class']['2']} in second class and {S['median_fare_by_class']['3']} in third class, "
  "with first class also showing the widest spread and the most extreme high-value outliers.")

h2("Family Size and Survival")
figure("08_family_size_survival.png", "Figure 8. Survival rate by family size category.")
p(f"OBSERVATION: Passengers travelling in small families (2-4 members) show the highest survival rate "
  f"({S['survival_rate_by_family_category_pct']['Small family (2-4)']}%), compared to "
  f"{S['survival_rate_by_family_category_pct']['Alone (1)']}% for those travelling alone and "
  f"{S['survival_rate_by_family_category_pct']['Large family (5+)']}% for large families. The relationship "
  "is non-monotonic: both travelling completely alone and travelling in a large group are associated with "
  "lower survival than travelling in a small family.")
p("POSSIBLE EXPLANATION: Small family groups may have been easier to coordinate during evacuation than "
  "large families, while solo travellers may have had less assistance. This is a plausible reading of the "
  "pattern rather than a proven mechanism.")

p(f"Related to this, passengers travelling with at least one family member had a survival rate of "
  f"{S['survival_rate_by_alone_status_pct']['0']}%, compared to {S['survival_rate_by_alone_status_pct']['1']}% "
  "for those travelling alone, reinforcing the family-size pattern above.")

h2("Embarkation Port")
figure("09_embarkation_survival.png",
       "Figure 9. Passenger counts (left) and survival rate (right) by embarkation port.")
p(f"OBSERVATION: Most passengers embarked at Southampton (916), followed by Cherbourg (270) and "
  f"Queenstown (123). Survival rate is highest for passengers who embarked at Cherbourg "
  f"({S['survival_rate_by_embarked_pct']['C']}%) compared to Queenstown "
  f"({S['survival_rate_by_embarked_pct']['Q']}%) and Southampton ({S['survival_rate_by_embarked_pct']['S']}%).")
p("POSSIBLE EXPLANATION: The higher survival rate among Cherbourg passengers may be linked to a higher "
  "proportion of first-class passengers embarking there rather than the port itself; this dataset supports "
  "further cross-tabulation but does not establish a direct causal link between port and survival.")

# ---------------- 7. MULTIVARIATE ANALYSIS ----------------
h1("7. Multivariate Analysis")
figure("11_survival_by_class_and_sex.png",
       "Figure 10. Survival rate by passenger class, split by sex.")
p("OBSERVATION: Female passengers show substantially higher survival rates than male passengers within "
  "every passenger class, and the gap between first and third class is present for both sexes but is more "
  "pronounced among male passengers. Female first- and second-class passengers show the highest survival "
  "rates of any subgroup, while male third-class passengers show the lowest.")
p("POSSIBLE EXPLANATION: This suggests that sex and passenger class act as separate, compounding factors "
  "rather than one fully explaining the other. The dataset supports this combined pattern directly, but "
  "cannot confirm the underlying evacuation mechanics that produced it.")

# ---------------- 8. CORRELATION ANALYSIS ----------------
h1("8. Correlation Analysis")
figure("10_correlation_heatmap.png", "Figure 11. Correlation matrix of numerical variables.")
corr = S["correlation_matrix"]
p(f"OBSERVATION: Survival shows its strongest linear associations with passenger class "
  f"(r = {corr['survived']['pclass']}, negative) and fare (r = {corr['survived']['fare']}, positive), "
  f"while its correlation with age (r = {corr['survived']['age']}) and family size "
  f"(r = {corr['survived']['family_size']}) is weak. Passenger class and fare are strongly negatively "
  f"correlated (r = {corr['pclass']['fare']}), which is expected since higher fares correspond to lower "
  f"(numerically smaller) class labels. sibsp and parch are strongly correlated with family_size "
  f"(r = {corr['sibsp']['family_size']} and r = {corr['parch']['family_size']} respectively), which is "
  "expected because family_size is derived directly from these two variables.")
p("Correlation coefficients describe linear association only and do not imply causation. The correlation "
  "between class and survival, for example, does not by itself explain why the relationship exists.")

# ---------------- 9. TRANSFORMATIONS AND AGGREGATIONS ----------------
h1("9. Transformations and Aggregations")
table_from_dict(
    ["Transformation", "Purpose", "Interpretation Benefit"],
    [
        ["Survival rate = mean(survived) x 100, grouped by category",
         "Converts a binary outcome into a comparable percentage across groups",
         "Allows direct comparison of survival likelihood between classes, sexes, ports, etc."],
        ["fare_log = log(1 + fare)",
         "Fare is highly right-skewed (skewness 4.37)",
         "Compresses extreme values so the distribution shape is easier to inspect visually"],
        ["family_category = binned family_size (Alone, Small family, Large family)",
         "Raw family_size has many sparse values at the high end",
         "Groups rare large-family sizes into a single interpretable category"],
        ["is_alone = 1 if family_size == 1 else 0",
         "Simplifies family_size into a binary travelling-alone indicator",
         "Enables a direct two-group survival comparison"],
        ["Groupby aggregations (mean, median) by pclass, sex, embarked, family_category",
         "Numerical summaries per category are not visible from raw rows",
         "Produces the survival percentages and median statistics used throughout this report"],
    ],
)

# ---------------- 10. KEY FINDINGS ----------------
h1("10. Key Findings")
for finding in [
    f"Overall survival rate was {S['overall_survival_rate_pct']}%, indicating an imbalanced outcome variable.",
    f"Sex was the strongest observed factor: female survival rate ({S['survival_rate_by_sex_pct']['female']}%) "
    f"was nearly four times that of male passengers ({S['survival_rate_by_sex_pct']['male']}%).",
    f"Survival rate declined monotonically with passenger class, from {S['survival_rate_by_class_pct']['1']}% "
    f"in first class to {S['survival_rate_by_class_pct']['3']}% in third class.",
    "Age distributions for survivors and non-survivors were similar, suggesting age alone was a weak "
    "predictor of survival relative to sex and class.",
    f"Fare was highly right-skewed (skewness {S['fare_skewness_original']}) and required a log transformation "
    f"for clearer visual comparison (skewness reduced to {S['fare_skewness_log']}).",
    "Family size had a non-monotonic relationship with survival: passengers in small families (2-4 members) "
    "survived at a higher rate than those travelling alone or in large families.",
    f"Passengers who embarked at Cherbourg had a higher survival rate ({S['survival_rate_by_embarked_pct']['C']}%) "
    "than those from Southampton or Queenstown, though this may relate to differences in class composition "
    "rather than the port itself.",
    "Passenger class and fare were strongly negatively correlated, reflecting that fare is largely determined "
    "by the class of accommodation purchased.",
]:
    bullet(finding)

# ---------------- 11. CRITICAL INTERPRETATION ----------------
h1("11. Critical Interpretation")
p(
    "The patterns identified in this analysis are observational and derived from a single historical "
    "voyage. None of the relationships reported here, including the associations between sex, class, and "
    "survival, should be interpreted as causal. The dataset does not record the mechanisms behind these "
    "outcomes, such as evacuation order, cabin location, or crew decisions, so any explanation offered "
    "for an observed pattern remains a plausible hypothesis rather than a demonstrated cause."
)
p(
    "Several limitations should be kept in mind. The dataset has a limited sample size (1,309 passengers), "
    "which restricts the granularity of subgroup analysis, particularly for combinations such as class, "
    "sex, and embarkation port together. Age and fare values were imputed during Week 1 preprocessing, "
    "which may slightly understate the true variability of those variables. Finally, correlation "
    "coefficients only capture linear relationships and may understate associations that are non-linear "
    "or specific to subgroups."
)

# ---------------- 12. CONCLUSION ----------------
h1("12. Conclusion")
p(
    "This exploratory analysis of the Titanic passenger manifest showed that survival outcomes were most "
    "strongly associated with sex and passenger class, with weaker associations for age and family size. "
    "Visualization was essential in this process: distribution plots revealed the skewness of fare, "
    "grouped bar charts made survival-rate differences across categories immediately comparable, and the "
    "multivariate class-and-sex breakdown showed that these two factors compound rather than substitute "
    "for one another. The correlation heatmap confirmed that passenger class and fare carry overlapping "
    "information, which is a useful consideration for any subsequent modelling work. Overall, the EDA "
    "process converted a moderately sized, mixed-type dataset into a set of concrete, evidence-based "
    "observations about the structure of the data and the passengers it represents."
)

# ---------------- 13. APPENDIX ----------------
doc.add_page_break()
h1("13. Appendix: EDA Source Code")
p("The complete analysis code is available in the project repository at src/week2_eda.py. "
  "It is organized into the following sections: imports, paths and configuration, data loading, "
  "initial exploration, descriptive statistics, univariate analysis, bivariate analysis, multivariate "
  "analysis, correlation analysis, and output saving. Key excerpts are shown below.")

with open("src/week2_eda.py") as f:
    code = f.read()

code_para = doc.add_paragraph()
code_run = code_para.add_run(code)
code_run.font.name = "Consolas"
code_run.font.size = Pt(8)

doc.save(OUT_PATH)
print(f"Report saved to {OUT_PATH}")

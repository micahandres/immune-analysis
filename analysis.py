#  ----- PART 1: INITALIZATION  -----
# import all statements 
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os

# connect
db_file = "immune_analysis.db"
output_directory = "outputs"
os.makedirs(output_directory, exist_ok=True)
connection = sqlite3.connect(db_file)


# ----- PART 2: INITIAL ANALYSIS -----
# create the query to extract the data
query_request_part2 = """
SELECT
    cell_counts.sample_id AS sample,
    cell_populations.population_name AS population,
    cell_counts.cell_count AS count
FROM cell_counts
JOIN cell_populations ON cell_counts.population_id = cell_populations.population_id
 """
# sql to pandas dataframe
df_part2 = pd.read_sql_query(query_request_part2, connection)

# calc total cell count per sample
df_part2["total_count"] = df_part2.groupby("sample")["count"].transform("sum")

# calculate the relative freq percentage 
df_part2["percentage"] = (df_part2["count"] / df_part2["total_count"]) * 100

# reoder columns for desired format
df_part2 = df_part2[["sample", "total_count", "population", "count","percentage"]] 
df_part2.to_csv("outputs/relative_frequencies.csv", index=False)


# ----- PART 3: STATISTICAL ANALYSIS -----
# PART 3A: subset data for melanoma miraclib PBMC responders/non-responders -----
query_request_part3 = """
SELECT
    cell_counts.sample_id AS sample,
    cell_populations.population_name AS population,
    cell_counts.cell_count AS count,
    conditions.condition_name AS condition,
    treatments.treatment_name AS treatment,
    subjects.response,
    subjects.sex,
    samples.time_from_treatment_start,
    sample_types.sample_type_name AS sample_type
FROM cell_counts
JOIN cell_populations ON cell_counts.population_id = cell_populations.population_id
JOIN samples ON cell_counts.sample_id = samples.sample_id
JOIN subjects ON samples.subject_id = subjects.subject_id
JOIN conditions ON subjects.condition_id = conditions.condition_id
JOIN treatments ON subjects.treatment_id = treatments.treatment_id
JOIN sample_types ON samples.sample_type_id = sample_types.sample_type_id
"""
df_part3 = pd.read_sql_query(query_request_part3, connection)

# recalculate relative fequency percentage for this subset
df_part3["total_count"] = df_part3.groupby("sample")["count"].transform("sum")
df_part3["percentage"] = (df_part3["count"] / df_part3["total_count"]) * 100

miraclib_melanoma_pbmc_response_df = df_part3[
    (df_part3["treatment"] == "miraclib") &
    (df_part3["condition"] == "melanoma") &
    (df_part3["sample_type"] == "PBMC") &
    (df_part3["response"].isin(["yes","no"]))
]
miraclib_melanoma_pbmc_response_df.to_csv("outputs/miraclib_melanoma_pbmc_response_data.csv", index=False)

# PART 3B: boxplots for responders vs non-responders
plt.figure(figsize=(12, 6))
sns.boxplot(
    data=miraclib_melanoma_pbmc_response_df,
    x="population",
    y="percentage",
    hue="response"
)
plt.title("Immune Cell Population Percentages in Miraclib-Treated Melanoma PBMC Responders vs Non-Responders")
plt.xlabel("Immune Cell Population")
plt.ylabel("Relative Frequency in Percentages")   
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/miraclib_melanoma_pbmc_response_boxplot.png")
plt.close()

# PART 3C: statistical tests (t-tests) for responders vs non-responders
statistical_results = []
for population in miraclib_melanoma_pbmc_response_df["population"].unique():
    responders = miraclib_melanoma_pbmc_response_df[
        (miraclib_melanoma_pbmc_response_df["population"] == population) &
        (miraclib_melanoma_pbmc_response_df["response"] == "yes")
    ]["percentage"]
    
    non_responders = miraclib_melanoma_pbmc_response_df[
        (miraclib_melanoma_pbmc_response_df["population"] == population) &
        (miraclib_melanoma_pbmc_response_df["response"] == "no")
    ]["percentage"]
    
    t_stat, p_value = ttest_ind(responders, non_responders, equal_var=False)
    
    statistical_results.append({
        "population": population,
        "t_statistic": t_stat,
        "p_value": p_value,
        "significant": p_value < 0.05
    })

stat_results_df = pd.DataFrame(statistical_results)
stat_results_df.to_csv("outputs/miraclib_melanoma_pbmc_response_statistical_results.csv", index=False)


# ----- PART 4: DATA SUBSET ANALYSIS -----
query_request_part4 = """
SELECT
    samples.sample_id AS sample,
    subjects.subject_id AS subject,
    projects.project_name AS project,
    conditions.condition_name AS condition,
    subjects.response,
    subjects.sex,
    sample_types.sample_type_name AS sample_type,
    samples.time_from_treatment_start
FROM samples
JOIN subjects ON samples.subject_id = subjects.subject_id
JOIN projects ON subjects.project_id = projects.project_id
JOIN conditions ON subjects.condition_id = conditions.condition_id
JOIN sample_types ON samples.sample_type_id = sample_types.sample_type_id
WHERE conditions.condition_name = "melanoma" 
AND sample_types.sample_type_name = "PBMC"
AND samples.time_from_treatment_start = 0
"""

baseline_melanoma_pbmc_df = pd.read_sql_query(query_request_part4, connection)
baseline_melanoma_pbmc_df.to_csv("outputs/baseline_melanoma_pbmc_samples.csv", index=False)

# Part 4a: answering question 1 "How many samples from each project?"
samples_per_project = baseline_melanoma_pbmc_df.groupby("project")["sample"].nunique().reset_index(name = "sample_total")
samples_per_project.to_csv("outputs/baseline_melanoma_pbmc_samples_per_project.csv", index=False)

# Part 4b: answering question 2: "how many subjects were responders/non-responders?"
response_totals = baseline_melanoma_pbmc_df.groupby("response")["subject"].nunique().reset_index(name = "subject_total")
response_totals.to_csv("outputs/baseline_melanoma_pbmc_response_counts.csv", index=False)

# Part 4c: answering question 3: "How many subjects were males/females?"
sex_totals = (baseline_melanoma_pbmc_df.groupby("sex")["subject"].nunique().reset_index(name="subject_total"))
sex_totals.to_csv("outputs/baseline_sex_counts.csv", index = False)

connection.close()
print("Analysis done and saved in outputs! :D")

# separate question
male_melanoma_bcell_average = df_part3[
    (df_part3["condition"] == "melanoma") & 
    (df_part3["response"] == "yes") &
    (df_part3["population"] == "b_cell") & 
    (df_part3["sex"] == "M") & 
    (df_part3["time_from_treatment_start"] == 0)
]["count"].mean()

print(round(male_melanoma_bcell_average, 2))
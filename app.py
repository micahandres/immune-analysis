import pandas as pd
import streamlit as st

st.set_page_config(page_title="Immune Analysis Dashboard", layout="wide")
st.title("Immune Analysis Dashboard")
st.write("This dashboard provides statistical analysis and visualizations of immune cell population data from the immune_analysis.db database for Bob Loblaw")

# PART 2: initial analysis - relative frequencies of cell populations
st.header("Part 2: Relative Frequencies of Cell Populations")
relative_freqs = pd.read_csv("outputs/relative_frequencies.csv")
st.dataframe(relative_freqs)

# PART 3: statistical analysis - compare, visualize with boxplots, and report
st.header("Part 3: Statistical Analysis of Melanoma PBMC Responders vs Non-Responders")
st.subheader("Part 3a and 3b: Boxplots of Cell Population Percentages by Response Status")
st.image("outputs/miraclib_melanoma_pbmc_response_boxplot.png")
st.subheader("Part 3c: Statisical Test Results (t-tests) for Responders vs Non-Responders")
stat_results = pd.read_csv("outputs/miraclib_melanoma_pbmc_response_statistical_results.csv")
st.dataframe(stat_results)

# PART 4: data subset analysis - identify subgroup and extend query
st.header("Part 4: Baseline Melanoma PBMC Subset Analysis")
st.subheader("Baseline Melanoma PBMC Subset Data")
baseline_subset = pd.read_csv("outputs/baseline_melanoma_pbmc_samples.csv")
st.dataframe(baseline_subset)

st.subheader("Part 4a: Total Number of Samples per project")
samples_per_project = pd.read_csv("outputs/baseline_melanoma_pbmc_samples_per_project.csv")
st.dataframe(samples_per_project)

st.subheader("Part 4b: Total Number of Response and Non-Responders in Subset Dataset")
response_totals = pd.read_csv("outputs/baseline_melanoma_pbmc_response_counts.csv")
st.dataframe(response_totals)

st.subheader("Part 4c: Total Number of Male and Female Subjects in Subset Dataset")
sex_totals = pd.read_csv("outputs/baseline_sex_counts.csv")
st.dataframe(sex_totals)

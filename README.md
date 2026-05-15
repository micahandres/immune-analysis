# Immune Analysis Pipeline

Hello! It's a pleasure to meet you and thank you for setting aside time to look at my work of analyzing immune cell population data from the provided `cell-count.csv`. :)

## Overview of Code Strucure
For this pipeline, it focuses on completing the necessary steps of:
- designing a relational database schema that is able to organize the cell-count.csv information
- organize the provided data into SQLite
- be able to calculate the immune cell relative frequencies
- compare how responders and non-responders differ and measured if statistically signficant
- get statistics on a specific subset of the data
- compile all of this information onto a single dashboard for easy viewability

Following the instructions, this project has the following files of:
- load_data.py = this python file creates the SQLite database, initialize 8 tables for greater scalability, loads the CSV data into the database
- analysis.py = performs the statistical analysis that is asked and turns these statistics into clear visualizations in the form of tables and boxplots
- app.py = is the python file that opens the Streamlit interactive dashboard and displays the information
- outputs/ = this folder stores all the CSV files and plots that are created by running this pipeline

## Quick Start
To run this pipeline, please run the following commands in order
```bash
make setup
make pipeline
make dashboard
```

- `make setup` = this installs all the necessary dependencies
- `make pipeline` = creates the database and runs all the necessary statistical analysis
- `make dashboard` = opens the streamlit dashboard 


## Statistical Analysis (Part 3)
For the statistical analysis on comparing the cell relative frequencies between those who were responders and non-responders, I used the two sample t-test with a signficance threshold of p < 0.05. This t-test was used because the two sample t-test is best used to identify the mean averages between two different groups; thereby, this specific test suited the amount of groups in the problem. So, this test allowed for a statistically-backed reasoning for observing if there were any significant differences in the immune cell population percentages between the two groups.

## Thought Process Behind Database Design / Code Structure 
For this database, it was made with the intention of provided the best amount of scalability for future projects, samples, and new analytics needed to be performed in the future. For example, if there were new treatments or projects that would need to be added in the future, then they could easily be inserted in their respective tables. Ulimately, this database design was created with the intention to prevent the constant restructuring of the databse and be suited best for scalability going forward.

The eight relational tables created through SQLite were:
- projects table
- conditions table
- treatments table
- sample types table
- cell populations table
- subjects table
- samples table
- cell counts table

This design reduces the amount of duplicated data, simplifies the amount of filtering, and improves the scalability of the datasets for future information. Finally, with this schema, some types of analysis I would be eager to perform is:
- identifying and comparing how different treatments can shift the immune cell populations
- implementing a longitudinal study tracking how a subject's immune system changes over the treatment period/multiple clinical treatments
- comparing how different treatments affect different genders and the minimum amount of dosage needed for different types of genders (ex: understanding how this affects a woman's period cycle, etc.)
- developing predictive visualizations and models to compare and estimate immune response outcomes based on different treatments

## Dashboard Link
Here is a public link to the dashboard!
https://immune-analysis-4vtv55pqryddtku5mga3kh.streamlit.app/

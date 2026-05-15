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
- `make setup` = this installs all the necessary dependencies
- `make pipeline` = creates the database and runs all the necessary statistical analysis
- `make dashboard` = opens the streamlit dashboard 

## Statistical Analysis (Part 3)
For the statistical analysis on comparing the cell relative frequencies between those who were responders and non-responders, I used the two sample t-test with a signficance threshold of p < 0.05. This t-test was used because the two sample t-test is best used to identify the mean averages between two different groups; thereby, this specific test suited the amount of groups in the problem. So, this test allowed for a statistically-backed reasoning for observing if there were any significant differences in the immune cell population percentages between the two groups.

## Thought Process Behind Database Design 
For this database, it was made with the intention of provided the best amount of scalability for future projects, samples, and new analytics needed to be performed in the future. For example, if there was a new treatment that was going to be added to the database, then the treatment can be added simply by extended the treatments table and so forth; so, this same purpose was implemented in order to efficiently separate the information for best scalability. The eight tables created were:
- projects table
- conditions table
- treatments table
- sample types table
- cell populations table
- subjects table
- samples table
- cell counts table

Overall, this design serves to help prevent duplicated data and simplify the processes of addition of new information within the database--where it is possible that new subjects, samples, treatments, etc. could be added to the database and thereby this separation helps to make the database as scalable as possible. So, through this relational databse, it can also open the floor for data analysis such as treatment comparisons, subgroup filtering, tracking of subject(s) over a long period of time, etc.

## Link to dashboard

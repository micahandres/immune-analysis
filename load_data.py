# establish imports
import sqlite3
import pandas as pd
import os

# define file names
csv_file = 'cell-count.csv'
db_file = 'immune_analysis.db'
if os.path.exists(db_file):
    os.remove(db_file)

cell_populations  = [
    "b_cell",
    "cd8_t_cell",
    "cd4_t_cell",
    "nk_cell",
    "monocyte"
]

# define all functions to establish relational database
def create_db_tables(cursor):
    cursor.executescript("""
        CREATE TABLE projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT UNIQUE
        );
        CREATE TABLE conditions (
            condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_name TEXT UNIQUE
        );
        CREATE TABLE treatments (
            treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            treatment_name TEXT UNIQUE
        );
        CREATE TABLE sample_types (
            sample_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_type_name TEXT UNIQUE
        );
        CREATE TABLE cell_populations (
            population_id INTEGER PRIMARY KEY AUTOINCREMENT,
            population_name TEXT UNIQUE
        );
        CREATE TABLE subjects (
            subject_id TEXT PRIMARY KEY,
            project_id INTEGER,
            condition_id INTEGER,
            age INTEGER,
            sex TEXT,
            treatment_id INTEGER,
            response TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(project_id),
            FOREIGN KEY (condition_id) REFERENCES conditions(condition_id),
            FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id)
        );
        CREATE TABLE samples (
            sample_id TEXT PRIMARY KEY,
            subject_id TEXT,
            sample_type_id INTEGER,
            time_from_treatment_start INTEGER,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
            FOREIGN KEY (sample_type_id) REFERENCES sample_types(sample_type_id)
        );
        CREATE TABLE cell_counts (
            sample_id TEXT,
            population_id INTEGER,
            cell_count INTEGER,
            PRIMARY KEY(sample_id, population_id),
            FOREIGN KEY (sample_id)
                REFERENCES samples(sample_id),
            FOREIGN KEY (population_id)
                REFERENCES cell_populations(population_id)
        );
        CREATE INDEX idx_subjects_project
        ON subjects(project_id);

        CREATE INDEX idx_subjects_condition
        ON subjects(condition_id);

        CREATE INDEX idx_subjects_treatment
        ON subjects(treatment_id);

        CREATE INDEX idx_samples_type
        ON samples(sample_type_id);

        CREATE INDEX idx_cell_counts_population
        ON cell_counts(population_id);                   
    """)
def insert_lookup(cursor, table, name_col, value):
    cursor.execute(
        f"INSERT OR IGNORE INTO {table} ({name_col}) VALUES (?)",
        (value,)
    )

def get_id(cursor, table, id_col, name_col, value):
    cursor.execute(
        f"SELECT {id_col} FROM {table} WHERE {name_col} = ?",
        (value,)
    )
    return cursor.fetchone()[0]

def load_csv_to_db():
    df = pd.read_csv(csv_file)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    create_db_tables(cursor)
    for _, row in df.iterrows():
        insert_lookup(cursor, "projects", "project_name", row['project'])
        insert_lookup(cursor, "conditions", "condition_name", row['condition'])
        insert_lookup(cursor, "treatments", "treatment_name", row['treatment'])
        insert_lookup(cursor, "sample_types", "sample_type_name", row['sample_type'])
        
        project_id = get_id(cursor, "projects", "project_id", "project_name", row['project'])
        condition_id = get_id(cursor, "conditions", "condition_id", "condition_name", row['condition'])
        treatment_id = get_id(cursor, "treatments", "treatment_id", "treatment_name", row['treatment'])
        sample_type_id = get_id(cursor, "sample_types", "sample_type_id", "sample_type_name", row['sample_type'])
        
        # insert subjects 
        cursor.execute("""
            INSERT OR IGNORE INTO subjects 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row['subject'],
            project_id,
            condition_id,
            row['age'],
            row['sex'],
            treatment_id,
            row['response']
        ))
        # insert samples
        cursor.execute("""
            INSERT OR IGNORE INTO samples
            VALUES (?, ?, ?, ?)
        """, (
            row['sample'],
            row['subject'],
            sample_type_id,
            int(row['time_from_treatment_start'])
        ))
        # insert cell population counts 
        for population in cell_populations:
            insert_lookup(cursor, "cell_populations", "population_name", population)
            population_id = get_id(cursor, "cell_populations", "population_id", "population_name", population)
            cursor.execute("""
                INSERT OR IGNORE INTO cell_counts
                VALUES (?, ?, ?)
            """, (
                row['sample'],
                population_id,
                row[population]
            ))
    # save and commit changes
    connection.commit()
    connection.close()
    print(f"Database was made :D! {db_file}")

# run the script 
if __name__ == "__main__":
    load_csv_to_db()
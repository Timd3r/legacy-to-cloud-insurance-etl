import sqlite3
import pandas as pd

# Connect to our local legacy database
conn = sqlite3.connect('legacy_teradata.db')

# Load the raw data into a Pandas DataFrame
df = pd.read_sql_query("SELECT * FROM raw_insurance_reporting", conn)
print(f"Loaded {len(df)} rows for cleaning.")

def cleanData(df : pd.DataFrame) -> pd.DataFrame:
    cols = df.columns.tolist()

    # 1. Clean the Naming
    for col in cols:
        if df[col].dtype == 'object':  # Only apply to text columns
            df[col] = df[col].str.strip().str.title()


    # 2. Handle Missing Values
    print("\n--- Null Counts ---")
    print(df.isnull().sum())
    # No null values in this dataset
    # if there were null values, you could choose to fill them with a default value or drop those rows, depending on the context and importance of the data.
    # or make a fuction to find the average value based on the columns they have in common with others who have the missing value filled in
    # or even make a algorithm/model that is trained and tested on the existing data to predict the missing values based on patterns in the data.


    # 3. Convert Data Types
    df['Response'] = df['Response'].map({'Yes': True, 'No': False})

    return df
df = cleanData(df)
conn.close()
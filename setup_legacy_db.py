import sqlite3
import pandas as pd

# 1. Connect to (or create) our local "Teradata" database file
conn = sqlite3.connect('legacy_teradata.db')
cursor = conn.cursor()

# 2. Load your raw CSV data (Replace 'your_downloaded_file.csv' with your actual file path)
# If you want me to generate the data for you, we will save it to 'legacy_salesforce_data.csv'
try:
    df = pd.read_csv('legacy_salesforce_data.csv')
    
    # 3. Dump this data into a SQL table called 'raw_insurance_reporting'
    df.to_sql('raw_insurance_reporting', conn, if_exists='replace', index=False)
    print("Successfully created 'legacy_teradata.db' and loaded raw data!")
    
except FileNotFoundError:
    print("Error: Please make sure your CSV file is in the same folder as this script.")

# 4. Close the connection
conn.close()

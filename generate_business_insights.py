import sqlite3
import pandas as pd
import clean_legacy_data

# Connect to our local legacy database
conn = sqlite3.connect('legacy_teradata.db')

# Load the data
df = pd.read_sql_query("SELECT * FROM raw_insurance_reporting", conn)

# Clean string columns quickly so groupings match perfectly
df = clean_legacy_data.cleanData(df)
print(df["Sales Channel"].value_counts())

# summarize the average CLV and claim amount by sales channel to identify which channels are more profitable.
summary_df = df.groupby('Sales Channel')[['Customer Lifetime Value', 'Total Claim Amount']].mean().reset_index()


# Higher CLV relative to claims means a more profitable channel.
summary_df['Value_to_Claim_Ratio'] = summary_df['Customer Lifetime Value'] / summary_df['Total Claim Amount']

# Sort by the most profitable channel ratio
summary_df = summary_df.sort_values(by='Value_to_Claim_Ratio', ascending=False)

print("\n=== BUSINESS INSIGHTS FOR THE EXECUTIVE DIRECTORS ===")
print(summary_df)

conn.close()

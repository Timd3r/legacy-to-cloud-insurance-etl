import sqlite3
import pandas as pd
import clean_legacy_data

# 1. Connect and load raw data
conn = sqlite3.connect('legacy_teradata.db')
df_raw = pd.read_sql_query("SELECT * FROM raw_insurance_reporting", conn)

# 2. Capture Baselines BEFORE cleaning
raw_row_count = len(df_raw)
raw_total_claims = df_raw['Total Claim Amount'].sum()
raw_total_clv = df_raw['Customer Lifetime Value'].sum()

# 3. Run your cleaning function
df_clean = clean_legacy_data.cleanData(df_raw)

# 4. Capture Metrics AFTER cleaning
clean_row_count = len(df_clean)
clean_total_claims = df_clean['Total Claim Amount'].sum()
clean_total_clv = df_clean['Customer Lifetime Value'].sum()

# ==========================================
# CHALLENGE 3: THE VALIDATION REPORT
# ==========================================

print("\n=============================================")
print("         DATA MIGRATION AUDIT REPORT         ")
print("=============================================")

clean = True
# Check 1: Row Counts if we know that we did not remove any rows else skip it
if raw_row_count == clean_row_count:
    print(f"ROW COUNT CHECK PASSED: {clean_row_count} rows")
else:
    print(f"ROW COUNT MISMATCH: Raw had {raw_row_count}, Clean has {clean_row_count}")
    clean = False

# Check 2: Financial Integrity (Claims)
if round(raw_total_claims, 2) == round(clean_total_claims, 2):
    print(f"FINANCIAL AUDIT PASSED: Total Claims perfectly reconciled (€{clean_total_claims:,.2f})")
else:
    print(f"FINANCIAL AUDIT FAILED: Raw claims sum was €{raw_total_claims:,.2f}, but clean is €{clean_total_claims:,.2f}")
    clean = False

# Check 3: Business Value Integrity (CLV)
if round(raw_total_clv, 2) == round(clean_total_clv, 2):
    print(f"VALUE AUDIT PASSED: (€{clean_total_clv:,.2f})")
else:
    print(f"VALUE AUDIT FAILED: Raw CLV sum was €{raw_total_clv:,.2f}, but clean is €{clean_total_clv:,.2f}")
    clean = False

print("=============================================\n")

if clean:
    df_clean.to_sql('clean_insurance_reporting', conn, if_exists='replace', index=False)
    print("Data migration successful and validated! Cleaned data saved to 'clean_insurance_reporting' table.")
else:
    print("Data migration completed but validation failed. Please review the audit report for details.")

conn.close()
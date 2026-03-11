"""Data cleaning script: removes duplicates, fixes outliers and missing values."""
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

df = pd.read_csv(DATA_DIR / "leads_data.csv")

print("=== Before cleaning ===")
print(f"Rows: {df.shape[0]}")
print(df.info())

# Remove duplicates
df = df.drop_duplicates()

# Fix aberrant revenue (negative values → NaN → median imputation)
df["revenu_mensuel"] = df["revenu_mensuel"].replace(-100, np.nan)
df["revenu_mensuel"] = df["revenu_mensuel"].fillna(df["revenu_mensuel"].median())

# Fill missing profession
df["profession"] = df["profession"].fillna("Inconnu")

# Normalize interaction dates
df["derniere_interaction"] = df["derniere_interaction"].replace(
    "date_inconnue", np.nan
)
df["derniere_interaction"] = pd.to_datetime(df["derniere_interaction"])

print("\n=== After cleaning ===")
print(f"Rows: {df.shape[0]}")
print(df.info())
print(df.head(10))

output_path = DATA_DIR / "leads_cleaned.csv"
df.to_csv(output_path, index=False)
print(f"\nCleaned data saved to {output_path}")

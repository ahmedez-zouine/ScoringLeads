import pandas as pd
import numpy as np

df = pd.read_csv('../data/leads_data.csv')

print("=== Before cleaning ===")
print(f"Rows: {df.shape[0]}")
print(df.info())

df = df.drop_duplicates()

df['revenu_mensuel'] = df['revenu_mensuel'].replace(-100, np.nan)
df['revenu_mensuel'] = df['revenu_mensuel'].fillna(df['revenu_mensuel'].median())

df['profession'] = df['profession'].fillna('Inconnu')

df['derniere_interaction'] = df['derniere_interaction'].replace('date_inconnue', np.nan)
df['derniere_interaction'] = pd.to_datetime(df['derniere_interaction'])

print("\n=== After cleaning ===")
print(f"Rows: {df.shape[0]}")
print(df.info())
print(df.head(10))

df.to_csv('../data/leads_cleaned.csv', index=False)
print("\nCleaned data saved to data/leads_cleaned.csv")

"""Exploratory Data Analysis: generates distribution and correlation charts."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CHARTS_DIR = BASE_DIR / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_DIR / "leads_cleaned.csv")
sns.set_theme(style="whitegrid")

# 1 — Score distribution
plt.figure(figsize=(10, 5))
sns.histplot(df["score_interet"], bins=20, kde=True, color="steelblue")
plt.title("Distribution du Score d'Interet")
plt.xlabel("Score d'Interet")
plt.ylabel("Nombre de Clients")
plt.savefig(CHARTS_DIR / "chart_score_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 1 saved: chart_score_distribution.png")

# 2 — Income by profession
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="profession", y="revenu_mensuel", palette="Set2")
plt.title("Revenu Mensuel par Profession")
plt.xlabel("Profession")
plt.ylabel("Revenu Mensuel")
plt.xticks(rotation=45)
plt.savefig(CHARTS_DIR / "chart_income_by_profession.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 2 saved: chart_income_by_profession.png")

# 3 — Score vs income scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df, x="revenu_mensuel", y="score_interet", hue="profession", s=80, alpha=0.7
)
plt.title("Score d'Interet vs Revenu Mensuel")
plt.xlabel("Revenu Mensuel")
plt.ylabel("Score d'Interet")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.savefig(CHARTS_DIR / "chart_score_vs_income.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 3 saved: chart_score_vs_income.png")

# 4 — Clients per profession
plt.figure(figsize=(10, 5))
profession_counts = df["profession"].value_counts()
sns.barplot(x=profession_counts.index, y=profession_counts.values, palette="viridis")
plt.title("Nombre de Clients par Profession")
plt.xlabel("Profession")
plt.ylabel("Nombre de Clients")
plt.xticks(rotation=45)
plt.savefig(CHARTS_DIR / "chart_clients_per_profession.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 4 saved: chart_clients_per_profession.png")

# 5 — Correlation heatmap
plt.figure(figsize=(8, 6))
numeric_cols = df[["revenu_mensuel", "score_interet"]]
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Matrice de Correlation")
plt.savefig(CHARTS_DIR / "chart_correlation.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 5 saved: chart_correlation.png")

# --- Descriptive statistics ---
print("\n" + "=" * 50)
print("STATISTIQUES DESCRIPTIVES")
print("=" * 50)
print(f"\nNombre total de clients: {len(df)}")
print(f"\nRevenu mensuel:")
print(f"  - Moyenne:  {df['revenu_mensuel'].mean():.0f}")
print(f"  - Mediane:  {df['revenu_mensuel'].median():.0f}")
print(f"  - Min:      {df['revenu_mensuel'].min():.0f}")
print(f"  - Max:      {df['revenu_mensuel'].max():.0f}")
print(f"\nScore d'interet:")
print(f"  - Moyenne:  {df['score_interet'].mean():.1f}")
print(f"  - Mediane:  {df['score_interet'].median():.1f}")
print(f"  - Min:      {df['score_interet'].min()}")
print(f"  - Max:      {df['score_interet'].max()}")
print(f"\nClients par profession:")
print(df["profession"].value_counts().to_string())
print(f"\nDates d'interaction:")
print(f"  - Dates valides:    {df['derniere_interaction'].notna().sum()}")
print(f"  - Dates manquantes: {df['derniere_interaction'].isna().sum()}")

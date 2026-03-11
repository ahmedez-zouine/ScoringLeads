"""Scoring engine: computes a weighted lead score for each prospect."""
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

df = pd.read_csv(DATA_DIR / "leads_cleaned.csv")
df["derniere_interaction"] = pd.to_datetime(df["derniere_interaction"])

# --- Recency feature ---
DATE_REFERENCE = datetime(2024, 3, 1)
df["jours_depuis_interaction"] = (
    DATE_REFERENCE - df["derniere_interaction"]
).dt.days
df["jours_depuis_interaction"] = df["jours_depuis_interaction"].fillna(
    df["jours_depuis_interaction"].max()
)

# --- Normalisation (min-max → 0-100) ---
def minmax(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    return (series - lo) / (hi - lo) * 100


df["revenu_norm"] = minmax(df["revenu_mensuel"])
df["interet_norm"] = minmax(df["score_interet"])
# Recency: fewer days = better → invert
df["recence_norm"] = 100 - minmax(df["jours_depuis_interaction"])

# --- Weighted lead score ---
POIDS_INTERET = 0.50
POIDS_REVENU = 0.30
POIDS_RECENCE = 0.20

df["lead_score"] = (
    df["interet_norm"] * POIDS_INTERET
    + df["revenu_norm"] * POIDS_REVENU
    + df["recence_norm"] * POIDS_RECENCE
).round(1)


def categoriser_lead(score: float) -> str:
    if score >= 70:
        return "Chaud"
    elif score >= 40:
        return "Tiede"
    return "Froid"


df["categorie"] = df["lead_score"].apply(categoriser_lead)
df_sorted = df.sort_values("lead_score", ascending=False).reset_index(drop=True)

# --- Console report ---
SEP = "=" * 60
print(SEP)
print("RESULTATS DU SCORING DES LEADS")
print(SEP)

cols = ["nom", "profession", "revenu_mensuel", "score_interet", "lead_score", "categorie"]
print("\nTop 10 meilleurs leads:")
print("-" * 60)
print(df_sorted[cols].head(10).to_string(index=False))

print("\n\nRepartition par categorie:")
print("-" * 40)
counts = df["categorie"].value_counts()
for cat in ["Chaud", "Tiede", "Froid"]:
    if cat in counts.index:
        print(f"  {cat:8s}: {counts[cat]:3d} leads ({counts[cat] / len(df) * 100:.0f}%)")

print("\n\nScore moyen par profession:")
print("-" * 40)
for prof, score in df.groupby("profession")["lead_score"].mean().sort_values(ascending=False).items():
    print(f"  {prof:12s}: {score:.1f}")

print("\n\nStatistiques du lead score:")
print("-" * 40)
print(f"  Moyenne:  {df['lead_score'].mean():.1f}")
print(f"  Mediane:  {df['lead_score'].median():.1f}")
print(f"  Min:      {df['lead_score'].min():.1f}")
print(f"  Max:      {df['lead_score'].max():.1f}")

output_cols = [
    "id", "nom", "profession", "revenu_mensuel", "score_interet",
    "jours_depuis_interaction", "lead_score", "categorie",
]
output_path = DATA_DIR / "leads_scored.csv"
df_sorted[output_cols].to_csv(output_path, index=False)
print(f"\nResultats sauvegardes dans {output_path}")

import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('../data/leads_cleaned.csv')
df['derniere_interaction'] = pd.to_datetime(df['derniere_interaction'])

date_reference = datetime(2024, 3, 1)
df['jours_depuis_interaction'] = (date_reference - df['derniere_interaction']).dt.days
df['jours_depuis_interaction'] = df['jours_depuis_interaction'].fillna(df['jours_depuis_interaction'].max())

revenu_min = df['revenu_mensuel'].min()
revenu_max = df['revenu_mensuel'].max()
df['revenu_norm'] = (df['revenu_mensuel'] - revenu_min) / (revenu_max - revenu_min) * 100

score_min = df['score_interet'].min()
score_max = df['score_interet'].max()
df['interet_norm'] = (df['score_interet'] - score_min) / (score_max - score_min) * 100

jours_min = df['jours_depuis_interaction'].min()
jours_max = df['jours_depuis_interaction'].max()
df['recence_norm'] = (1 - (df['jours_depuis_interaction'] - jours_min) / (jours_max - jours_min)) * 100

poids_interet = 0.50
poids_revenu = 0.30
poids_recence = 0.20

df['lead_score'] = (
    df['interet_norm'] * poids_interet +
    df['revenu_norm'] * poids_revenu +
    df['recence_norm'] * poids_recence
)

df['lead_score'] = df['lead_score'].round(1)

def categoriser_lead(score):
    if score >= 70:
        return 'Chaud'
    elif score >= 40:
        return 'Tiede'
    else:
        return 'Froid'

df['categorie'] = df['lead_score'].apply(categoriser_lead)

df_sorted = df.sort_values('lead_score', ascending=False).reset_index(drop=True)

print("=" * 60)
print("RESULTATS DU SCORING DES LEADS")
print("=" * 60)

print("\nTop 10 meilleurs leads:")
print("-" * 60)
cols = ['nom', 'profession', 'revenu_mensuel', 'score_interet', 'lead_score', 'categorie']
print(df_sorted[cols].head(10).to_string(index=False))

print("\n\nRepartition par categorie:")
print("-" * 40)
counts = df['categorie'].value_counts()
for cat in ['Chaud', 'Tiede', 'Froid']:
    if cat in counts.index:
        print(f"  {cat:8s}: {counts[cat]:3d} clients ({counts[cat]/len(df)*100:.0f}%)")

print(f"\n\nScore moyen par profession:")
print("-" * 40)
moyennes = df.groupby('profession')['lead_score'].mean().sort_values(ascending=False)
for prof, score in moyennes.items():
    print(f"  {prof:12s}: {score:.1f}")

print(f"\n\nStatistiques du lead score:")
print("-" * 40)
print(f"  Moyenne:  {df['lead_score'].mean():.1f}")
print(f"  Mediane:  {df['lead_score'].median():.1f}")
print(f"  Min:      {df['lead_score'].min():.1f}")
print(f"  Max:      {df['lead_score'].max():.1f}")

output_cols = ['id', 'nom', 'profession', 'revenu_mensuel', 'score_interet',
               'jours_depuis_interaction', 'lead_score', 'categorie']
df_sorted[output_cols].to_csv('../data/leads_scored.csv', index=False)
print("\nResultats sauvegardes dans data/leads_scored.csv")

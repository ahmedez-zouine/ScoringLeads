import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('../data/leads_cleaned.csv')

# Set style for nice charts
sns.set_theme(style="whitegrid")

# ============================
# 1. Distribution of Interest Score
# ============================
plt.figure(figsize=(10, 5))
sns.histplot(df['score_interet'], bins=20, kde=True, color='steelblue')
plt.title('Distribution du Score d\'Interet')
plt.xlabel('Score d\'Interet')
plt.ylabel('Nombre de Clients')
plt.savefig('../charts/chart_score_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 1 saved: chart_score_distribution.png")

# ============================
# 2. Income by Profession (Boxplot)
# ============================
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='profession', y='revenu_mensuel', palette='Set2')
plt.title('Revenu Mensuel par Profession')
plt.xlabel('Profession')
plt.ylabel('Revenu Mensuel (€)')
plt.xticks(rotation=45)
plt.savefig('../charts/chart_income_by_profession.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 2 saved: chart_income_by_profession.png")

# ============================
# 3. Score vs Income (Scatter)
# ============================
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='revenu_mensuel', y='score_interet', hue='profession', s=80, alpha=0.7)
plt.title('Score d\'Interet vs Revenu Mensuel')
plt.xlabel('Revenu Mensuel (€)')
plt.ylabel('Score d\'Interet')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig('../charts/chart_score_vs_income.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 3 saved: chart_score_vs_income.png")

# ============================
# 4. Number of Clients per Profession
# ============================
plt.figure(figsize=(10, 5))
profession_counts = df['profession'].value_counts()
sns.barplot(x=profession_counts.index, y=profession_counts.values, palette='viridis')
plt.title('Nombre de Clients par Profession')
plt.xlabel('Profession')
plt.ylabel('Nombre de Clients')
plt.xticks(rotation=45)
plt.savefig('../charts/chart_clients_per_profession.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 4 saved: chart_clients_per_profession.png")

# ============================
# 5. Correlation Matrix
# ============================
plt.figure(figsize=(8, 6))
numeric_cols = df[['revenu_mensuel', 'score_interet']]
correlation = numeric_cols.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Matrice de Correlation')
plt.savefig('../charts/chart_correlation.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 5 saved: chart_correlation.png")

# ============================
# 6. Summary Statistics
# ============================
print("\n" + "="*50)
print("STATISTIQUES DESCRIPTIVES")
print("="*50)
print(f"\nNombre total de clients: {len(df)}")
print(f"\nRevenu mensuel:")
print(f"  - Moyenne:  {df['revenu_mensuel'].mean():.0f} €")
print(f"  - Mediane:  {df['revenu_mensuel'].median():.0f} €")
print(f"  - Min:      {df['revenu_mensuel'].min():.0f} €")
print(f"  - Max:      {df['revenu_mensuel'].max():.0f} €")
print(f"\nScore d'interet:")
print(f"  - Moyenne:  {df['score_interet'].mean():.1f}")
print(f"  - Mediane:  {df['score_interet'].median():.1f}")
print(f"  - Min:      {df['score_interet'].min()}")
print(f"  - Max:      {df['score_interet'].max()}")
print(f"\nClients par profession:")
print(df['profession'].value_counts().to_string())
print(f"\nDates d'interaction:")
print(f"  - Dates valides: {df['derniere_interaction'].notna().sum()}")
print(f"  - Dates manquantes: {df['derniere_interaction'].isna().sum()}")

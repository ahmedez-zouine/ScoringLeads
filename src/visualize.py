import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/leads_scored.csv')

sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Lead Scoring - Tableau de Bord', fontsize=16, fontweight='bold')

colors = {'Chaud': '#e74c3c', 'Tiede': '#f39c12', 'Froid': '#3498db'}
counts = df['categorie'].value_counts()
axes[0, 0].pie(
    [counts.get('Chaud', 0), counts.get('Tiede', 0), counts.get('Froid', 0)],
    labels=['Chaud', 'Tiede', 'Froid'],
    colors=['#e74c3c', '#f39c12', '#3498db'],
    autopct='%1.0f%%',
    startangle=90
)
axes[0, 0].set_title('Repartition des Leads')

color_list = [colors[c] for c in df['categorie']]
axes[0, 1].scatter(df['revenu_mensuel'], df['score_interet'], c=color_list, s=60, alpha=0.7)
axes[0, 1].set_xlabel('Revenu Mensuel')
axes[0, 1].set_ylabel('Score Interet')
axes[0, 1].set_title('Score Interet vs Revenu')

top10 = df.head(10)
bars = axes[1, 0].barh(top10['nom'], top10['lead_score'], color='#e74c3c')
axes[1, 0].set_xlabel('Lead Score')
axes[1, 0].set_title('Top 10 Leads')
axes[1, 0].invert_yaxis()

moyennes = df.groupby('profession')['lead_score'].mean().sort_values(ascending=True)
moyennes.plot(kind='barh', ax=axes[1, 1], color='#2ecc71')
axes[1, 1].set_xlabel('Score Moyen')
axes[1, 1].set_title('Score Moyen par Profession')

plt.tight_layout()
plt.savefig('../charts/dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("Dashboard saved: charts/dashboard.png")

fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
ax.set_title('Top 20 Leads - Classement', fontsize=14, fontweight='bold', pad=20)

top20 = df.head(20)
table_data = []
for _, row in top20.iterrows():
    table_data.append([
        row['nom'],
        row['profession'],
        f"{row['revenu_mensuel']:.0f}",
        str(row['score_interet']),
        f"{row['lead_score']:.1f}",
        row['categorie']
    ])

table = ax.table(
    cellText=table_data,
    colLabels=['Nom', 'Profession', 'Revenu', 'Interet', 'Lead Score', 'Categorie'],
    cellLoc='center',
    loc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.5)

for i in range(len(table_data)):
    cat = table_data[i][5]
    if cat == 'Chaud':
        color = '#fadbd8'
    elif cat == 'Tiede':
        color = '#fdebd0'
    else:
        color = '#d6eaf8'
    for j in range(6):
        table[i + 1, j].set_facecolor(color)

plt.savefig('../charts/classement_leads.png', dpi=150, bbox_inches='tight')
plt.close()
print("Classement saved: charts/classement_leads.png")

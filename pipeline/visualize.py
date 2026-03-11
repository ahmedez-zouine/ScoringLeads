"""Visualization: generates summary dashboard chart and top-20 ranking table."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CHARTS_DIR = BASE_DIR / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_DIR / "leads_scored.csv")
sns.set_theme(style="whitegrid")

COLORS = {"Chaud": "#e74c3c", "Tiede": "#f39c12", "Froid": "#3498db"}

# --- 2×2 dashboard ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Lead Scoring - Tableau de Bord", fontsize=16, fontweight="bold")

counts = df["categorie"].value_counts()
axes[0, 0].pie(
    [counts.get("Chaud", 0), counts.get("Tiede", 0), counts.get("Froid", 0)],
    labels=["Chaud", "Tiede", "Froid"],
    colors=["#e74c3c", "#f39c12", "#3498db"],
    autopct="%1.0f%%",
    startangle=90,
)
axes[0, 0].set_title("Repartition des Leads")

color_list = [COLORS[c] for c in df["categorie"]]
axes[0, 1].scatter(
    df["revenu_mensuel"], df["score_interet"], c=color_list, s=60, alpha=0.7
)
axes[0, 1].set_xlabel("Revenu Mensuel")
axes[0, 1].set_ylabel("Score Interet")
axes[0, 1].set_title("Score Interet vs Revenu")

top10 = df.head(10)
axes[1, 0].barh(top10["nom"], top10["lead_score"], color="#e74c3c")
axes[1, 0].set_xlabel("Lead Score")
axes[1, 0].set_title("Top 10 Leads")
axes[1, 0].invert_yaxis()

moyennes = df.groupby("profession")["lead_score"].mean().sort_values(ascending=True)
moyennes.plot(kind="barh", ax=axes[1, 1], color="#2ecc71")
axes[1, 1].set_xlabel("Score Moyen")
axes[1, 1].set_title("Score Moyen par Profession")

plt.tight_layout()
plt.savefig(CHARTS_DIR / "dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("Dashboard saved: charts/dashboard.png")

# --- Top-20 ranking table ---
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis("off")
ax.set_title("Top 20 Leads - Classement", fontsize=14, fontweight="bold", pad=20)

top20 = df.head(20)
table_data = [
    [
        row["nom"],
        row["profession"],
        f"{row['revenu_mensuel']:.0f}",
        str(row["score_interet"]),
        f"{row['lead_score']:.1f}",
        row["categorie"],
    ]
    for _, row in top20.iterrows()
]

table = ax.table(
    cellText=table_data,
    colLabels=["Nom", "Profession", "Revenu", "Interet", "Lead Score", "Categorie"],
    cellLoc="center",
    loc="center",
)
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.5)

ROW_COLORS = {"Chaud": "#fadbd8", "Tiede": "#fdebd0", "Froid": "#d6eaf8"}
for i, row in enumerate(table_data):
    color = ROW_COLORS.get(row[5], "#ffffff")
    for j in range(6):
        table[i + 1, j].set_facecolor(color)

plt.savefig(CHARTS_DIR / "classement_leads.png", dpi=150, bbox_inches="tight")
plt.close()
print("Classement saved: charts/classement_leads.png")

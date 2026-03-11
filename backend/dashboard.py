import os

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Lead Scoring Dashboard", layout="wide")
st.title("Lead Scoring - Dashboard")

try:
    stats = requests.get(f"{API_URL}/api/stats").json()
    professions = requests.get(f"{API_URL}/api/professions").json()
except Exception:
    st.error("API non disponible. Lancez le serveur avec: uvicorn api:app --reload")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Leads", stats["total_leads"])
col2.metric("Score Moyen", stats["score_moyen"])
col3.metric("Leads Chauds", stats["repartition"]["Chaud"])
col4.metric("Leads Froids", stats["repartition"]["Froid"])

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Repartition des Leads")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    labels = ["Chaud", "Tiede", "Froid"]
    sizes = [stats["repartition"][label] for label in labels]
    colors = ["#e74c3c", "#f39c12", "#3498db"]
    ax1.pie(sizes, labels=labels, colors=colors, autopct="%1.0f%%", startangle=90)
    st.pyplot(fig1)

with col_right:
    st.subheader("Score Moyen par Profession")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    profs = list(stats["score_par_profession"].keys())
    scores = list(stats["score_par_profession"].values())
    ax2.barh(profs, scores, color="#2ecc71")
    ax2.set_xlabel("Score Moyen")
    plt.tight_layout()
    st.pyplot(fig2)

st.markdown("---")
st.subheader("Liste des Leads")

col_filter1, col_filter2, col_filter3 = st.columns(3)
with col_filter1:
    cat_filter = st.selectbox("Categorie", ["Tous"] + ["Chaud", "Tiede", "Froid"])
with col_filter2:
    prof_filter = st.selectbox("Profession", ["Tous"] + professions)
with col_filter3:
    sort_option = st.selectbox(
        "Trier par", ["lead_score", "revenu_mensuel", "score_interet"]
    )

params = {"sort_by": sort_option, "order": "desc"}
if cat_filter != "Tous":
    params["categorie"] = cat_filter
if prof_filter != "Tous":
    params["profession"] = prof_filter

leads = requests.get(f"{API_URL}/api/leads", params=params).json()
df = pd.DataFrame(leads)


def color_categorie(val):
    if val == "Chaud":
        return "background-color: #fadbd8"
    elif val == "Tiede":
        return "background-color: #fdebd0"
    else:
        return "background-color: #d6eaf8"


if not df.empty:
    display_cols = [
        "nom",
        "profession",
        "revenu_mensuel",
        "score_interet",
        "lead_score",
        "categorie",
    ]
    styled = df[display_cols].style.map(color_categorie, subset=["categorie"])
    st.dataframe(styled, use_container_width=True, height=500)
else:
    st.info("Aucun lead trouve avec ces filtres.")

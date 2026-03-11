from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Optional

app = FastAPI(title="Lead Scoring API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_scored_data():
    return pd.read_csv("data/leads_scored.csv")

def load_cleaned_data():
    return pd.read_csv("data/leads_cleaned.csv")

@app.get("/")
def root():
    return {"message": "Lead Scoring API", "version": "1.0.0"}

@app.get("/api/leads")
def get_leads(
    categorie: Optional[str] = None,
    profession: Optional[str] = None,
    sort_by: str = "lead_score",
    order: str = "desc",
    limit: int = Query(default=100, le=100)
):
    df = load_scored_data()

    if categorie:
        df = df[df["categorie"] == categorie]
    if profession:
        df = df[df["profession"] == profession]

    ascending = order == "asc"
    if sort_by in df.columns:
        df = df.sort_values(sort_by, ascending=ascending)

    df = df.head(limit)
    return df.to_dict(orient="records")

@app.get("/api/leads/{lead_id}")
def get_lead(lead_id: int):
    df = load_scored_data()
    lead = df[df["id"] == lead_id]
    if lead.empty:
        return {"error": "Lead not found"}
    return lead.iloc[0].to_dict()

@app.get("/api/stats")
def get_stats():
    df = load_scored_data()
    stats = {
        "total_leads": len(df),
        "score_moyen": round(df["lead_score"].mean(), 1),
        "score_median": round(df["lead_score"].median(), 1),
        "score_min": round(df["lead_score"].min(), 1),
        "score_max": round(df["lead_score"].max(), 1),
        "repartition": {
            "Chaud": int(df[df["categorie"] == "Chaud"].shape[0]),
            "Tiede": int(df[df["categorie"] == "Tiede"].shape[0]),
            "Froid": int(df[df["categorie"] == "Froid"].shape[0]),
        },
        "score_par_profession": df.groupby("profession")["lead_score"]
            .mean().round(1).sort_values(ascending=False).to_dict()
    }
    return stats

@app.get("/api/professions")
def get_professions():
    df = load_scored_data()
    return sorted(df["profession"].unique().tolist())

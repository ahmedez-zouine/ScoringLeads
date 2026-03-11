# Lead Scoring - Data Challenge

Projet d'analyse de donnees pour le scoring et la priorisation de leads commerciaux.

## Objectif

A partir d'un jeu de donnees brutes contenant des informations sur 100 clients (revenu, profession, score d'interet, date de derniere interaction), ce projet realise :

1. **Nettoyage des donnees** : suppression des doublons, traitement des valeurs manquantes et invalides
2. **Analyse exploratoire (EDA)** : visualisation des distributions, correlations et tendances
3. **Scoring des leads** : creation d'un score composite pour prioriser les leads
4. **API REST** : backend FastAPI pour acceder aux donnees
5. **Dashboard interactif** : interface Streamlit pour visualiser et filtrer les leads

## Structure du Projet

```
ScoringLeads/
├── data/
│   ├── leads_data.csv          # Donnees brutes
│   ├── leads_cleaned.csv       # Donnees nettoyees
│   └── leads_scored.csv        # Donnees avec scores
├── src/
│   ├── clean_data.py           # Nettoyage des donnees
│   ├── eda.py                  # Analyse exploratoire
│   ├── score_leads.py          # Modele de scoring
│   └── visualize.py            # Visualisations finales
├── charts/                     # Graphiques generes
├── api.py                      # Backend FastAPI
├── dashboard.py                # Dashboard Streamlit
├── requirements.txt            # Dependances Python
└── README.md
```

## Methode de Scoring

Le lead score est calcule a partir de trois criteres ponderes :

| Critere | Poids | Description |
|---------|-------|-------------|
| Score d'interet | 50% | Niveau d'interet exprime par le client |
| Revenu mensuel | 30% | Capacite financiere du client |
| Recence | 20% | Fraicheur de la derniere interaction |

Chaque critere est normalise sur une echelle de 0 a 100 avant d'appliquer les poids.

### Categories

- **Chaud** (score >= 70) : leads prioritaires a contacter rapidement
- **Tiede** (score >= 40) : leads a entretenir
- **Froid** (score < 40) : leads a faible potentiel

## Resultats

- **13%** des leads sont classes comme "Chaud"
- **60%** sont classes comme "Tiede"
- **27%** sont classes comme "Froid"
- Les professions Ingenieur et Commercial ont les scores moyens les plus eleves


Cela lance :
- **API** : http://localhost:8000
- **Dashboard** : http://localhost:8501

## Lancement Local

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Etape 1 : Nettoyer les donnees
cd src && python clean_data.py

# Etape 2 : Analyse exploratoire
python eda.py

# Etape 3 : Scoring
python score_leads.py

# Etape 4 : Visualisations
python visualize.py

# Etape 5 : Lancer l'API
cd .. && uvicorn api:app --reload

# Etape 6 : Lancer le dashboard (dans un autre terminal)
streamlit run dashboard.py
```

## API Endpoints

| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/leads` | Liste des leads (filtrable par categorie, profession) |
| GET | `/api/leads/{id}` | Detail d'un lead |
| GET | `/api/stats` | Statistiques globales |
| GET | `/api/professions` | Liste des professions |

Exemple : `GET /api/leads?categorie=Chaud&sort_by=lead_score&order=desc`

## Technologies

- Python 3.11
- pandas, numpy, matplotlib, seaborn
- FastAPI, Uvicorn
- Streamlit

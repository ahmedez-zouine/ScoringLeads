# Lead Scoring - Data Challenge

Projet d'analyse de donnees pour le scoring et la priorisation de leads commerciaux.

## Objectif

A partir d'un jeu de donnees brutes contenant des informations sur 100 clients (revenu, profession, score d'interet, date de derniere interaction), ce projet realise :

1. **Nettoyage des donnees** : suppression des doublons, traitement des valeurs manquantes et invalides
2. **Analyse exploratoire (EDA)** : visualisation des distributions, correlations et tendances
3. **Scoring des leads** : creation d'un score composite pour prioriser les leads
4. **API REST** : backend FastAPI pour acceder aux donnees
5. **Dashboard interactif** : interface React + Streamlit pour visualiser et filtrer les leads
6. **Deploiement** : Docker Compose pour lancer l'application en une seule commande

## Lancement avec Docker (une seule commande)

```bash
docker-compose up --build
```

Cela lance :
- **Frontend React** : http://localhost:3000
- **API FastAPI** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs

Pour arreter :
```bash
docker-compose down
```

## Structure du Projet

```
ScoringLeads/
├── .env.example                # Variables d'environnement (template)
├── .gitignore
├── Makefile                    # Commandes utilitaires
├── README.md
├── docker-compose.yml          # Orchestration Docker
├── nginx.conf                  # Config Nginx (reverse proxy)
├── requirements.txt            # Dependances Python
│
├── data/
│   ├── leads_data.csv          # Donnees brutes (source)
│   ├── leads_cleaned.csv       # Donnees nettoyees (generees)
│   └── leads_scored.csv        # Donnees avec scores (generees)
│
├── pipeline/                   # Scripts du pipeline de donnees
│   ├── clean_data.py           # Nettoyage des donnees
│   ├── eda.py                  # Analyse exploratoire
│   ├── score_leads.py          # Moteur de scoring
│   └── visualize.py            # Visualisations finales
│
├── backend/                    # API & Dashboard Streamlit
│   ├── Dockerfile
│   ├── api.py                  # Backend FastAPI
│   └── dashboard.py            # Dashboard Streamlit
│
├── frontend/                   # Dashboard React (Vite)
│   ├── Dockerfile
│   └── src/
│
└── charts/                     # Graphiques generes
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

## Lancement Local

```bash
make install
make pipeline
make api         # Terminal 1
make frontend    # Terminal 2
```

Ou manuellement :

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python pipeline/clean_data.py && python pipeline/score_leads.py
cd backend && uvicorn api:app --reload

# Dans un autre terminal
cd frontend && npm install && npm run dev
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

- Python 3.11, FastAPI, Uvicorn
- pandas, numpy, matplotlib, seaborn
- React, Vite, Recharts
- Streamlit
- Docker, Docker Compose, Nginx

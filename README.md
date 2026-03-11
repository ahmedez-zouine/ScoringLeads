# Lead Scoring - Data Challenge

Projet d'analyse de donnees pour le scoring et la priorisation de leads commerciaux.

## Objectif

A partir d'un jeu de donnees brutes contenant des informations sur 100 clients (revenu, profession, score d'interet, date de derniere interaction), ce projet realise :

1. **Nettoyage des donnees** : suppression des doublons, traitement des valeurs manquantes et invalides
2. **Analyse exploratoire (EDA)** : visualisation des distributions, correlations et tendances
3. **Scoring des leads** : creation d'un score composite pour prioriser les leads
4. **Visualisation finale** : dashboard recapitulatif et classement des leads

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
├── .gitignore
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

## Technologies

- Python 3
- pandas, numpy
- matplotlib, seaborn

## Utilisation

```bash
python -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib seaborn

cd src
python clean_data.py
python eda.py
python score_leads.py
python visualize.py
```

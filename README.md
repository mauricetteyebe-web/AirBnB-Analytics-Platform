# AirBnB-Analytics-Platform
Airbnb souhaite mettre en place une plateforme analytique qui analyse les données et de mettre à disposition des indicateurs.

Voici le README en syntaxe Markdown GitHub parfaite à copier-coller directement :

```markdown
# 🏠 AirBnB Analytics Platform

## Présentation du projet

Ce projet a été réalisé dans le cadre de l'évaluation du module **Management Opérationnel 2026** — MBA Big Data & IA, MBA ESG Paris.

Il consiste à construire une plateforme analytique complète sur les données AirBnB, en suivant une architecture **Medallion (Bronze / Silver / Gold)** avec les technologies suivantes :

- **DuckDB** — moteur analytique local
- **dbt** — transformations et tests de qualité des données
- **GitHub** — versioning et collaboration
- **Streamlit** — dashboard interactif

---

## Architecture

```
CSV Seeds (données brutes)
        │
        ▼
    Bronze (dbt)
    Tables brutes sans transformation
        │
        ▼
    Silver (dbt)
    Nettoyage, typage, renommage des colonnes
        │
        ▼
    Gold (dbt)
    Data products : vues analytiques et tables finales
        │
        ▼
    Streamlit
    Dashboard interactif pour les utilisateurs métier
```

---

## Structure des éléments importants du projet

```
AirBnB-Analytics-Platform/
├── airbnb/
│   ├── models/
│   │   ├── bronze/
│   │   │   ├── bronze_hosts.sql
│   │   │   ├── bronze_listings.sql
│   │   │   ├── bronze_reviews.sql
│   │   │   └── bronze_full_moon_dates.sql
│   │   ├── silver/
│   │   │   ├── silver_hosts.sql
│   │   │   ├── silver_listings.sql
│   │   │   ├── silver_reviews.sql
│   │   │   ├── silver_full_moon_dates.sql
│   │   │   └── schema.yml
│   │   └── gold/
│   │       ├── gold_dim_hosts.sql
│   │       ├── gold_dim_listings.sql
│   │       ├── gold_fact_reviews.sql
│   │       └── gold_full_moon_reviews.sql
│   ├── seeds/
│   │   ├── hosts.csv
│   │   ├── listings.csv
│   │   └── seed_full_moon_dates.csv
│   └── dbt_project.yml
├── scripts/
│   └── clean_reviews.py
├── streamlit_app.py
├── .gitignore
└── README.md
```

---

## Données

Les fichiers sources sont les suivants :

| Fichier | Description | Lignes |
|---|---|---|
| `hosts.csv` | Informations sur les hôtes | 14 111 |
| `listings.csv` | Informations sur les logements | 17 499 |
| `reviews.csv` | Avis clients | 410 284 |
| `seed_full_moon_dates.csv` | Dates de pleine lune | 272 |

> ⚠️ Le fichier `reviews.csv` dépasse la limite GitHub (100 MB). Il doit être téléchargé manuellement et placé dans `airbnb/seeds/reviews.csv` avant de lancer le pipeline.
>
> Téléchargement : [reviews.csv](https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/reviews.csv)

---

## Installation et exécution

### Prérequis

```bash
pip install dbt-duckdb duckdb pandas streamlit
```

### Étape 1 — Nettoyer le fichier reviews.csv

```bash
python scripts/clean_reviews.py
```

### Étape 2 — Charger les seeds

```bash
dbt seed
```

### Étape 3 — Lancer les transformations

```bash
dbt run
```

### Étape 4 — Lancer les tests de qualité

```bash
dbt test
```

### Étape 5 — Générer la documentation dbt

```bash
dbt docs generate
dbt docs serve
```

### Étape 6 — Lancer le dashboard Streamlit

```bash
streamlit run streamlit_app.py
```

---

## Fonctionnalités du dashboard

### 📊 Vue générale
- KPIs globaux : nombre de logements, hôtes, avis, prix moyen
- Distribution des sentiments des avis
- Évolution du nombre d'avis par année

### 🏘️ Logements
- Filtre par type de logement
- Distribution des prix par tranche
- Top 10 des logements les plus commentés

### 👤 Hôtes
- Répartition Superhosts vs hôtes standards
- Top 10 des hôtes avec le plus de logements
- Recherche par nom d'hôte

### 🌕 Pleine lune & avis
- Comparaison des sentiments les nuits de pleine lune vs les autres nuits
- Filtre par nom de reviewer
- Table détaillée des avis

---

## Pipeline dbt — Détail des couches

### Bronze
Tables brutes chargées directement depuis les seeds CSV sans transformation.

### Silver
- Typage explicite des colonnes (BOOLEAN, DECIMAL, TIMESTAMPTZ, DATE)
- Renommage des colonnes (`comments` → `review_text`, `date` → `review_date`)
- Nettoyage du champ `price` (suppression du symbole `$`)
- Gestion des valeurs nulles (`host_name` → `'Anonymous'`, `minimum_nights` → `1`)
- Filtrage des avis sans contenu (`review_text IS NOT NULL`)

### Gold
- `gold_dim_hosts` — vue des hôtes nettoyée
- `gold_dim_listings` — vue des logements avec prix normalisé
- `gold_fact_reviews` — table des avis triés par date décroissante
- `gold_full_moon_reviews` — jointure avis × dates de pleine lune avec flag `is_full_moon`

---

## Tests de qualité

| Modèle | Colonne | Test |
|---|---|---|
| silver_hosts | host_id | unique, not_null |
| silver_listings | listing_id | unique, not_null |
| silver_listings | price | not_null |
| silver_reviews | listing_id | not_null |
| silver_reviews | review_text | not_null |

---

## Auteure

**Ann Yebe Ollomo**
MBA Big Data & Intelligence Artificielle — MBA ESG Paris — Promotion 2026

---

## Soumission

Livrable envoyé à : axel@logbrain.fr
Intitulé : **MBAESG_EVALUATION_MANAGEMENT_OPERATIONNEL_2026**
```

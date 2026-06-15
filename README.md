```markdown
# 🏠 AirBnB Analytics Platform

## Présentation du projet

Ce projet a été réalisé dans le cadre de l'évaluation **MBAESG_EVALUATION_MANAGEMENT_OPERATIONNEL_2026**.  
Il consiste à construire une plateforme analytique complète sur les données Airbnb, en suivant une architecture **Medallion (Bronze → Silver → Gold)** avec les outils suivants :

- **DuckDB** comme moteur analytique local
- **dbt** pour les transformations SQL
- **GitHub** pour le versioning et la collaboration
- **Streamlit** pour la restitution et les visualisations interactives

La plateforme permet de :
- Analyser les logements
- Analyser les hôtes
- Analyser les avis clients
- Étudier l'impact des nuits de pleine lune sur les avis
- Mettre à disposition des indicateurs via une application Streamlit

---

## Structure du projet

```
AirBnB-Analytics-Platform/
│
├── airbnb/                          # Projet dbt
│   │
│   ├── models/                      # Transformations SQL
│   │   ├── bronze/                  # Couche Bronze — données brutes
│   │   │   ├── bronze_hosts.sql
│   │   │   ├── bronze_listings.sql
│   │   │   ├── bronze_reviews.sql
│   │   │   └── bronze_full_moon_dates.sql
│   │   │
│   │   ├── silver/                  # Couche Silver — nettoyage + typage
│   │   │   ├── silver_hosts.sql
│   │   │   ├── silver_listings.sql
│   │   │   ├── silver_reviews.sql
│   │   │   ├── silver_full_moon_dates.sql
│   │   │   └── schema.yml           # Tests qualité
│   │   │
│   │   └── gold/                    # Couche Gold — data products
│   │       ├── gold_dim_hosts.sql
│   │       ├── gold_dim_listings.sql
│   │       ├── gold_fact_reviews.sql
│   │       └── gold_full_moon_reviews.sql
│   │
│   ├── seeds/                       # Données sources CSV
│   │   ├── hosts.csv
│   │   ├── listings.csv
│   │   ├── reviews.csv
│   │   └── seed_full_moon_dates.csv
│   │
│   ├── tests/                       # Tests personnalisés dbt
│   ├── macros/                      # Macros dbt
│   ├── analyses/                    # Analyses ad hoc
│   ├── snapshots/                   # Snapshots dbt
│   │
│   ├── airbnb.db                    # Base DuckDB persistante
│   └── dbt_project.yml              # Configuration dbt
│
├── scripts/                         # Scripts utilitaires
│   ├── clean_reviews.py             # Nettoyage guillemets CSV reviews
│   └── backups/                     # Sauvegardes fichiers originaux
│       └── reviews_backup.csv
│
├── streamlit_app.py                 # Dashboard Streamlit
├── README.md                        # Documentation du projet
└── .gitignore                       # Fichiers exclus du versioning
```

---

## Stack technique

| Outil | Version | Rôle |
|---|---|---|
| DuckDB | 1.10.1 | Moteur analytique local |
| dbt-duckdb | 1.11.11 | Transformations SQL |
| Python | 3.11+ | Nettoyage des données |
| Streamlit | latest | Dashboard interactif |
| GitHub | — | Versioning & collaboration |

---

## Architecture Medallion

```
CSV (seeds/)
    ↓ dbt seed
Bronze — données brutes chargées sans transformation
    ↓ dbt run
Silver — nettoyage, typage, renommage des colonnes + tests qualité
    ↓ dbt run
Gold — vues analytiques et data products métier
    ↓
Streamlit — dashboard interactif
    ↓
Business Users
```

### Couche Bronze
Chargement des données brutes depuis les fichiers CSV sans transformation.  
Chaque table Bronze correspond à un fichier source.

| Table | Source | Nb lignes |
|---|---|---|
| bronze_hosts | hosts.csv | 14 111 |
| bronze_listings | listings.csv | 17 499 |
| bronze_reviews | reviews.csv | 410 284 |
| bronze_full_moon_dates | seed_full_moon_dates.csv | 272 |

### Couche Silver
Nettoyage, typage et renommage des colonnes. Tests de qualité appliqués.

| Table | Transformations appliquées |
|---|---|
| silver_hosts | Typage BOOLEAN sur is_superhost, valeur par défaut 'Anonymous' |
| silver_listings | Nettoyage du champ price (suppression du $), gestion minimum_nights = 0 |
| silver_reviews | Filtrage des commentaires NULL, renommage des colonnes |
| silver_full_moon_dates | Cast en DATE |

### Couche Gold
Data products métier prêts pour la restitution.

| Table / Vue | Description |
|---|---|
| gold_dim_hosts | Dimension hôtes |
| gold_dim_listings | Dimension logements |
| gold_fact_reviews | Table de faits des avis |
| gold_full_moon_reviews | Avis enrichis avec indicateur pleine lune |

---

## Instructions d'installation

### Prérequis

```bash
Python 3.11+
pip install dbt-duckdb duckdb pandas streamlit
```

### Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/<votre-repo>/AirBnB-Analytics-Platform.git
cd AirBnB-Analytics-Platform

# 2. Installer les dépendances
pip install dbt-duckdb duckdb pandas streamlit

# 3. Installer les packages dbt
cd airbnb
dbt deps
```

---

## Instructions d'exécution

```bash
# Étape 1 — Nettoyage du fichier reviews.csv
# (correction des guillemets doubles imbriqués non conformes au standard CSV)
python scripts/clean_reviews.py

# Étape 2 — Chargement des seeds dans DuckDB
cd airbnb
dbt seed

# Étape 3 — Exécution des transformations Bronze → Silver → Gold
dbt run

# Étape 4 — Tests de qualité des données
dbt test

# Étape 5 — Documentation dbt (optionnel)
dbt docs generate
dbt docs serve

# Étape 6 — Lancement du dashboard Streamlit
cd ..
streamlit run streamlit_app.py
```

---

## Fonctionnalités du dashboard Streamlit

Le dashboard est organisé en **4 onglets** :

### 📊 Vue générale
- KPIs globaux : nombre de logements, hôtes, avis, prix moyen
- Distribution des sentiments des avis
- Évolution du nombre d'avis par année

### 🏘️ Logements
- Filtre dynamique par type de logement
- Nombre de logements et prix moyen par type
- Distribution des prix par tranche
- Top 10 des logements les plus commentés

### 👤 Hôtes
- Répartition Superhosts vs Hôtes standards
- Top 10 des hôtes avec le plus de logements
- Recherche dynamique par nom d'hôte

### 🌕 Pleine lune & Avis
- Comparaison des sentiments : nuits de pleine lune vs autres nuits
- Taux de sentiments positifs/négatifs selon la pleine lune
- Filtre dynamique par nom de reviewer

---

## Tests qualité (dbt test)

Les tests suivants sont appliqués sur la couche Silver :

| Table | Colonne | Test |
|---|---|---|
| silver_hosts | host_id | unique, not_null |
| silver_listings | listing_id | unique, not_null |
| silver_listings | price | not_null |
| silver_reviews | listing_id | not_null |
| silver_reviews | review_text | not_null |

---

## Note technique — Nettoyage du fichier reviews.csv

Le fichier `reviews.csv` contient des guillemets doubles imbriqués (`""nom""`) non conformes au standard CSV strict de DuckDB (erreur détectée à la ligne 18028).  
Le script `scripts/clean_reviews.py` corrige ce problème avant le chargement des seeds.  
Le fichier original est sauvegardé dans `scripts/backups/reviews_backup.csv`.


---

## Auteure

**Ann Yebe Ollomo**  
MBA Big Data & Intelligence Artificielle — MBA ESG Paris  
Juin 2026
```

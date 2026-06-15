"""
AirBnB Analytics Platform
Streamlit Dashboard connecté à DuckDB
Auteur : Ann Yebe Ollomo
Date : Juin 2026
"""

import duckdb
import streamlit as st
import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Connexion DuckDB
# ─────────────────────────────────────────────────────────────────────────────

DB_PATH = Path(__file__).parent / "airbnb" / "airbnb.db"

@st.cache_resource
def get_connection():
    return duckdb.connect(database=str(DB_PATH), read_only=True)

conn = duckdb.connect("./airbnb/dev.duckdb")
conn.execute("SHOW ALL TABLES").fetchdf()

# ─────────────────────────────────────────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AirBnB Analytics Platform",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 AirBnB Analytics Platform")
st.write("Dashboard analytique basé sur DuckDB + dbt")

# ─────────────────────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Vue générale",
    "🏘️ Logements",
    "👤 Hôtes",
    "🌕 Pleine lune & avis"
])

# =============================================================================
# TAB 1 — VUE GÉNÉRALE
# =============================================================================

with tab1:
    st.subheader("Vue générale")

    col1, col2, col3, col4 = st.columns(4)

    total_logements = conn.execute(
        "SELECT COUNT(*) FROM main.gold_dim_listings"
    ).fetchone()[0]

    total_hotes = conn.execute(
        "SELECT COUNT(*) FROM main.gold_dim_hosts"
    ).fetchone()[0]

    total_avis = conn.execute(
        "SELECT COUNT(*) FROM main.gold_fact_reviews"
    ).fetchone()[0]

    prix_moyen_nuit = conn.execute(
        "SELECT ROUND(AVG(price), 2) FROM main.gold_dim_listings"
    ).fetchone()[0]

    col1.metric("🏠 Logements", f"{total_logements:,}")
    col2.metric("👤 Hôtes", f"{total_hotes:,}")
    col3.metric("💬 Avis", f"{total_avis:,}")
    col4.metric("💶 Prix moyen / nuit", f"${prix_moyen_nuit}")

    st.divider()

    # Distribution des sentiments
    st.subheader("Distribution des sentiments")
    df_distribution_sentiments = conn.execute("""
        SELECT sentiment, COUNT(*) AS nb_reviews
        FROM main.gold_fact_reviews
        GROUP BY sentiment
        ORDER BY nb_reviews DESC
    """).df()

    st.bar_chart(df_distribution_sentiments.set_index("sentiment"))

    # Avis par année
    st.subheader("Évolution des avis par année")
    df_evolution_avis = conn.execute("""
        SELECT
            YEAR(review_date) AS annee,
            COUNT(*) AS nb_reviews
        FROM main.gold_fact_reviews
        GROUP BY annee
        ORDER BY annee
    """).df()

    st.line_chart(df_evolution_avis.set_index("annee"))

# =============================================================================
# TAB 2 — LOGEMENTS
# =============================================================================

with tab2:
    st.subheader("Analyse des logements")

    types_logement = conn.execute(
        "SELECT DISTINCT room_type FROM main.gold_dim_listings ORDER BY room_type"
    ).df()["room_type"].tolist()

    type_logement_selectionne = st.selectbox(
        "Filtrer par type de logement",
        ["Tous"] + types_logement
    )

    if type_logement_selectionne == "Tous":
        df_logements_par_type = conn.execute("""
            SELECT room_type, COUNT(*) AS nb, ROUND(AVG(price),2) AS avg_price
            FROM main.gold_dim_listings
            GROUP BY room_type
            ORDER BY nb DESC
        """).df()
    else:
        df_logements_par_type = conn.execute(f"""
            SELECT room_type, COUNT(*) AS nb, ROUND(AVG(price),2) AS avg_price
            FROM main.gold_dim_listings
            WHERE room_type = '{type_logement_selectionne}'
            GROUP BY room_type
        """).df()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Nombre de logements par type**")
        st.bar_chart(df_logements_par_type.set_index("room_type")["nb"])

    with col2:
        st.markdown("**Prix moyen par type**")
        st.bar_chart(df_logements_par_type.set_index("room_type")["avg_price"])

    # Distribution des prix
    st.subheader("Distribution des prix")
    df_distribution_prix = conn.execute("""
        SELECT
            CASE
                WHEN price < 50  THEN '< $50'
                WHEN price < 100 THEN '$50 - $100'
                WHEN price < 200 THEN '$100 - $200'
                WHEN price < 500 THEN '$200 - $500'
                ELSE '> $500'
            END AS tranche_prix,
            COUNT(*) AS nb
        FROM main.gold_dim_listings
        GROUP BY tranche_prix
        ORDER BY nb DESC
    """).df()

    st.bar_chart(df_distribution_prix.set_index("tranche_prix"))

    # Top 10 logements les plus commentés
    st.subheader("Top 10 logements les plus commentés")
    df_top_logements = conn.execute("""
        SELECT
            l.listing_name,
            l.room_type,
            l.price,
            COUNT(r.listing_id) AS nb_reviews
        FROM main.gold_dim_listings l
        LEFT JOIN main.gold_fact_reviews r ON l.listing_id = r.listing_id
        GROUP BY l.listing_name, l.room_type, l.price
        ORDER BY nb_reviews DESC
        LIMIT 10
    """).df()

    st.dataframe(df_top_logements, use_container_width=True)

# =============================================================================
# TAB 3 — HÔTES
# =============================================================================

with tab3:
    st.subheader("Analyse des hôtes")

    col1, col2 = st.columns(2)

    df_repartition_superhosts = conn.execute("""
        SELECT
            CASE WHEN is_superhost THEN 'Superhost' ELSE 'Hôte standard' END AS type_hote,
            COUNT(*) AS nb
        FROM main.gold_dim_hosts
        GROUP BY is_superhost
    """).df()

    with col1:
        st.markdown("**Superhosts vs Hôtes standards**")
        st.bar_chart(df_repartition_superhosts.set_index("type_hote"))

    df_top_hotes = conn.execute("""
        SELECT
            h.host_name,
            h.is_superhost,
            COUNT(l.listing_id) AS nb_listings,
            ROUND(AVG(l.price), 2) AS avg_price
        FROM main.gold_dim_hosts h
        LEFT JOIN main.gold_dim_listings l ON h.host_id = l.host_id
        GROUP BY h.host_name, h.is_superhost
        ORDER BY nb_listings DESC
        LIMIT 10
    """).df()

    with col2:
        st.markdown("**Top 10 hôtes (nb logements)**")
        st.bar_chart(df_top_hotes.set_index("host_name")["nb_listings"])

    st.subheader("Détail des top hôtes")
    st.dataframe(df_top_hotes, use_container_width=True)

    nom_hote_recherche = st.text_input("Nom de l'hôte", placeholder="ex: Michael")

    if nom_hote_recherche:
        df_resultats_hote = conn.execute(f"""
            SELECT
                h.host_name,
                h.is_superhost,
                l.listing_name,
                l.room_type,
                l.price,
                COUNT(r.listing_id) AS nb_reviews
            FROM main.gold_dim_hosts h
            LEFT JOIN main.gold_dim_listings l ON h.host_id = l.host_id
            LEFT JOIN main.gold_fact_reviews r ON l.listing_id = r.listing_id
            WHERE LOWER(h.host_name) LIKE LOWER('%{nom_hote_recherche}%')
            GROUP BY h.host_name, h.is_superhost, l.listing_name, l.room_type, l.price
            ORDER BY nb_reviews DESC
        """).df()

        if df_resultats_hote.empty:
            st.warning("Aucun hôte trouvé.")
        else:
            st.dataframe(df_resultats_hote, use_container_width=True)

# =============================================================================
# TAB 4 — PLEINE LUNE & AVIS
# =============================================================================

with tab4:
    st.subheader("Impact des nuits de pleine lune sur les avis")

    df_avis_pleine_lune = conn.execute("""
        SELECT
            is_full_moon,
            sentiment,
            COUNT(*) AS nb_reviews
        FROM main.gold_seed_full_moon_reviews
        GROUP BY is_full_moon, sentiment
        ORDER BY is_full_moon, nb_reviews DESC
    """).df()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Avis les nuits de pleine lune**")
        df_avis_nuits_pleine_lune = df_avis_pleine_lune[df_avis_pleine_lune["is_full_moon"] == "full moon"]
        if not df_avis_nuits_pleine_lune.empty:
            st.bar_chart(df_avis_nuits_pleine_lune.set_index("sentiment")["nb_reviews"])

    with col2:
        st.markdown("**Avis les autres nuits**")
        df_avis_nuits_hors_pleine_lune = df_avis_pleine_lune[df_avis_pleine_lune["is_full_moon"] == "not full moon"]
        if not df_avis_nuits_hors_pleine_lune.empty:
            st.bar_chart(df_avis_nuits_hors_pleine_lune.set_index("sentiment")["nb_reviews"])

    st.subheader("Comparaison globale : pleine lune vs autres nuits")
    df_comparaison_globale_lune = conn.execute("""
        SELECT
            is_full_moon,
            COUNT(*) AS nb_reviews,
            ROUND(100.0 * SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_positif,
            ROUND(100.0 * SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_negatif
        FROM main.gold_seed_full_moon_reviews
        GROUP BY is_full_moon
    """).df()

    st.dataframe(df_comparaison_globale_lune, use_container_width=True)

    reviewer_selectionne = st.selectbox(
        "Sélectionner un reviewer",
        ["Tous"] + conn.execute("""
            SELECT DISTINCT reviewer_name
            FROM main.gold_seed_full_moon_reviews
            WHERE reviewer_name IN (
                'Michael','Daniel','Thomas','David','Anna',
                'Laura','Alexander','Julia','Maria','Martin',
                'Andrea','Sarah','Christian','Lisa','Alex'
            )
            ORDER BY reviewer_name
        """).df()["reviewer_name"].tolist()
    )

    if reviewer_selectionne == "Tous":
        df_avis_reviewer = conn.execute("""
            SELECT listing_id, review_date, reviewer_name,
                   sentiment, is_full_moon
            FROM main.gold_seed_full_moon_reviews
            ORDER BY review_date DESC
            LIMIT 100
        """).df()
    else:
        df_avis_reviewer = conn.execute(f"""
            SELECT listing_id, review_date, reviewer_name,
                   sentiment, is_full_moon
            FROM main.gold_seed_full_moon_reviews
            WHERE reviewer_name = '{reviewer_selectionne}'
            ORDER BY review_date DESC
        """).df()

    st.dataframe(df_avis_reviewer, use_container_width=True)

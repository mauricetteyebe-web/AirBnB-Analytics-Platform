import duckdb
import pandas as pd
from pathlib import Path

DB_PATH   = Path(r"./airbnb/airbnb.db")
SEEDS_DIR = Path(r"./airbnb/seeds")

print(f"📁 DB path : {DB_PATH}")
print(f"📁 DB existe déjà : {DB_PATH.exists()}")

db = duckdb.connect(database=str(DB_PATH))

tables = {
    'hosts':                SEEDS_DIR / 'hosts.csv',
    'listings':             SEEDS_DIR / 'listings.csv',
    'reviews':              SEEDS_DIR / 'reviews.csv',
    'seed_full_moon_dates': SEEDS_DIR / 'seed_full_moon_dates.csv',
}

for table_name, csv_path in tables.items():
    print(f"\n⏳ Chargement {table_name} depuis {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"   DataFrame shape : {df.shape}")
    db.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
    count = db.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"   ✅ {table_name} — {count} lignes insérées")

db.close()
print(f"\n✅ Done — {DB_PATH}")
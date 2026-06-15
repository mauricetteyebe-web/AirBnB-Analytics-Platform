"""
Script de nettoyage du fichier reviews.csv
Problème : guillemets doubles imbriqués ("") sur certaines lignes (ex: ligne 18028)
causant une erreur CSV dans dbt seed (DuckDB strict_mode=true)
Solution : remplacement des guillemets imbriqués par des guillemets simples
Auteur : Ann Yebe Ollomo
Date : Juin 2026
"""

import re
import shutil
from pathlib import Path

# Chemins
SEEDS_DIR = Path(__file__).parent.parent / "airbnb" / "seeds"
INPUT_FILE = SEEDS_DIR / "reviews.csv"
BACKUP_FILE = SEEDS_DIR / "reviews_backup.csv"

# 1. Sauvegarde de l'original
shutil.copy(INPUT_FILE, BACKUP_FILE)
print(f"✅ Backup créé : {BACKUP_FILE}")

# 2. Lecture du fichier
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 3. Nettoyage : remplace les guillemets doubles imbriqués "" par '
original_count = content.count('""')
content_clean = re.sub(r'""([^"]+)""', r"'\1'", content)
new_count = content_clean.count('""')

# 4. Écriture du fichier nettoyé
with open(INPUT_FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content_clean)

print(f"✅ Nettoyage terminé")
print(f"   Occurrences de \"\"...\"\" avant : {original_count}")
print(f"   Occurrences restantes après   : {new_count}")
print(f"   Fichier mis à jour : {INPUT_FILE}")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 15:08:17 2025

@author: gabinbalhan
"""

import pandas as pd

# Charger les fichiers
rsds_file = "/Volumes/evelyn_hv62/rsds_data_raquaypampa/copernicus_data/copernicus_combined_month/rsds_monthly_combined_1981-2010.csv"  # Remplace par le chemin réel
df_rsds = pd.read_csv(rsds_file, sep=",")  # Ajuster le séparateur si nécessaire

change_factor_file = "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/change_factor/change_factor_models_new_ssp585/change_factor_TaiESM1.csv"  # Remplace par le chemin réel
df_cf = pd.read_csv(change_factor_file, sep=",")  # Ajuster le séparateur si nécessaire

# Créer un dictionnaire pour mapper les mois en texte vers leur numéro
mois_map = {
    "Janvier": "01",
    "Février": "02",
    "Mars": "03",
    "Avril": "04",
    "Mai": "05",
    "Juin": "06",
    "Juillet": "07",
    "Août": "08",
    "Septembre": "09",
    "Octobre": "10",
    "Novembre": "11",
    "Décembre": "12"
}

# Liste pour stocker les DataFrames modifiés
modified_rows = []

# Date de départ (2021-01)
start_year = 2021
start_month = 1  # Janvier

# Calcul du nombre total de lignes
total_rows = len(df_rsds)

# Calculer le nombre total de mois
total_months = total_rows  # car chaque ligne correspond à un mois

# Pour chaque ligne, calculer la date correspondante
for index, row in df_rsds.iterrows():
    # Calculer l'année et le mois à partir du nombre total de mois
    year_offset = (start_month + index - 1) // 12  # Décalage d'année
    month_offset = (start_month + index - 1) % 12 + 1  # Mois de 1 à 12
    
    # Créer la nouvelle date au format YYYY-MM
    new_year = start_year + year_offset
    new_month = f"{month_offset:02d}"  # Formater le mois avec deux chiffres (ex : "01", "02", ...)
    new_date = f"{new_year}-{new_month}"

    # Créer une copie de la ligne de données et mettre à jour la date
    df_rsds_copy = row.copy()
    df_rsds_copy["Date"] = new_date
    
    # Appliquer le facteur de changement pour chaque mois
    mois_num = row["Date"].split("-")[1]  # Extraire le mois de la date
    change_factor = df_cf[df_cf["Mois"] == list(mois_map.keys())[int(mois_num)-1]]["Change Factor"].values[0]
    
    # Appliquer le facteur de changement
    df_rsds_copy["RSDS (W/m²)"] *= change_factor
    
    # Arrondir les valeurs de la colonne 'RSDS (W/m²)' à 2 chiffres après la virgule
    df_rsds_copy["RSDS (W/m²)"] = df_rsds_copy["RSDS (W/m²)"].round(2)
    
    # Ajouter la ligne modifiée à la liste
    modified_rows.append(df_rsds_copy)

# Combiner toutes les lignes modifiées
df_modified = pd.DataFrame(modified_rows)

# Sauvegarder le DataFrame modifié dans un fichier CSV
output_file = "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/prediction_mois_model/prediction_2021-2050_TaiESM1_ssp585.csv"  # Remplace par le chemin souhaité
df_modified.to_csv(output_file, index=False)

print(f"Les résultats ont été sauvegardés dans : {output_file}")

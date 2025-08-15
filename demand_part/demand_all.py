#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 30 12:03:46 2026

@author: gabinbalhan
"""
import pandas as pd
import os

# Répertoire racine
root = "/Volumes/evelyn_hv62/part2/demand"

# Dossiers et modèles de noms des fichiers
categories = {
    "cool": f"{root}/cold/ssp585/year_by_year/demand_cold_{{year}}.csv",
    "t_ind": f"{root}/t_ind1st/year_by_year/demand_t_ind_{{year}}.csv",
    #"fan": f"{root}/fan/ssp126/year_by_year/demand_fan_{{year}}.csv"
}

# Répertoire de sortie
output_dir = f"{root}/all/ssp126_1st/year_by_year"
os.makedirs(output_dir, exist_ok=True)

# Boucle sur les années
for year in range(2026, 2046):
    print(f"📦 Traitement de l'année {year}...")

    dfs = []

    for name, path_template in categories.items():
        file_path = path_template.format(year=year)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ Fichier manquant : {file_path}")

        df = pd.read_csv(file_path)
        if not {'Date', 'Minute', 'Load'}.issubset(df.columns):
            raise ValueError(f"❌ Fichier {file_path} n'a pas les colonnes attendues.")

        df = df[['Date', 'Minute', 'Load']].copy()
        df = df.rename(columns={"Load": f"Load_{name}"})
        dfs.append(df)

    # Fusion sur Date et Minute
    df_merged = dfs[0]
    for df in dfs[1:]:
        df_merged = pd.merge(df_merged, df, on=['Date', 'Minute'], how='outer')

    # Remplacer les NaN par 0
    load_cols = [col for col in df_merged.columns if col.startswith("Load_")]
    df_merged[load_cols] = df_merged[load_cols].fillna(0)

    # Somme finale
    df_merged['Load'] = df_merged[load_cols].sum(axis=1)

    # ✅ Arrondi à deux décimales
    df_merged['Load'] = df_merged['Load'].round(2)

    # Tri pour garder l'ordre temporel
    df_merged = df_merged.sort_values(by=["Date", "Minute"])

    # Sauvegarde
    output_path = f"{output_dir}/demand_all_{year}.csv"
    df_merged[['Date', 'Minute', 'Load']].to_csv(output_path, index=False)

    print(f"✅ Fichier 'demand_all_{year}.csv' généré.")

print("🎉 Traitement terminé pour toutes les années.")

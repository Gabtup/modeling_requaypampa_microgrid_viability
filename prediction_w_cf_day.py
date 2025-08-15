#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 11:46:45 2025

@author: gabinbalhan
"""

import pandas as pd

# Charger les données
rsds_df = pd.read_csv(
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/copernicus_data/copernicus_combined_day/rsds_daily_combined_1981-2010.csv",
    parse_dates=["date"],
    sep=","
)
change_factor_df = pd.read_csv(
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/change_factor/change_factor_models_new_ssp585/change_factor_NorESM2-MM.csv",
    sep=","
)

# Associer les noms des mois en français aux valeurs numériques
mois_dict = {
    "Janvier": 1, "Février": 2, "Mars": 3, "Avril": 4, "Mai": 5, "Juin": 6,
    "Juillet": 7, "Août": 8, "Septembre": 9, "Octobre": 10, "Novembre": 11, "Décembre": 12
}
change_factor_df["Mois"] = change_factor_df["Mois"].map(mois_dict)

# Ajouter une colonne Mois à rsds_df pour la fusion
rsds_df["Mois"] = rsds_df["date"].dt.month

# Fusionner les données sur le mois
result_df = rsds_df.merge(change_factor_df, on="Mois")

# Calculer le rsds ajusté et arrondir à 2 décimales
result_df["rsds_adjusted"] = (result_df["rsds"] * result_df["Change Factor"]).round(2)

# Décalage des dates : passer de 1981-01-01 à 2021-01-01
annee_debut = 2021
result_df["date"] = result_df["date"].apply(lambda x: x.replace(year=annee_debut + (x.year - 1981)))

# Trier les données par date
result_df = result_df.sort_values(by="date")

# Renommer les colonnes
result_df = result_df.rename(columns={"date": "Date", "rsds_adjusted": "RSDS (W/m²)"})

# Ne conserver que les colonnes "Date" et "RSDS (W/m²)"
result_df = result_df[["Date", "RSDS (W/m²)"]]

# Enregistrer le résultat dans un fichier CSV
output_path = "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/irradiation/prediction_day_model/prediction_2021-2050_NorESM2-MM_ssp585.csv"
result_df.to_csv(output_path, index=False)

print(f"Fichier CSV enregistré avec succès à : {output_path}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 16:37:31 2025

@author: gabinbalhan
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Liste des fichiers CSV des modèles
rsds_files = [
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_ACCESS-CM2_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_CanESM5_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_CESM2_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_EC-Earth3_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_IPSL-CM6A-LR_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_KACE-1-0-G_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_MIROC6_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_MPI-ESM1-2-HR_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_MPI-ESM1-2-LR_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_MRI-ESM2-0_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_NorESM2-LM_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_NorESM2-MM_ssp585.csv",
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_model_month/prediction_2021-2050_TaiESM1_ssp585.csv"
]

# Fichiers pour les moyennes et les observations
rsds_mean_file = "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/month/prediction_avg_month/prediction_2021-2050_mean_ssp585.csv"
rsds_copernicus_file = "/Volumes/evelyn_hv62/part1/data_raquaypampa/copernicus_data/t/month/avg_month/historical_month_1981-2010.csv"

# Mois en ordre et traduction
ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
french_to_english = {
    'Janvier': 'January', 'Février': 'February', 'Mars': 'March', 'Avril': 'April', 'Mai': 'May', 'Juin': 'June',
    'Juillet': 'July', 'Août': 'August', 'Septembre': 'September', 'Octobre': 'October', 'Novembre': 'November', 'Décembre': 'December'
}

# Chargement des modèles
df_list = []
for file in rsds_files:
    df = pd.read_csv(file, usecols=["Mois", "Moyenne"])
    df["Mois"] = df["Mois"].map(french_to_english).fillna(df["Mois"])
    df["Mois"] = pd.Categorical(df["Mois"], categories=ordered_months, ordered=True)
    df.sort_values("Mois", inplace=True)
    df_list.append(df)

# Chargement des données de moyenne et observation
df_mean = pd.read_csv(rsds_mean_file, usecols=["Mois", "T(°C)"])
df_obs = pd.read_csv(rsds_copernicus_file, usecols=["Mois", "Moyenne"])

for df in [df_mean, df_obs]:
    df["Mois"] = df["Mois"].map(french_to_english).fillna(df["Mois"])
    df["Mois"] = pd.Categorical(df["Mois"], categories=ordered_months, ordered=True)
    df.sort_values("Mois", inplace=True)

# Construction DataFrame combiné
df_combined = df_list[0][["Mois"]].copy()
for i, df in enumerate(df_list):
    df_combined[f"temp_{i+1}"] = df["Moyenne"].values

df_combined["temp_mean"] = df_mean["T(°C)"].values
df_combined["temp_obs"] = df_obs["Moyenne"].values

# Calcul incertitude min/max
model_temp_cols = [f"temp_{i+1}" for i in range(len(df_list))]
df_combined["temp_min"] = df_combined[model_temp_cols].min(axis=1)
df_combined["temp_max"] = df_combined[model_temp_cols].max(axis=1)

# Plot
plt.figure(figsize=(18, 10))
plt.plot(df_combined["Mois"], df_combined["temp_mean"], color='black', linestyle='-', linewidth=2,
         label="Model Mean SSP5-8.5 (2026–2045)")
plt.fill_between(df_combined["Mois"], df_combined["temp_min"], df_combined["temp_max"],
                 color='gray', alpha=0.3, label="Inter-modèles Uncertainty SSP5-8.5 (min-max)")
plt.plot(df_combined["Mois"], df_combined["temp_obs"], color='black', linestyle='--', linewidth=2,
         label="Observation (1981–2000)")

# Titres et tailles
plt.xlabel("Month", fontsize=24)
plt.ylabel(r"RSDS (W/m$^2$)", fontsize=24)
plt.xticks(rotation=45, fontsize=20)
plt.yticks(fontsize=20)

# Légende agrandie
plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=3, fontsize=18)
plt.xlim("January", "December")
plt.ylim(180,280)

plt.grid(axis='y')
plt.tight_layout()

# Enregistrement
plt.savefig("/Volumes/evelyn_hv62/part1/plot/rsds_plot_with_uncertainty_ssp585.pdf",
            format="pdf", dpi=300, bbox_inches="tight")
plt.show()


# Moyennes annuelles
mean_future = df_combined["temp_mean"].mean()
print(mean_future)
mean_historical = df_combined["temp_obs"].mean()

# Différence absolue et relative
absolute_increase = mean_future - mean_historical
relative_increase_percent = (absolute_increase / mean_historical) * 100

# Affichage
print(f"Moyenne RSDS future (2026–2045) : {mean_future:.2f} W/m²")
print(f"Moyenne RSDS historique (1981–2000) : {mean_historical:.2f} W/m²")
print(f"Augmentation absolue : {absolute_increase:.2f} W/m²")
print(f"Augmentation relative : {relative_increase_percent:.2f} %")


"""
import pandas as pd
import matplotlib.pyplot as plt

# Liste des fichiers CSV des modèles
rsds_files = [
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_ACCESS-CM2_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/imoyennes_mensuelles_2021-2050_CanESM5_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/imoyennes_mensuelles_2021-2050_CESM2_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/imoyennes_mensuelles_2021-2050_EC-Earth3_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_IPSL-CM6A-LR_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_KACE-1-0-G_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_MIROC6_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_MPI-ESM1-2-HR_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_MPI-ESM1-2-LR_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_MRI-ESM2-0_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_NorESM2-LM_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_NorESM2-MM_ssp585.csv",
    "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/i/moyennes_mensuelles_2021-2050_TaiESM1_ssp585.csv"
]

# Fichiers des moyennes et observations
rsds_mean_file = "/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/prediction/ssp_585/prediction_moyenne/moyennes_mensuelles_2021-2050_mean_ssp585.csv"
rsds_copernicus_file = "/Volumes/evelyn_hv62/rsds_data_raquaypampa/copernicus_data/moyenne_mensuelle_copernicus/moyennes_mensuelles_1981-2010.csv"

# Définir l'ordre des mois
mois_ordonne = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

# Charger et traiter les fichiers des modèles
df_list = []
for file in rsds_files:
    df = pd.read_csv(file, sep=",", usecols=["Mois", "Moyenne"])
    df["Mois"] = pd.Categorical(df["Mois"], categories=mois_ordonne, ordered=True)
    df.sort_values("Mois", inplace=True)
    df_list.append(df)

# Charger et traiter les moyennes et observations
df_mean = pd.read_csv(rsds_mean_file, sep=",", usecols=["Mois", "Moyenne"])
df_obs = pd.read_csv(rsds_copernicus_file, sep=",", usecols=["Mois", "Moyenne"])
for df in [df_mean, df_obs]:
    df["Mois"] = pd.Categorical(df["Mois"], categories=mois_ordonne, ordered=True)
    df.sort_values("Mois", inplace=True)

# Construire le DataFrame combiné
df_combined = df_list[0][["Mois"]].copy()
for i, df in enumerate(df_list):
    df_combined[f"RSDS_{i+1}"] = df["Moyenne"].values

df_combined["RSDS_mean"] = df_mean["Moyenne"].values
df_combined["RSDS_obs"] = df_obs["Moyenne"].values

df_combined["RSDS_min"] = df_combined.iloc[:, 1:-2].min(axis=1)
df_combined["RSDS_max"] = df_combined.iloc[:, 1:-2].max(axis=1)

# Tracer le graphique
plt.figure(figsize=(12, 6))
plt.fill_between(df_combined["Mois"], df_combined["RSDS_min"], df_combined["RSDS_max"], color='gray', alpha=0.3, label="Inter-model Uncertainty ssp585 (Min-Max Range)")
plt.plot(df_combined["Mois"], df_combined["RSDS_mean"], color='black', linestyle='-', linewidth=2, label="Model Mean ssp585 (2021-2050)")
plt.plot(df_combined["Mois"], df_combined["RSDS_obs"], color='black', linestyle='--', linewidth=2, label="Observation (1981-2010)")

# Personnalisation
plt.xlabel("Mois")
plt.ylabel("RSDS (W/m²)")
plt.title("Comparison of statistical downscaling methods for climate change impact analysis (ssp585)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Sauvegarde et affichage
plt.savefig("/Volumes/evelyn_hv62/rsds_data_raquaypampa/rsds_plot_with_uncertainty.pdf", format="pdf", dpi=300)
plt.show()

"""
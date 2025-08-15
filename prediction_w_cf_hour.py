#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 17:55:03 2025

@author: gabinbalhan
"""
"""
import csv
from datetime import datetime

# === Lire le fichier de facteurs mensuels ===
change_factors = {}
with open('/Volumes/evelyn_hv62/part1/data_raquaypampa/stats/change_factor/change_factor_models_new_ssp126/change_factor_CanESM5.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        mois = row['Mois'].strip().lower()
        facteur = float(row['Change Factor'])
        change_factors[mois] = facteur

# === Correspondance nom du mois → numéro de mois ===
mois_to_num = {
    'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
    'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
    'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
}

# === Lire le fichier horaire et appliquer les facteurs ===
input_file = '/Volumes/evelyn_hv62/part1/data_raquaypampa/copernicus_data/irradiation/copernicus_combined_hour/rsds_hourly_combined.csv'
output_file = '/Volumes/evelyn_hv62/part1/data_raquaypampa/stats/prediction/ssp_126/irradiation/prediction_hour_model/prediction_2021-2050_CanESM5_ssp126.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["Date (UTC−4)", "RSDS (W/m²)"])

    for row in reader:
        date_str = row['Date (UTC−4)']
        rsds = float(row['Rayonnement solaire (W/m²)'])

        date_obj = datetime.fromisoformat(date_str)
        mois_num = date_obj.month

        # Récupérer le facteur du mois
        for nom_mois, num in mois_to_num.items():
            if mois_num == num:
                facteur = change_factors[nom_mois]
                break

        rsds_adjusted = round(rsds * facteur, 2)
        writer.writerow([date_str, rsds_adjusted])

print(f"✅ Nouveau fichier exporté : {output_file}")
"""
import csv
from datetime import datetime
import pandas as pd

# === Lire les facteurs de changement mensuels ===
change_factors = {}
with open('/Volumes/evelyn_hv62/part1/data_raquaypampa/stats/change_factor/change_factor_models_new_ssp585/change_factor_NorESM2-MM.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        mois = row['Mois'].strip().lower()
        facteur = float(row['Change Factor'])
        change_factors[mois] = facteur

# === Correspondance mois (français) → numéro ===
mois_to_num = {
    'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
    'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
    'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
}
num_to_mois = {v: k for k, v in mois_to_num.items()}

# === Générer toutes les dates horaires entre 2021 et 2050 ===
start_date = pd.Timestamp('2021-01-01 00:00:00', tz='America/La_Paz')
end_date = pd.Timestamp('2050-12-31 23:00:00', tz='America/La_Paz')
all_dates = pd.date_range(start=start_date, end=end_date, freq='H')

# === Lire les données horaires initiales (1981–2010) ===
input_file = '/Volumes/evelyn_hv62/part1/data_raquaypampa/copernicus_data/irradiation/copernicus_combined_hour/rsds_hourly_combined.csv'
original_df = pd.read_csv(input_file)
original_rsds = original_df['Rayonnement solaire (W/m²)'].tolist()

# === Étendre les données initiales cycliquement ===
repeats = len(all_dates) // len(original_rsds) + 1
extended_rsds = (original_rsds * repeats)[:len(all_dates)]

# === Appliquer les facteurs mensuels et écrire le fichier de sortie ===
output_file = '/Volumes/evelyn_hv62/part1/data_raquaypampa/stats/prediction/ssp_585/irradiation/prediction_hour_model/prediction_2021-2050_NorESM2-MM_ssp585.csv'
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Date (UTC−4)", "RSDS (W/m²)"])

    for dt, rsds in zip(all_dates, extended_rsds):
        mois_nom = num_to_mois[dt.month]
        facteur = change_factors[mois_nom]
        rsds_corr = round(float(rsds) * facteur, 2)
        formatted_date = dt.strftime('%Y-%m-%dT%H:%M:%S-04:00')
        writer.writerow([formatted_date, rsds_corr])

print(f"✅ Fichier exporté : {output_file}")


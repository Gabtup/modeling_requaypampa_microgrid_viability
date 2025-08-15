#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 14:38:24 2025

@author: gabinbalhan
"""

import pandas as pd

# Chargement des fichiers CSV
file1 = pd.read_csv("/Volumes/evelyn_hv62/rsds_data_raquaypampa/historical/moyennes_mensuelles_1981-2010/moyennes_mensuelles_ACCESS-CM2.csv", sep=",")
file2 = pd.read_csv("/Volumes/evelyn_hv62/rsds_data_raquaypampa/prediction_ssp126/moyennes_mensuelles_2021-2050/moyennes_mensuelles_ACCESS-CM2.csv", sep=",")

# Conversion des valeurs des moyennes en float pour effectuer les calculs
file1['Moyenne'] = file1['Moyenne'].astype(float)
file2['Moyenne'] = file2['Moyenne'].astype(float)

# Calcul du ratio (change factor) pour chaque mois et arrondi à 2 décimales
file1['Change Factor'] = (file2['Moyenne'] / file1['Moyenne']).round(2)

# Sauvegarde du résultat dans un nouveau fichier CSV
file1[['Mois', 'Change Factor']].to_csv("/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/change_factor/change_factor_models_new_ssp126/change_factor_ACCESS-CM2.csv", index=False)

print("Le fichier avec les facteurs de changement a été créé avec succès.")

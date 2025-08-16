#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 14:38:24 2025

@author: gabinbalhan
"""

import pandas as pd

# Load CSV files
file1 = pd.read_csv("/Volumes/evelyn_hv62/rsds_data_raquaypampa/historical/moyennes_mensuelles_1981-2010/moyennes_mensuelles_ACCESS-CM2.csv", sep=",")
file2 = pd.read_csv("/Volumes/evelyn_hv62/rsds_data_raquaypampa/prediction_ssp126/moyennes_mensuelles_2021-2050/moyennes_mensuelles_ACCESS-CM2.csv", sep=",")

# Conversion of mean values to float for calculation purposes.
file1['Moyenne'] = file1['Moyenne'].astype(float)
file2['Moyenne'] = file2['Moyenne'].astype(float)

# Calculation of the change factor for each month, rounded to two decimal places.
file1['Change Factor'] = (file2['Moyenne'] / file1['Moyenne']).round(2)

# Saving the result to a new CSV file
file1[['Mois', 'Change Factor']].to_csv("/Volumes/evelyn_hv62/rsds_data_raquaypampa/stats/change_factor/change_factor_models_new_ssp126/change_factor_ACCESS-CM2.csv", index=False)

print("The file containing the change factors was successfully created.")

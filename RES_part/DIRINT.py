#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 10:49:55 2025

@author: gabinbalhan
"""

import pandas as pd
import pvlib
import numpy as np

# === 1. Charger les données ===
fichier = '/Volumes/evelyn_hv62/part3/data/RES/i/i_global/ssp585/i_2026.csv'

df = pd.read_csv(fichier, parse_dates=['Date'])
df = df.rename(columns={'Date': 'datetime'})
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.set_index('datetime')

# Renommer la colonne GHI
df = df.rename(columns={'RSDS (W/m²)': 'GHI'})

# === 2. Paramètres du site ===
latitude = -18.2
longitude = -64.62

# === 3. Position du soleil ===
solar_position = pvlib.solarposition.get_solarposition(
    time=df.index,
    latitude=latitude,
    longitude=longitude
)
df['zenith'] = solar_position['zenith']

# === 4. DHI/DNI avec modèle DIRINT ===
dni = pvlib.irradiance.dirint(
    ghi=df['GHI'],
    solar_zenith=df['zenith'],
    times=df.index,
    pressure=101325.0,
    use_delta_kt_prime=True,
    temp_dew=None,
    min_cos_zenith=0.4,
    max_zenith=87
)

# Remplacer les NaN éventuels par 0 (par exemple avant le lever du soleil)
dni = dni.fillna(0)
df['DNI'] = dni

# Calculer DHI à partir de : GHI = DHI + DNI * cos(zenith)
df['DHI'] = df['GHI'] - df['DNI'] * np.cos(np.radians(df['zenith']))
df['DHI'] = df['DHI'].clip(lower=0)  # éviter valeurs négatives

# === 5. Irradiation diffuse annuelle ===
energie_diffuse_Whm2 = df['DHI'].sum()
energie_diffuse_kWhm2 = energie_diffuse_Whm2 / 1000

# === 6. Affichage + Export ===
print(f"Irradiation diffuse annuelle : {energie_diffuse_kWhm2:.2f} kWh/m²")
print(df.head(24))

# Export
df.round(2).to_csv('/Volumes/evelyn_hv62/part3/data/RES/i/i_isotropic/ssp585/i_2026.csv')

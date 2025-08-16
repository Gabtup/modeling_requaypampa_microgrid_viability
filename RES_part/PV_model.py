import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import pvlib
import numpy as np

# === Geographic coordinates (Raquay Pampa)
lat, lon = -18.2, -64.62

# === Load the local TMY3 file
df = pd.read_csv("/Volumes/evelyn_hv62/part3/data/RES/pv_lib/ssp126/pv_2026.csv", sep=';', skiprows=2, skipfooter=0)
#df = df.iloc[:, 1:]
#print(df['T2m'])
df = df.iloc[:8760]
df.index = pd.date_range("2026-01-01 00:00", periods=8760, freq="H", tz="Etc/GMT+4")
print(df.columns.tolist())  # Vérifie les noms
# === Rename columns for consistency

df.rename(columns={
    'GHI': 'ghi',
    'DHI': 'dhi',
    'DNI': 'dni',
    'Temperature': 'temp_air',
    'Wind Speed': 'wind_speed',
    'Pressure': 'air_pressure'
}, inplace=True)

# === Remove negative irradiance values
for col in ['ghi', 'dni', 'dhi']:
    df[col] = df[col].clip(lower=0)

# === Compute solar position
solpos = pvlib.solarposition.get_solarposition(df.index, lat, lon)
# === 6. Define PV system parameters
tilt = 18
azimuth = 0
pdc0 = 250
gamma_pdc = -0.0043
NOCT = 45

# === Calculate POA irradiance (isotropic model)
poa = pvlib.irradiance.get_total_irradiance(
    surface_tilt=tilt,
    surface_azimuth=azimuth,
    solar_zenith=solpos['zenith'],
    solar_azimuth=solpos['azimuth'],
    dni=df['dni'],
    ghi=df['ghi'],
    dhi=df['dhi'],
    model='isotropic',
    albedo=0.2
)['poa_global'].clip(lower=0)

# === Estimate cell temperature using NOCT model
cell_temp = df['temp_air'] + ((NOCT - 20) / 800) * poa

# === Compute DC output using PVWatts model
dc_power = pvlib.pvsystem.pvwatts_dc(
    g_poa_effective=poa,
    temp_cell=cell_temp,
    pdc0=pdc0,
    gamma_pdc=gamma_pdc
)

# === Export DC power production (timestamp index)
df_prod = pd.DataFrame({
    'Production_DC_W': dc_power.values
}, index=dc_power.index.tz_localize(None))
df_prod.dropna(inplace=True)
df_prod.to_csv("/Volumes/evelyn_hv62/part3/data/RES/PV_prod/ssp126/2026/Production_PV_DC_Watts.csv", index_label="Hour")

print(" PV production files successfully saved.")


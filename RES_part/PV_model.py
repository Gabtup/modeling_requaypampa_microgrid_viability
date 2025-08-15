import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import pvlib
import numpy as np

# === 1. Geographic coordinates (Raquay Pampa)
lat, lon = -18.2, -64.62

# === 2. Load the local TMY3 file
df = pd.read_csv("/Volumes/evelyn_hv62/part3/data/RES/pv_lib/ssp126/pv_2026.csv", sep=';', skiprows=2, skipfooter=0)
#df = df.iloc[:, 1:]
#print(df['T2m'])
df = df.iloc[:8760]
df.index = pd.date_range("2026-01-01 00:00", periods=8760, freq="H", tz="Etc/GMT+4")
print(df.columns.tolist())  # Vérifie les noms
# === 3. Rename columns for consistency

df.rename(columns={
    'GHI': 'ghi',
    'DHI': 'dhi',
    'DNI': 'dni',
    'Temperature': 'temp_air',
    'Wind Speed': 'wind_speed',
    'Pressure': 'air_pressure'
}, inplace=True)

# === 4. Remove negative irradiance values
for col in ['ghi', 'dni', 'dhi']:
    df[col] = df[col].clip(lower=0)

# === 5. Compute solar position
solpos = pvlib.solarposition.get_solarposition(df.index, lat, lon)
# === 6. Define PV system parameters
tilt = 18
azimuth = 0
pdc0 = 250
gamma_pdc = -0.0043
NOCT = 45

# === 7. Calculate POA irradiance (isotropic model)
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

# === 8. Estimate cell temperature using NOCT model
cell_temp = df['temp_air'] + ((NOCT - 20) / 800) * poa

# === 9. Compute DC output using PVWatts model
dc_power = pvlib.pvsystem.pvwatts_dc(
    g_poa_effective=poa,
    temp_cell=cell_temp,
    pdc0=pdc0,
    gamma_pdc=gamma_pdc
)

# === 10. Plot DC production for March 12–14
df_sim = pd.DataFrame({
    'POA (W/m²)': poa,
    'Ambient Temperature (°C)': df['temp_air'],
    'Cell Temperature (°C)': cell_temp,
    'DC Power (W)': dc_power
}, index=df.index)

df_3days = df_sim.loc["2026-01-01":"2026-01-03"]

plt.figure(figsize=(7, 4))
df_3days['DC Power (W)'].plot(label='DC Power', color='green')
plt.ylabel("DC Power (W)")
plt.xlabel("Time (UTC-4)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/Volumes/evelyn_hv62/part3/data/RES/PV_prod/ssp126/2026/Simulation_PV_days.png", dpi=300)
plt.show()

# === 11. Plot GHI and ambient temperature (hourly)
mpl.rcParams.update(mpl.rcParamsDefault)
df.index = df.index.tz_localize(None)

fig, ax1 = plt.subplots(figsize=(7, 4))
ax1.plot(df.index, df['ghi'], color='blue', linewidth=0.5)
ax1.set_ylabel("GHI (W/m²)", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.plot(df.index, df['temp_air'], color='red', linewidth=0.5)
ax2.set_ylabel("Ambient Temperature (°C)", color='red')
ax2.tick_params(axis='y', labelcolor='red')

ax1.set_xlim(df.index[0], df.index[-1])
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax1.set_xlabel("Month (TMY year)")
fig.legend(['GHI', 'Ambient Temperature'], loc='upper left', fontsize=12)
plt.tight_layout()
plt.savefig("/Volumes/evelyn_hv62/part3/data/RES/PV_prod/ssp126/2026/GHI_AmbientTemperature_TMY_Hourly.png", dpi=400)
plt.show()

# === 12. Plot POA and cell temperature (hourly)
fig, ax1 = plt.subplots(figsize=(7, 4))
ax1.plot(df.index, poa, color='purple', linewidth=0.5)
ax1.set_ylabel("POA (W/m²)", color='purple')
ax1.tick_params(axis='y', labelcolor='purple')

ax2 = ax1.twinx()
ax2.plot(df.index, cell_temp, color='orange', linewidth=0.5)
ax2.set_ylabel("Cell Temperature (°C)", color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

ax1.set_xlim(df.index[0], df.index[-1])
ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax1.set_xlabel("Month (TMY year)")
fig.legend(['POA', 'Cell Temperature'], loc='upper left', fontsize=12)
plt.tight_layout()
plt.savefig("/Volumes/evelyn_hv62/part3/data/RES/PV_prod/ssp126/2026/POA_CellTemperature_TMY_Hourly.png", dpi=400)
plt.show()

# === 13. Export DC power production (timestamp index)
df_prod = pd.DataFrame({
    'Production_DC_W': dc_power.values
}, index=dc_power.index.tz_localize(None))
df_prod.dropna(inplace=True)
df_prod.to_csv("/Volumes/evelyn_hv62/part3/data/RES/PV_prod/ssp126/2026/Production_PV_DC_Watts.csv", index_label="Hour")
df_prod.to_excel("/Volumes/evelyn_hv62/part3/data/RES/PV_prod/ssp126/2026/Production_PV_DC_Watts.xlsx", index_label="Hour")

# === 14. Export DC power production (numeric index 1–8760)
df_prod_num = pd.DataFrame({
    'Hour': range(1, 8761),
    'Production_DC_W': dc_power.values
})
df_prod_num.dropna(inplace=True)
df_prod_num.to_csv("/Volumes/evelyn_hv62/part3/data/RES/PV_prod/ssp126/2026/Production_PV_DC_Watts_numeric.csv", index=False)
df_prod_num.to_excel("/Volumes/evelyn_hv62/part3/data/RES/PV_prod/ssp126/2026/Production_PV_DC_Watts_numeric.xlsx", index=False)

print(" PV production files successfully saved.")

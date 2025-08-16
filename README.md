# Requaypampa microgrid viability modelisation
This repository provides access to the codes and data used in a feasibility analysis of a microgrid in Raquaypampa, Bolivia, under various socio-economic contexts (SSP5 and SSP1). It contains four files, each representing one of the successive stages in the microgrid modeling process, presented in sequential order.

# Climatical_part
This folder contains all the codes and compiled results related to climate data processing for the microgrid feasibility study.

* **Codes:**
  - `change_factor`: calculates the change factor between historical and future climate models.
  - `prediction_w_cf_day`, `prediction_w_cf_hour`, `prediction_w_cf_month`: generate future climate predictions adjusted using the calculated change factor and Copernicus data.

* **Subfolders:**
  - `model`: contains monthly historical data and monthly SSP1 and SSP5 future data for each climate model at Raquaypampa.
  - `copernicus`: contains the historical observed climate data for Raquaypampa.
  - `change_factor`: contains the change factor results for each climate model, under each socio-economic scenario.
  - `prediction`: contains the future climate predictions for each model, along with their averaged values.

# Demand_part
This folder contains the electricity demand results for the community under the two socio-economic scenarios. It also includes the codes used to generate these results.

* **Codes:**
  - `cold_storage`: models thermal storage appliances (refrigerators, freezers) that depend on temperature prediction files for each socio-economic scenario.
  - `t_ind+fan`: models all other appliances that do not depend on temperature predictions, as well as the fans, which are influenced by temperature predictions.
  - `demand_all`: aggregates the results from the two previous codes to simulate the community’s total electricity demand.

* **Subfolders:** contain the output of the `demand_all` code, providing annual electricity demand profiles for each socio-economic scenario.

# RES_part
This folder contains the codes and resulting data required to develop the photovoltaic production profile of the microgrid for both the sunniest year (max.) and the least sunny year (min.) of each SSP.

* **Codes:**
  - `DIRINT`: decomposes Global Horizontal Irradiance (GHI) into Direct Normal Irradiance (DNI) and Diffuse Horizontal Irradiance (DHI).
  - `PV_model`: estimates the electrical output of a photovoltaic (PV) panel by combining its specified characteristics, ambient temperature, and the decomposed components of GHI.

* **Subfolders:**
  - `irradiation`, `temperature`: provide the maximum and minimum irradiation values and corresponding temperatures for each scenario.
  - `pv_input`: structured as inputs for `PV_model`, with adjusted max/min irradiation and temperature values.
  - `PV_prod`: contains the defined PV panel electrical production for each scenario.

# Microgrid_part
Contains input data required to model the microgrid using microgridspy (https://microgridspy/documentation.readthedocs.io/en/latest/index.html) and the simulation results.

* **Subfolders:**
  - `Demand_Time_Series` and `RES_Time_Series`: hourly profiles of electricity demand and renewable energy production for each SSP.
  - `results`: summary of simulation results and dispatch profiles. Organized by max/min irradiation years. Two diesel generator formulations are used: Linear Programming (LP) and Mixed-Integer Linear Programming for a 10 kW nominal generator (MILP_10k).

---
# Contact

For questions, feedback, or collaboration inquiries, please contact gabin.balhan@uliege.be

# modeling_requaypampa_microgrid_viability
This repository provides access to the codes and data used in a feasibility analysis of a microgrid in Raquaypampa, Bolivia, under various socio-economic contexts (SSP5 and SSP1). It contains four files, each representing one of the successive stages in the microgrid modeling process, presented in sequential order.

climatical_part:

This folder contains all the codes and compiled results related to climate data processing for the microgrid feasibility study.

  * Codes:
    - change_factor: calculates the change factor between historical and future climate models.
    - prediction_w_cf_day, prediction_w_cf_hour, prediction_w_cf_month: generate future climate predictions adjusted using the calculated change factor and copernicus data.

  * Subfolders:
    - model: contains monthly historical data and monthly SSP1 and SSP5 futur data for each climate model at Raquaypampa.
    - copernicus: ontains the historical observed climate data for Raquaypampa.
    - change_factor: contains the change factor results for each climate model, under each socio-economic scenario.
    - prediction: contains the future climate predictions for each model, along with their averaged values.

demand_part:

This folder contains the electricity demand results for the community under the two socio-economic scenarios. It also includes the codes used to generate these results.

  * Codes:
    - cold_storage: models thermal storage appliances (refrigerators, freezers) that depend on temperature prediction files for each socio-economic scenario.
    - t_ind+fan: models all other appliances that do not depend on temperature predictions, as well as the village fans, which are influenced by temperature predictions.
    - demand_all: aggregates the results from the two previous codes to simulate the village’s total electricity demand.

  * The subfolders contain the output of the demand_all code, providing annual electricity demand profiles for each socio-economic scenario.

RES_part:

This folder contains the codes and data required to develop the photovoltaic production profile of the microgrid.






# modeling_requaypampa_microgrid_viability
This repository provides access to the codes and data used in a feasibility analysis of a microgrid in Raquaypampa, Bolivia, under various socio-economic contexts (SSP5 and SSP1). It contains four files, each representing one of the successive stages in the microgrid modeling process, presented in sequential order.

climatical_part:

This folder contains all the codes and compiled results related to climate data processing for the microgrid feasibility study.

  * Codes:
    - change_factor: calculates the change factor between historical and future climate models.
    - prediction_w_cf_day, prediction_w_cf_hour, prediction_w_cf_month: generate future climate predictions adjusted using the calculated change factor.

  * Subfolders :
    - change_factor: contains the change factor results for each climate model, under each socio-economic scenario.
    - prediction: contains the future climate predictions for each model, along with their averaged values.

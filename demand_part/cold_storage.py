#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 23:02:16 2025

@author: gabinbalhan
"""
import numpy as np
import pandas as pd
from ramp import User, UseCase
from tqdm import tqdm

# === Load temperature data === 
temperature_df = pd.read_csv(
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp_126/t/mean_temperature_hourly/temperature_hourly_2026-2045.csv", 
    parse_dates=["datetime"]
)

temperature_df["date"] = temperature_df["datetime"].dt.date
temperature_df["year"] = temperature_df["datetime"].dt.year

# Param. fridge
eta_fridge = 0.6
U_fridge = 0.75
A_fridge = 6.2

# Param. fridge shop
eta_fridge_s = 0.3
U_fridge_s = 0.75
A_fridge_s = 4.83

# Param. fridge shop
eta_fridge_h = 0.3
U_fridge_h = 1.05
A_fridge_h = 4.42

# Param. freezer shop
eta_freezer = 0.6
U_freezer = 0.42
A_freezer = 4.18

i = 0  # Index for annual growth

for year in tqdm(sorted(temperature_df["year"].unique()), desc="Simulation annuelle"):
    Fridge_cold = []

    year_df = temperature_df[temperature_df["year"] == year]
    
    for current_date in year_df["date"].unique():
        daily_df = year_df[year_df["date"] == current_date]
        hourly_temperatures = daily_df["T(°C)"].values

        if len(hourly_temperatures) != 24:
            print(f"⚠️ Températures incomplètes pour {current_date}, jour ignoré.")
            continue
        
        f_share = 0.25 + ( (1.0 - 0.25) / 19 ) * i
        
        temperatures_minute = np.repeat(hourly_temperatures, 60)
        nb_minutes = len(temperatures_minute) # 1440 minutes

        nb_fridges = int(125 * 1.002**i * f_share)
        F = User("Fridge", nb_fridges)
        
        nb_fridges_h = 1 # hospital
        F_h = User("Fridge Shop", nb_fridges_h)
        
        nb_fridges_s = 7 # shop + resto
        F_s = User("Fridge Shop", nb_fridges_s)
        
        nb_freezer = 5
        C = User("Freezer Shop", nb_freezer)
        
        # FRIDGE HOUSEHOLD 
        for start_minute in range(0, nb_minutes, 30):
            end_minute = start_minute + 30
            index_temp = end_minute - 1
            temp = temperatures_minute[index_temp]
            
            T_evap_fridge = 267.15 #[K] (pinch of 5°C)
            T_cond_fridge = (temp + 10) + 273.15  #[K] pinch of 5°C
            
            T_lim = 17 #[°C] room temp cannot be below

            if temp >= T_lim : 
                cop_fridge = (T_evap_fridge/(T_cond_fridge-T_evap_fridge))*eta_fridge
                delt_T_fridge = (temp - 4)
            
            else : 
                cop_fridge = (T_evap_fridge/((T_lim + 10 + 273.15)-T_evap_fridge))*eta_fridge
                delt_T_fridge = (T_lim - 4)                
            
            
            Q_ech_fridge = U_fridge*A_fridge*delt_T_fridge
            W_el_fridge = Q_ech_fridge/cop_fridge 
            t_fridge = round(((W_el_fridge*30)-150)/195)
            
            # Apply a power factor depending on the time of day
            power_multiplier = 1.2 if 360 <= start_minute <= 480 or 1080 <= start_minute <= 1200 else 1
            power_fridge = int(200 * power_multiplier)
            
            fridge = F.add_appliance(
                name="Fridge",
                number= 1,
                power=power_fridge,
                num_windows=1,
                func_time=30,
                time_fraction_random_variability=0,
                func_cycle=20,
                fixed="yes",
                fixed_cycle=1,
                )
            fridge.windows([start_minute, end_minute])
            
            
            if t_fridge >= 5:
                fridge.specific_cycle_1(p_11=200 * power_multiplier, t_11=5, p_12=5 * power_multiplier, t_12=25, r_c1=0)
            elif t_fridge >= 4:
                fridge.specific_cycle_1(p_11=200 * power_multiplier, t_11=4, p_12=5 * power_multiplier, t_12=26, r_c1=0)
            elif t_fridge >= 3:
                fridge.specific_cycle_1(p_11=200 * power_multiplier, t_11=3, p_12=5 * power_multiplier, t_12=27, r_c1=0)
            elif t_fridge >= 2:
                fridge.specific_cycle_1(p_11=200 * power_multiplier, t_11=2, p_12=5 * power_multiplier, t_12=28, r_c1=0)
            elif t_fridge >= 1:
                fridge.specific_cycle_1(p_11=200 * power_multiplier, t_11=1, p_12=5 * power_multiplier, t_12=29, r_c1=0)
                
                
        # FRIDGE SHOP
        for start_minute in range(0, nb_minutes, 30):
            end_minute = start_minute + 30
            index_temp = end_minute - 1
            temp = temperatures_minute[index_temp]
            
            T_evap_fridge = 267.15 #[K] (pinch of 5°C)
            T_cond_fridge = (temp + 10) + 273.15  #[K] pinch of 5°C
            
            T_lim = 15 #[°C] room temp cannot be below

            if temp >= T_lim : 
                cop_fridge = (T_evap_fridge/(T_cond_fridge-T_evap_fridge))*eta_fridge_s
                delt_T_fridge = (temp - 4)
            
            else : 
                cop_fridge = (T_evap_fridge/((T_lim + 10 + 273.15)-T_evap_fridge))*eta_fridge_s
                delt_T_fridge = (T_lim - 4)            
            
            Q_ech_fridge = U_fridge_s*A_fridge_s*delt_T_fridge
            W_el_fridge = Q_ech_fridge/cop_fridge 
            t_fridge = round(((W_el_fridge*30)-150)/315)
            
            
            # Apply a power factor depending on the time of day
            power_multiplier = 1.4 if 480 <= start_minute <= 1200 else 1
            power_fridge = int(320 * power_multiplier)
            
            fridge = F_s.add_appliance(
                name="Fridge shop",
                number= 1,
                power=power_fridge,
                num_windows=1,
                func_time=30,
                time_fraction_random_variability=0,
                func_cycle=20,
                fixed="yes",
                fixed_cycle=1,
                )
            fridge.windows([start_minute, end_minute])
            
            if t_fridge >= 5:
                fridge.specific_cycle_1(p_11=320 * power_multiplier, t_11=5, p_12=5 * power_multiplier, t_12=25, r_c1=0)
            elif t_fridge >= 4:
                fridge.specific_cycle_1(p_11=320 * power_multiplier, t_11=4, p_12=5 * power_multiplier, t_12=26, r_c1=0)
            elif t_fridge >= 3:
                fridge.specific_cycle_1(p_11=320 * power_multiplier, t_11=3, p_12=5 * power_multiplier, t_12=27, r_c1=0)
            elif t_fridge >= 2:
                fridge.specific_cycle_1(p_11=320 * power_multiplier, t_11=2, p_12=5 * power_multiplier, t_12=28, r_c1=0)
            elif t_fridge >= 1:
                fridge.specific_cycle_1(p_11=320 * power_multiplier, t_11=1, p_12=5 * power_multiplier, t_12=29, r_c1=0)
                
        
        # FRIDGE HOSPITAL
        for start_minute in range(0, nb_minutes, 30):
            end_minute = start_minute + 30
            index_temp = end_minute - 1
            temp = temperatures_minute[index_temp]
            
            T_evap_fridge = 267.15 #[K] (pinch of 10°C)
            T_cond_fridge = (temp + 10) + 273.15  #[K] pinch of 10°C
            
            T_lim = 21 #[°C] room temp cannot be below

            if temp >= T_lim : 
                cop_fridge = (T_evap_fridge/(T_cond_fridge-T_evap_fridge))*eta_fridge_s
                delt_T_fridge = (temp - 4)
            
            else : 
                cop_fridge = (T_evap_fridge/((T_lim + 10 + 273.15)-T_evap_fridge))*eta_fridge_s
                delt_T_fridge = (T_lim - 4)            
            
            Q_ech_fridge = U_fridge_h*A_fridge_h*delt_T_fridge
            W_el_fridge = Q_ech_fridge/cop_fridge 
            t_fridge = round(((W_el_fridge*30)-150)/261)
            
            # Apply a power factor depending on the time of day
            power_multiplier = 1.45 if 480 <= start_minute <= 1080 else 1
            power_fridge = int(281 * power_multiplier)
            
            fridge = F_s.add_appliance(
                name="Fridge hospital",
                number= 1,
                power=power_fridge,
                num_windows=1,
                func_time=30,
                time_fraction_random_variability=0,
                func_cycle=20,
                fixed="yes",
                fixed_cycle=1,
                )
            fridge.windows([start_minute, end_minute])
            
            
            if t_fridge >= 4:
                fridge.specific_cycle_1(p_11=281 * power_multiplier, t_11=4, p_12=20 * power_multiplier, t_12=26, r_c1=0)
            elif t_fridge >= 3:
                fridge.specific_cycle_1(p_11=281 * power_multiplier, t_11=3, p_12=20 * power_multiplier, t_12=27, r_c1=0)
            elif t_fridge >= 2:
                fridge.specific_cycle_1(p_11=281 * power_multiplier, t_11=2, p_12=20 * power_multiplier, t_12=28, r_c1=0)
            elif t_fridge >= 1:
                fridge.specific_cycle_1(p_11=281 * power_multiplier, t_11=1, p_12=20 * power_multiplier, t_12=29, r_c1=0)
                
        
        
        
         # FREEZER SHOP
        for start_minute in range(0, nb_minutes, 30):
            end_minute = start_minute + 30
            index_temp = end_minute - 1
            temp = temperatures_minute[index_temp]
            
            T_evap_freezer = 245.15 #[K] pinch de 5°C
            T_cond_freezer = (temp + 10)+273.15  #[K]
            
            T_lim = 15 #[°C] room temp cannot be below
            
            if temp >= T_lim : 
                cop_freezer = T_evap_freezer/(T_cond_freezer-T_evap_freezer)*eta_freezer
                delt_T_freezer = (temp + 18)
            
            else : 
                cop_freezer = T_evap_freezer/((T_lim + 10 + 273.15)-T_evap_freezer)*eta_freezer
                delt_T_freezer = (T_lim + 18)
            
            Q_ech_freezer = U_freezer*A_freezer*delt_T_freezer
            W_el_freezer = Q_ech_freezer/cop_freezer
            t_freezer = round(((W_el_freezer*30)-150)/205)

            # Apply a power factor depending on the time of day
            power_multiplier = 1.3 if 480 <= start_minute <= 1200 else 1 
            power_freezer = int(210 * power_multiplier)
            
            freezer = C.add_appliance(
                name="Freezer shop",
                number= 1,
                power=power_freezer,
                num_windows=1,
                func_time=30,
                time_fraction_random_variability=0,
                func_cycle=20,
                fixed="yes",
                fixed_cycle=1,
                )
            freezer.windows([start_minute, end_minute])
            
            
            if t_freezer >= 9:
                freezer.specific_cycle_1(210 * power_multiplier, 9, 5 * power_multiplier, 21, 0)    
            elif t_freezer >= 8:
                freezer.specific_cycle_1(210 * power_multiplier, 8, 5 * power_multiplier, 22, 0)    
            elif t_freezer >= 7:
                freezer.specific_cycle_1(210 * power_multiplier, 7, 5 * power_multiplier, 23, 0)    
            elif t_freezer >= 6:
                freezer.specific_cycle_1(210 * power_multiplier, 6, 5 * power_multiplier, 24, 0)
            elif t_freezer >= 5:
                freezer.specific_cycle_1(210 * power_multiplier, 5, 5 * power_multiplier, 25, 0)
            elif t_freezer >= 4:
                freezer.specific_cycle_1(210 * power_multiplier, 4, 5 * power_multiplier, 26, 0)
        
        uc_cold = UseCase(
            users=[F, C, F_s, F_h],
            parallel_processing=False,
            date_start=str(current_date),
            date_end=str(current_date)
        )
        uc_cold.initialize(peak_enlarge=0.15)
        Profiles_array_cold = uc_cold.generate_daily_load_profiles(flat=False)
        flat_load_cold = Profiles_array_cold.flatten()

        for minute in range(len(flat_load_cold)):
            min_multiplier_fridge = 6 if (360 <= start_minute <= 480 or 1080 <= start_minute <= 1200) else 5
            min_multiplier_freezer = 6.5 if 480 <= start_minute <= 1200 else 5
            min_multiplier_fridge_h = 22.25 if 480 <= start_minute <= 1080 else 20
            min_multiplier_fridge_s = 7 if 480 <= start_minute <= 1200 else 5
            
            min_value_fridge = nb_fridges * min_multiplier_fridge
            min_value_freezer = nb_freezer * min_multiplier_freezer
            min_value_fridge_s = nb_fridges_s * min_multiplier_fridge_s
            min_value_fridge_h = nb_fridges_h * min_multiplier_fridge_h
            
            min_value = min_value_fridge + min_value_freezer + min_value_fridge_s + min_value_fridge_h
            
            if flat_load_cold[minute] < min_value:
                flat_load_cold[minute] = min_value 
        
        
        # Rolling smoothing over 60 minutes with mirror padding
        window_size = 60
        pad = window_size // 2
        series = pd.Series(flat_load_cold)
        pre = series.iloc[1:pad+1][::-1]
        post = series.iloc[-pad-1:-1][::-1]
        extended = pd.concat([pre, series, post], ignore_index=True)
        smoothed = extended.rolling(window=window_size, center=True).mean().iloc[pad:-pad].reset_index(drop=True)
        
        df_profile_cold = pd.DataFrame({
            "Date": [str(current_date)] * len(smoothed),
            "Minute": range(len(smoothed)),
            "Load": smoothed.round(2)
        })
        Fridge_cold.append(df_profile_cold)

    # Annual save
    if Fridge_cold:
        year_df_final = pd.concat(Fridge_cold, ignore_index=True)
        year_df_final.to_csv(
            f"/Volumes/evelyn_hv62/part2/demand/cold/ssp126/demand_cold_{year}.csv", index=False)
        print(f"File for {year} loaded.")

    i += 1

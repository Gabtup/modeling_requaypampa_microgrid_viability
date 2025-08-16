#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 09:28:20 2025

@author: gabinbalhan
"""
import numpy as np
import pandas as pd
from ramp import User, UseCase
from tqdm import tqdm

# === Load temperature data ===
temperature_df = pd.read_csv(
    "/Volumes/evelyn_hv62/part1/result/prediction/ssp585/t/hour/prediction_2026-2045.csv",
    parse_dates=["datetime"]
)

temperature_df["date"] = temperature_df["datetime"].dt.date
temperature_df["year"] = temperature_df["datetime"].dt.year
i = 0

for year in tqdm(sorted(temperature_df["year"].unique()), desc="Simulation annuelle"):
    all_profiles = []
    # --- Sélectionner les données de l'année en cours ---
    year_df = temperature_df[temperature_df["year"] == year]

    # --- Boucle sur chaque jour de l'année ---
    for current_date in year_df["date"].unique():
        daily_df = year_df[year_df["date"] == current_date]
        hourly_temperatures = daily_df["T(°C)"].values

        if len(hourly_temperatures) != 24:
            print(f"⚠️ Températures incomplètes pour {current_date}, jour ignoré.")
            continue

        temperatures_minute = np.repeat(hourly_temperatures, 60)
        nb_minutes = len(temperatures_minute)
        
        # Activer l'école du 20 janvier au 7 juillet et du 19 juillet au 2 décembre pour toutes les années
        school_start_1 = pd.to_datetime(f"{year}-01-20")
        school_end_1 = pd.to_datetime(f"{year}-07-07")
        school_start_2 = pd.to_datetime(f"{year}-07-19")
        school_end_2 = pd.to_datetime(f"{year}-12-02")
        
        # Cold season 
        cold_start = pd.to_datetime(f"{year}-05-01")
        cold_end = pd.to_datetime(f"{year}-09-30")
        
        # Activer période de plantation du 15 octobre au 31 decembre
        plant_start = pd.to_datetime(f"{year}-10-15")
        plant_end = pd.to_datetime(f"{year}-12-31")
        
        # Activer période de recolte du 1 mars au 15 mai
        harvest_start = pd.to_datetime(f"{year}-03-01")
        harvest_end = pd.to_datetime(f"{year}-05-15")
        
        current_date_dt = pd.to_datetime(current_date)
        
        LH_share = 0.75 + ( (0.0 - 0.75) / 19 ) * i
        HH_share = 0.25 + ( (1.0 - 0.25) / 19 ) * i

        if (plant_start <= current_date_dt <= plant_end) or (harvest_start <= current_date_dt <= harvest_end): # reduce of 20 %
            
            total_households = 125 * 1.002**i

            LH = User("Households Low incomes", int(total_households * LH_share))

            HH = User("Households High incomes", int(total_households * HH_share))
            
        else:
            
            total_households = 125 * 1.002**i * (1 - 0.2)

            LH = User("Households Low incomes", int(total_households * LH_share))
            
            HH = User("Households High incomes", int(total_households * HH_share))
        
        SC = User("School", 1)
    
        HC = User("Health post", 1)

        R = User("Restaurant", 2)
        
        GS = User("Grocery Store 1", 5)

        WS = User("Workshop", 1)
        
        #HOUSEHOLD LOW OK
        
        H_indoor_bulb = HH.add_appliance(number=2, power=7, num_windows=2, func_time=360, 
                                        time_fraction_random_variability=0.2, func_cycle=10,
                                        wd_we_type=2, occasional_use=1) 
        H_indoor_bulb.windows([300,480], [960,1440], random_var_w=0.35) 
        
        H_Phone_charger = HH.add_appliance(number=2, power=5, num_windows=2, func_time= 120, 
                                          func_cycle=10, time_fraction_random_variability=0.2,
                                          wd_we_type=2, occasional_use=1) 
        H_Phone_charger.windows([1020,1440], [0,300], random_var_w=0.35)

        H_Radio = HH.add_appliance(number=1, power=36, num_windows=2, func_time=180, 
                                  time_fraction_random_variability=0.1, func_cycle=5,
                                  wd_we_type=2, occasional_use=0.5) 
        H_Radio.windows([390,450], [1080,1260], random_var_w=0.35)
        
        #HOUSEHOLD HIGH OK
        
        H_indoor_bulb = HH.add_appliance(number=4, power=7, num_windows=2, func_time=360, 
                                        time_fraction_random_variability=0.2, func_cycle=10,
                                        wd_we_type=2, occasional_use=1) 
        H_indoor_bulb.windows([300,480], [960,1440], random_var_w=0.35) 
             
        H_outdoor_bulb = HH.add_appliance(number=2, power=14, num_windows=1, func_time=180, 
                                          time_fraction_random_variability=0.2, func_cycle=10,
                                          wd_we_type=2, occasional_use=1)
        H_outdoor_bulb.windows([1140,1380], random_var_w=0.35) 
        
        H_Phone_charger = HH.add_appliance(number=4, power=5, num_windows=2, func_time= 120, 
                                          func_cycle=10, time_fraction_random_variability=0.2,
                                          wd_we_type=2, occasional_use=1) 
        H_Phone_charger.windows([1020,1440], [0,300], random_var_w=0.35)

        H_Radio = HH.add_appliance(number=1, power=36, num_windows=2, func_time=180, 
                                  time_fraction_random_variability=0.1, func_cycle=5,
                                  wd_we_type=2, occasional_use=0.5) 
        H_Radio.windows([390,450], [1080,1260], random_var_w=0.35)
        
        H_TV = HH.add_appliance(number=1, power=30, num_windows=2, func_time=120, 
                                  time_fraction_random_variability=0.1, func_cycle=5,
                                  wd_we_type=2, occasional_use=1) 
        H_TV.windows([1080,1440], [0,60], random_var_w=0.35)
        
        H_PC = HH.add_appliance(number=1, power=70, num_windows=1, func_time=150, 
                                time_fraction_random_variability=0.3, func_cycle=30,
                                wd_we_type=2, occasional_use=0.33) 
        H_PC.windows([960,1200], random_var_w=0.35)
        
        #SCHOOL OK
        
        if (school_start_1 <= current_date_dt <= school_end_1) or (school_start_2 <= current_date_dt <= school_end_2):
            
            SC_indoor_bulb = SC.add_appliance(number=27, power=7, num_windows=1, func_time=300,
                                              time_fraction_random_variability=0.2, func_cycle=10, 
                                              wd_we_type=0)
            SC_indoor_bulb.windows([480,780], random_var_w=0.35) 

            SC_outdoor_bulb = SC.add_appliance(number=7, power=14, num_windows=1, func_time=60,
                                               time_fraction_random_variability=0.2, func_cycle=10, 
                                               wd_we_type=0, occasional_use = 1)
            SC_outdoor_bulb.windows([480,780], random_var_w=0.35)
            
            SC_Printer = SC.add_appliance(number=1, power=20, num_windows=1, func_time=30,
                                                time_fraction_random_variability=0.2, func_cycle=5, 
                                                wd_we_type=0, occasional_use = 0.5)
            SC_Printer.windows([480,780], random_var_w=0.35)
            
            SC_Phone_charger = SC.add_appliance(number=5, power=5, num_windows=1, func_time=180,
                                                time_fraction_random_variability=0.2, func_cycle=10, 
                                                wd_we_type=0, occasional_use = 1)
            SC_Phone_charger.windows([480,780], random_var_w=0.35)
            
            
            SC_PC = SC.add_appliance(number=25, power=150, num_windows=1, func_time=240,
                                     time_fraction_random_variability=0.2, func_cycle=45, 
                                     wd_we_type=0, occasional_use = 1)
            SC_PC.windows([480,780], random_var_w=0.35)
            

            SC_radio = SC.add_appliance(number=5, power=36, num_windows=1, func_time=120,
                                        time_fraction_random_variability=0.2, func_cycle=5, 
                                        occasional_use = 0.3, wd_we_type=0)
            SC_radio.windows([480,780], random_var_w=0.35)
            
            SC_Data = SC.add_appliance(number=3, power=420, num_windows=1, func_time=60,
                                     time_fraction_random_variability=0.2, func_cycle=10, 
                                     wd_we_type=0, occasional_use = 0.5)
            SC_Data.windows([480,780], random_var_w=0.35)
            
            if (cold_start <= current_date_dt <= cold_end) :
                
                for start_minute in range(0, nb_minutes, 60):
                    end_minute = start_minute + 60
                    index_temp = end_minute - 1
                    temp = temperatures_minute[index_temp]
                
                    if temp >= 25 and 480 <= start_minute <= 780 : 
                        HC_fan = SC.add_appliance(number=15, power=30, num_windows=1, func_time=60,
                                                 time_fraction_random_variability=0, fixed="yes", 
                                                 flat="yes")
                        HC_fan.windows([start_minute,end_minute])
            else :
                
                for start_minute in range(0, nb_minutes, 60):
                    end_minute = start_minute + 60
                    index_temp = end_minute - 1
                    temp = temperatures_minute[index_temp]
                
                    if temp >= 26 and 480 <= start_minute <= 780 : 
                        HC_fan = SC.add_appliance(number=15, power=30, num_windows=1, func_time=60,
                                                 time_fraction_random_variability=0, fixed="yes", 
                                                 flat="yes")
                        HC_fan.windows([start_minute,end_minute])
            
        #HOSPITAL OK
        
        HC_indoor_bulb = HC.add_appliance(number=20, power=7, num_windows=2, func_time=690,
                                          time_fraction_random_variability=0.2, func_cycle=10,
                                          wd_we_type=2, occasional_use=1)
        HC_indoor_bulb.windows([0,720],[870,1440], random_var_w=0.35)

        HC_outdoor_bulb = HC.add_appliance(number=5, power=14, num_windows=2, func_time=240,
                                           time_fraction_random_variability=0.2, func_cycle=10, 
                                           wd_we_type=2, occasional_use = 1)
        HC_outdoor_bulb.windows([0,340],[1030,1440], random_var_w=0.35)
        
        HC_Phone_charger = HC.add_appliance(number=5, power=5, num_windows=2, func_time=300,
                                            time_fraction_random_variability=0.2, func_cycle=10,
                                            wd_we_type=2, occasional_use=1)
        HC_Phone_charger.windows([480,720],[900,1440], random_var_w=0.35)

        HC_radio = HC.add_appliance(number=2, power=36, num_windows=2, func_time=390,
                                    time_fraction_random_variability=0.2, func_cycle=10,
                                    wd_we_type=0, occasional_use=0.5)
        HC_radio.windows([480,720],[780,1080], random_var_w=0.35)

        HC_PC = HC.add_appliance(number=2, power=150, num_windows=2, func_time=300,
                                 time_fraction_random_variability=0.1, func_cycle=10,
                                 wd_we_type=0, occasional_use=1)
        HC_PC.windows([480,720],[780,1080], random_var_w=0.35)
        
        SC_Printer = HC.add_appliance(number=1, power=100, num_windows=1, func_time=60,
                                            time_fraction_random_variability=0.2, func_cycle=5, 
                                            wd_we_type=0, occasional_use = 1)
        SC_Printer.windows([540,1080], random_var_w=0.35)
        
        HC_sterilizer = HC.add_appliance(number=2, power=600, num_windows=2, func_time=120,
                                           time_fraction_random_variability=0.3, func_cycle=30, 
                                           occasional_use=0.5, wd_we_type=0)
        HC_sterilizer.windows([480,720],[780,1080], random_var_w=0.35)

        HC_Water_pump = HC.add_appliance(number=1, power=400, num_windows=1, func_time=45, 
                                     time_fraction_random_variability=0.2, func_cycle=10,
                                     occasional_use=1, wd_we_type=2)
        HC_Water_pump.windows([480,720],random_var_w=0.35)
        
        HC_Water_purifier = HC.add_appliance(number=1, power=415, num_windows=2, func_time=480,
                                              time_fraction_random_variability=0.3, func_cycle=30,
                                              occasional_use=0.5, wd_we_type=0)
        HC_Water_purifier.windows([480,720],[780,1080], random_var_w=0.35)
        
        HC_Pulse = HC.add_appliance(number=1, power=24, num_windows=2, func_time=120,
                                    time_fraction_random_variability=0.3, func_cycle=15,
                                    occasional_use=0.5, wd_we_type=0)
        HC_Pulse.windows([480,720],[780,1080],random_var_w=0.35)
        
        HC_Suction = HC.add_appliance(number=1, power=24, num_windows=2, func_time=240,
                                      time_fraction_random_variability=0.3, func_cycle=30,
                                      occasional_use=0.5, wd_we_type=0)
        HC_Suction.windows([480,720],[780,1080],random_var_w=0.35)
        
        HC_microscope = HC.add_appliance(number=1, power=30, num_windows=2, func_time=120,
                                     time_fraction_random_variability=0.3, func_cycle=10, 
                                     occasional_use=0.5, wd_we_type=0)
        HC_microscope.windows([480,720],[780,1080], random_var_w=0.1)
        
        if (cold_start <= current_date_dt <= cold_end) :
        
            for start_minute in range(0, nb_minutes, 60):
                end_minute = start_minute + 60
                index_temp = end_minute - 1
                temp = temperatures_minute[index_temp]
            
                if temp >= 25 : 
                    HC_fan = HC.add_appliance(number=10, power=30, num_windows=1, func_time=60,
                                             time_fraction_random_variability=0, fixed="yes", 
                                             flat="yes")
                    HC_fan.windows([start_minute,end_minute])
        
        else : 
            
            for start_minute in range(0, nb_minutes, 60):
                end_minute = start_minute + 60
                index_temp = end_minute - 1
                temp = temperatures_minute[index_temp]
            
                if temp >= 26 : 
                    HC_fan = HC.add_appliance(number=10, power=30, num_windows=1, func_time=60,
                                             time_fraction_random_variability=0, fixed="yes", 
                                             flat="yes")
                    HC_fan.windows([start_minute,end_minute])
            
        
        #RESTAURANT OK
        
        R_indoor_bulb = R.add_appliance(number=2, power=7, num_windows=2, func_time=360,
                                    time_fraction_random_variability=0.2, func_cycle=60,
                                    wd_we_type=0, occasional_use=1)
        R_indoor_bulb.windows([330,480], [1110,1380], random_var_w=0.35)
        
        R_Blender = R.add_appliance(number=1, power=350, num_windows=2, func_time=20,
                                    time_fraction_random_variability=0.3, func_cycle=5,
                                    occasional_use=0.5, wd_we_type=0)
        R_Blender.windows([420,480], [720,780], random_var_w=0.35)
        
        
        R_Plancha = R.add_appliance(number=1, power=2200, num_windows=2, func_time=90,
                                    time_fraction_random_variability=0.3, func_cycle=10,
                                    occasional_use=0.5, wd_we_type=0)
        R_Plancha.windows([360,480], [1020,1200], random_var_w=0.35)
        
        GS_Stereo = R.add_appliance(number=1, power=150, num_windows=1, func_time=400,
                                    time_fraction_random_variability=0.2, func_cycle=10,
                                    occasional_use=1, wd_we_type=1)
        GS_Stereo.windows([900,1440], random_var_w=0.35)
        
        #GROCERY STORE
        
        GS_indoor_bulb = GS.add_appliance(number=2, power=7, num_windows=2, func_time=150,
                                          time_fraction_random_variability=0.2, func_cycle=30,
                                          occasional_use=1, wd_we_type=0)
        GS_indoor_bulb.windows([480,600],[960,1080], random_var_w=0.35)
        
        #WORKSHOP
        
        WS_indoor_bulb = WS.add_appliance(number=2, power=7, num_windows=2, func_time=120,
                                          time_fraction_random_variability=0.2, func_cycle=30, 
                                          wd_we_type=0)
        WS_indoor_bulb.windows([480,600],[960,1080], random_var_w=0.35)
        
        #WASHING SHOP
        
        WS_Dryer = WS.add_appliance(number=1, power=600, num_windows=1, func_time=180,
                                    time_fraction_random_variability=0.2, func_cycle=60, 
                                    wd_we_type=0, occasional_use=0.02)
        
        WS_Dryer.windows([480,1080], random_var_w=0.35) 
        
        WS_Washing_machine = WS.add_appliance(number=1, power=2200, num_windows=1, func_time=120,
                                    time_fraction_random_variability=0.2, func_cycle=20, 
                                    wd_we_type=0, occasional_use=0.02)
        
        WS_Washing_machine.windows([480,1080], random_var_w=0.35) 
        
        #ATELIER 

        WS_welding_machine = WS.add_appliance(number=1, power=5000, num_windows=1, func_time=120,
                                              time_fraction_random_variability=0.2, func_cycle=15,
                                              wd_we_type=0)
        WS_welding_machine.windows([480,1080], random_var_w=0.35) 
        
        WS_grinding_machine = WS.add_appliance(number=1, power=1500, num_windows=1, func_time=120,
                                               time_fraction_random_variability=0.2, func_cycle=10, 
                                               wd_we_type=0, occasional_use=1)
        WS_grinding_machine.windows([480,1080], random_var_w=0.35) 
        
        #MILL
        
        GS_Mill = WS.add_appliance(number=1, power=1100, num_windows=1, func_time=240, 
                                    time_fraction_random_variability=0.2, func_cycle=60,
                                    wd_we_type=0, occasional_use=0.5)
        GS_Mill.windows([480,1080], random_var_w=0.35)
        
        
        uc_all = UseCase(
            users=[LH, HH, SC, R, GS, WS, HC],#[LH, HH, SC, HC, R, GS, WS],
            parallel_processing=False,
            date_start=str(current_date),
            date_end=str(current_date)
        )
        uc_all.initialize(peak_enlarge=0.15)
        Profiles_array_all = uc_all.generate_daily_load_profiles(flat=False)
        flat_load_all = Profiles_array_all.flatten()

        df_profile_all = pd.DataFrame({
            "Date": [str(current_date)] * len(flat_load_all),
            "Minute": range(len(flat_load_all)),
            "Load": flat_load_all.round(2)
        })
        all_profiles.append(df_profile_all)
        

    # --- Export annuel ---
    if all_profiles:
        year_df_final = pd.concat(all_profiles, ignore_index=True)
        year_df_final.to_csv((f"/Volumes/evelyn_hv62/part2/demand/t_ind/year_by_year/demand_t_ind_{year}.csv"), index=False)
        print(f"✅ Fichier pour {year} enregistré.")
    
    i += 1    
    
    

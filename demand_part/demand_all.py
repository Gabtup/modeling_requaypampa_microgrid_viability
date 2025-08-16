#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 30 12:03:46 2026

@author: gabinbalhan
"""

import pandas as pd
import os

# Root directory
root = "/Volumes/evelyn_hv62/part2/demand"

# File categories and name templates
categories = {
    "cool": f"{root}/cold/ssp585/year_by_year/demand_cold_{{year}}.csv",
    "t_ind": f"{root}/t_ind1st/year_by_year/demand_t_ind_{{year}}.csv",
}

# Output directory
output_dir = f"{root}/all/ssp126_1st/year_by_year"
os.makedirs(output_dir, exist_ok=True)

# Loop over years
for year in range(2026, 2046):
    print(f"Processing year {year}...")

    dfs = []

    for name, path_template in categories.items():
        file_path = path_template.format(year=year)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ Missing file: {file_path}")

        df = pd.read_csv(file_path)
        if not {"Date", "Minute", "Load"}.issubset(df.columns):
            raise ValueError(f"❌ File {file_path} does not have the expected columns.")

        df = df[["Date", "Minute", "Load"]].copy()
        df = df.rename(columns={"Load": f"Load_{name}"})
        dfs.append(df)

    # Merge on Date and Minute
    df_merged = dfs[0]
    for df in dfs[1:]:
        df_merged = pd.merge(df_merged, df, on=["Date", "Minute"], how="outer")

    # Replace NaN with 0
    load_cols = [col for col in df_merged.columns if col.startswith("Load_")]
    df_merged[load_cols] = df_merged[load_cols].fillna(0)

    # Final sum
    df_merged["Load"] = df_merged[load_cols].sum(axis=1)

    # Round to two decimals
    df_merged["Load"] = df_merged["Load"].round(2)

    # Sort to keep chronological order
    df_merged = df_merged.sort_values(by=["Date", "Minute"])

    # Save
    output_path = f"{output_dir}/demand_all_{year}.csv"
    df_merged[["Date", "Minute", "Load"]].to_csv(output_path, index=False)

    print(f"File 'demand_all_{year}.csv' generated.")

print("Processing completed for all years.")

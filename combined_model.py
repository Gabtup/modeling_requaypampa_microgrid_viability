#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 15:46:42 2025

@author: gabinbalhan
"""

# SERT A COMBINNER LES DOSSIER D'UN MEME MODELE ENSEMBLE #

import pandas as pd
import glob
import os

# Définir le dossier contenant les fichiers CSV
data_folder = "/Volumes/evelyn_hv62/part2/demand/fridge"
data_folder_output = "/Volumes/evelyn_hv62/part2/demand/fridge"

# Trouver tous les fichiers CSV dans le dossier avec un motif spécifique
csv_files = glob.glob(os.path.join(data_folder, "demand_fridge_*.csv"))

# Vérifier si des fichiers ont été trouvés
if not csv_files:
    print("❌ Aucun fichier CSV trouvé.")
else:
    # Lire et fusionner tous les fichiers trouvés
    dfs = [pd.read_csv(f) for f in csv_files]
    df_combined = pd.concat(dfs, ignore_index=True)

    # Trier par date si nécessaire (en supposant que la première colonne est la date)
    df_combined = df_combined.sort_values(by=df_combined.columns[0])

    # Définir le fichier de sortie
    output_file = os.path.join(data_folder_output, "demand_fridge_combined.csv")

    # Sauvegarder le fichier fusionné
    df_combined.to_csv(output_file, index=False)

    print(f"✅ Fichier combiné sauvegardé ici : {output_file}")


# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2024-07-13
# This script is used to load and preprocess the zircon data from a CSV file.
# ------------------------------------------------------------------------------------ #
import pandas as pd

def load_and_preprocess_data(csv_file):
    try:
        print(f"Loading data from {csv_file}...")
        zircon_data = pd.read_csv(csv_file, low_memory=False)
        
        print("Column names in the dataset:", zircon_data.columns)
        
        latitude_col = 'Latitude'
        longitude_col = 'Longitude'
        age_col = 'Best Age'
        
        zircon_data.dropna(subset=[latitude_col, longitude_col], inplace=True)
        zircon_data[latitude_col] = pd.to_numeric(zircon_data[latitude_col], errors='coerce')
        zircon_data[longitude_col] = pd.to_numeric(zircon_data[longitude_col], errors='coerce')
        zircon_data[age_col] = pd.to_numeric(zircon_data[age_col], errors='coerce')
        
        zircon_data = zircon_data.dropna(subset=[latitude_col, longitude_col])
        zircon_data[latitude_col] = zircon_data[latitude_col].astype(float)
        zircon_data[longitude_col] = zircon_data[longitude_col].astype(float)
        
        print("Data loaded and preprocessed successfully.")
        
        return zircon_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

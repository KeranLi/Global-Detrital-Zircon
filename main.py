#!/usr/bin/env python3
"""
Zircon Globality Calculator
===========================

Calculates globality over time for zircon data using the PaleoGlobal framework.

This script loads preprocessed zircon data, initializes a rotation model,
and computes globality values over a specified time range. The results are
saved to a CSV file.

Usage:
    python main.py

Requirements:
    - PyGMT
    - PyGplate

Example:
    python zircon_globality_calculator.py

Note:
    - Ensure that the required libraries are installed.
    - Update the file paths for the input CSV and output CSV as needed.
    - The script assumes that the input CSV file is properly formatted.
"""

# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2024-06-19
# Description: This script calculates globality over time for zircon data using the PaleoGlobal.
# ------------------------------------------------------------------------------------ #
from PaleoGlobal.Utils import load_and_preprocess_data
from PaleoGlobal.Models.ini import initialize_rotation_model
from PaleoGlobal.Global.calculate_global_light import calculate_globality_over_time_light
from gprm.datasets import Reconstructions

csv_file = './data/global_u-pb_clean_cormodified_mass_rocktype_ages_main.csv'
zircon_data = load_and_preprocess_data(csv_file)

if zircon_data is not None:
    print("Data loaded successfully.")
else:
    print("Data loading failed.")

start_time = 1
end_time = 999
step = 1
grid_size = 4

print("Fetching the reconstruction model...")
M2021 = Reconstructions.fetch_Merdith2021()
initialize_rotation_model(M2021)
print("Reconstruction model fetched successfully.")

print("Starting globality calculations over time...")
results_df = calculate_globality_over_time_light(zircon_data, start_time, end_time, step, grid_size)

output_file = './results/globality_over_time.csv'
results_df.to_csv(output_file, index=False)
print(f"Results saved to {output_file}.")

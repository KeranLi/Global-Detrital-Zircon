# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.comy
# Date: 2023-12-20
# This module is mainly designed to load, merge and export excel files
# ------------------------------------------------------------------------------------ #

import os
import pandas as pd
from tqdm import tqdm
import time
import dask.dataframe as dd
import dask.delayed as delayed
import dask.diagnostics

def import_merge_data_pd(folder_path):

    # Set up a new df to store data
    combined_data = pd.DataFrame()
    # Calculate the running time/Gain the start time point
    start_time = time.time() 

    # Loops all excel files in the fold
    for filename in tqdm(os.listdir(folder_path), desc="Merging Excel Files"):
        if filename.endswith('.xlsx'): # Make sure all files are .xlsx type
            file_path = os.path.join(folder_path, filename) # Build full direction
            df = pd.read_excel(file_path) # Load data
            combined_data = pd.concat([combined_data, df], ignore_index=True) # Merge data
    
    # Calculate the running time/Gain the end time point
    end_time = time.time()
    # Calculate the running time/Gain the total time
    total_time = end_time - start_time
    # Print the total time
    print(f"Total time taken: {total_time} seconds")
    return combined_data

def export_combined_data_pd(combined_data, output_path):
    combined_data.to_excel(output_path, index=False)
    print("Excel files merged and exported successfully.")

def load_excel_file(file_path):
    df = pd.read_excel(file_path)
    return df

def import_merge_data_dk(folder_path):
    # Define the start time
    start_time = time.time()
    # Get a list of all Excel files in the folder
    file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]

    # Load each Excel file as a delayed object
    delayed_dfs = [delayed(load_excel_file)(f) for f in file_list]

    # Convert the delayed objects to Dask DataFrame partitions
    dask_partitions = [dd.from_delayed(d) for d in delayed_dfs]

    # Combine the Dask DataFrame partitions into a single Dask DataFrame
    combined_data = dd.concat(dask_partitions)

    # Calculate the running time/Gain the end time point
    end_time = time.time()
    # Calculate the running time/Gain the total time
    total_time = end_time - start_time
    # Print the total time
    print(f"Total time taken: {total_time} seconds")

    return combined_data

def export_combined_data_dk(combined_data, output_path):
    # Convert the Dask DataFrame to a Pandas DataFrame
    pandas_df = combined_data.compute()
    # Write the Pandas DataFrame to an Excel file
    pandas_df.to_csv(output_path, index=False)
    print("Excel files merged and exported successfully.")
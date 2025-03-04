# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2024-05-15
# Description: This script evaluates the globality of ancient light reconstructions.
# ------------------------------------------------------------------------------------ #
import numpy as np
from PaleoGlobal.Models.get_coordinates_df import get_lon_lat_for_dataframe
import gc

def evaluate_globality_ancient_light(dataframe, reconstruction_time, grid_size=1):
    reconstructed_data = get_lon_lat_for_dataframe(dataframe, reconstruction_time)
    reconstructed_data_np = reconstructed_data[['Reconstructed_Latitude', 'Reconstructed_Longitude']].to_numpy()
    
    lat_range = np.arange(-90, 90 + grid_size, grid_size)
    lon_range = np.arange(-180, 180 + grid_size, grid_size)
    grid = np.zeros((len(lat_range), len(lon_range)), dtype=int)
    
    lat_indices = ((reconstructed_data_np[:, 0] + 90) // grid_size).astype(int)
    lon_indices = ((reconstructed_data_np[:, 1] + 180) // grid_size).astype(int)
    
    valid_indices = np.isfinite(lat_indices) & np.isfinite(lon_indices)
    lat_indices = lat_indices[valid_indices]
    lon_indices = lon_indices[valid_indices]
    
    grid[lat_indices, lon_indices] = 1
    
    activated_grids = np.sum(grid)
    total_grids = grid.size
    globality = activated_grids / total_grids
    
    del reconstructed_data, reconstructed_data_np, grid, lat_indices, lon_indices
    gc.collect()
    
    return globality
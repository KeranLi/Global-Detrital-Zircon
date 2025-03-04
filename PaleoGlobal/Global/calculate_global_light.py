# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2024-05-29
# Description: This script calculates globality over time for a given zircon data set.
# ------------------------------------------------------------------------------------ #

import pandas as pd
import numpy as np
import concurrent.futures
from tqdm import tqdm
from PaleoGlobal.Models.ini import initialize_rotation_model
from PaleoGlobal.Global.calculate_global import calculate_globality_for_time

def calculate_globality_over_time_light(zircon_data, start_time, end_time, step, grid_size):
    times = np.arange(start_time, end_time + 1, step)
    globalities = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=64, initializer=initialize_rotation_model, initargs=(global_rotation_model,)) as executor:
        results = list(tqdm(executor.map(calculate_globality_for_time, 
                                         [(zircon_data, time, grid_size) for time in times]),
                            total=len(times), desc="Calculating globality over time"))
        globalities.extend(results)

    results_df = pd.DataFrame({
        'Reconstruction_Time_Ma': times,
        'Globality': globalities
    })
    
    return results_df
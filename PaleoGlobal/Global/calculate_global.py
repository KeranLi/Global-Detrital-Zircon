# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2023-12-22
# Description: Calculate globality for a given time
# ------------------------------------------------------------------------------------ #
from PaleoGlobal.Global.eval_light import evaluate_globality_ancient_light

def calculate_globality_for_time(args):
    zircon_data, time, grid_size = args
    return evaluate_globality_ancient_light(zircon_data, time, grid_size)
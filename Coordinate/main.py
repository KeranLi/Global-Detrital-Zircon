# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2024-04-30
# Description: This module is designed to parse DMS (degrees, minutes, seconds) strings
#              and convert them to decimal degrees. It demonstrates the conversion
#              process with a list of example latitude and longitude strings.
# Usage: This script can be run directly in a Python environment.
# Example:
#     python script_name.py
# Note:
#     - The script uses the `dms2dd` module to perform the conversion.
#     - It handles various DMS formats, including those with spaces, hyphens, and different delimiters.
#     - The script prints the converted decimal degrees for each input DMS string.
# ------------------------------------------------------------------------------------ #
from dms2dd import *

# Example usage
latitude_dms_strs = [
    "34°3'36\"N", "34D3M36S", "34 3 36 N", 
    "34° 3' 36\" N", "34-03-36 N", "34 3.5 N",
    "34.5N", "34°_3'36''N", "34-3-36N", "34 3' 36\"_N"
]
longitude_dms_strs = [
    "118°14'55\"W", "118D14M55S", "118 14 55 W", 
    "118° 14' 55\" W", "118-14-55 W", "118 14.9167 W",
    "118.25W", "118°_14'55''W", "118-14-55W", "118 14' 55\"_W"
]

for lat_str, lon_str in zip(latitude_dms_strs, longitude_dms_strs):
    try:
        latitude_dd = parse_dms(lat_str)
        longitude_dd = parse_dms(lon_str)
        print(f"Input Latitude: {lat_str}, Decimal Degrees: {latitude_dd}")
        print(f"Input Longitude: {lon_str}, Decimal Degrees: {longitude_dd}")
    except ValueError as e:
        print(f"Error parsing '{lat_str}' or '{lon_str}': {e}")
    print('-' * 60)

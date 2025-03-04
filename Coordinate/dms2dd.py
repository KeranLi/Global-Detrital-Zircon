# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2024-04-30
# This module is mainly designed to remove duplicate samples
# Use add parse to run code on the terminal
# ------------------------------------------------------------------------------------ #
import re

def parse_dms(dms_str):
    """
    Parse a DMS (degrees, minutes, seconds) string and convert it to decimal degrees.

    Parameters:
    dms_str (str): DMS string (e.g., "34°3'36\"N", "34D3M36S", "34 3 36 N")

    Returns:
    float: Decimal degrees
    """
    # Remove unwanted characters and normalize input
    dms_str = re.sub(r'[^0-9A-Z°\'\"\.NSEW\s-]', '', dms_str.upper().replace('_', ''))

    # Regex pattern to extract degrees, minutes, seconds, and direction
    pattern = re.compile(r"""
        (?P<degrees>-?\d+(?:\.\d+)?)[°\sD]*   # Degrees, allowing for negative and decimal
        (?P<minutes>\d*(?:\.\d+)?)[\'\sM]*    # Minutes, allowing for decimal
        (?P<seconds>\d*(?:\.\d+)?)[\"\sS]*    # Seconds, allowing for decimal
        (?P<direction>[NSEW]?)                # Direction
    """, re.VERBOSE)

    match = pattern.match(dms_str)
    if not match:
        raise ValueError("Invalid DMS format")

    parts = match.groupdict()
    degrees = float(parts['degrees'])
    minutes = float(parts['minutes']) if parts['minutes'] else 0
    seconds = float(parts['seconds']) if parts['seconds'] else 0
    direction = parts['direction']

    return dms_to_dd(degrees, minutes, seconds, direction)

def dms_to_dd(degrees, minutes, seconds, direction):
    """
    Convert DMS (degrees, minutes, seconds) to decimal degrees.

    Parameters:
    degrees (float): Degrees
    minutes (float): Minutes
    seconds (float): Seconds
    direction (str): Direction ('N', 'S', 'E', 'W')

    Returns:
    float: Decimal degrees
    """
    dd = abs(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if degrees < 0 or direction in ('S', 'W'):
        dd = -dd
    return dd

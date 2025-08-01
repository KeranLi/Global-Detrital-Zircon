# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2024-04-30
# Description: This module is designed to read a file containing DMS (degrees, minutes, seconds) coordinates,
#              convert them to decimal degrees, and save the results to a new file.
# Usage: Use argparse to run the code on the terminal.
# Example:
#     python convert_dms.py --input_file coordinates.xlsx --lat_column Latitude --lon_column Longitude --output_file converted_coordinates.xlsx
# Note:
#     - The input file should contain columns with DMS coordinates.
#     - Supported file formats: .csv, .xlsx, .xls, .txt (tab-delimited).
#     - The script will create new columns 'Latitude_DD' and 'Longitude_DD' with the converted decimal degrees.
# ------------------------------------------------------------------------------------ #
import pandas as pd
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

def convert_dms_column(df, column_name):
    """
    Convert a column of DMS strings in a DataFrame to decimal degrees.

    Parameters:
    df (pd.DataFrame): DataFrame containing the DMS column
    column_name (str): Name of the column with DMS strings

    Returns:
    pd.Series: Series with decimal degrees
    """
    return df[column_name].apply(parse_dms)

def read_file(file_path):
    """
    Read a file and return a DataFrame.

    Parameters:
    file_path (str): Path to the file

    Returns:
    pd.DataFrame: DataFrame with the file data
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.txt'):
        return pd.read_csv(file_path, delimiter='\t')
    else:
        raise ValueError("Unsupported file format")

def save_file(df, file_path):
    """
    Save a DataFrame to a file.

    Parameters:
    df (pd.DataFrame): DataFrame to save
    file_path (str): Path to the file

    Returns:
    None
    """
    if file_path.endswith('.csv'):
        df.to_csv(file_path, index=False)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df.to_excel(file_path, index=False)
    elif file_path.endswith('.txt'):
        df.to_csv(file_path, sep='\t', index=False)
    else:
        raise ValueError("Unsupported file format")

def main(input_file, lat_column, lon_column, output_file):
    """
    Main function to read, convert, and save the file.

    Parameters:
    input_file (str): Path to the input file
    lat_column (str): Name of the latitude column
    lon_column (str): Name of the longitude column
    output_file (str): Path to the output file

    Returns:
    None
    """
    df = read_file(input_file)
    df['Latitude_DD'] = convert_dms_column(df, lat_column)
    df['Longitude_DD'] = convert_dms_column(df, lon_column)
    save_file(df, output_file)
    print(f"Converted coordinates saved to {output_file}")

# Example usage
input_file = 'coordinates.xlsx'
lat_column = 'Latitude'
lon_column = 'Longitude'
output_file = 'converted_coordinates.xlsx'

main(input_file, lat_column, lon_column, output_file)

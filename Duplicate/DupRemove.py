# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2023-12-18
# Description: This module is designed to remove duplicate samples from an Excel file
#              based on specified column keywords and save the result to a new file.
# Usage: Run the script on the terminal using argparse to specify input, output, and column keywords.
# Example:
#     python remove_duplicates.py input.xlsx output.xlsx keyword1 keyword2
# Note:
#     - The script reads an Excel file, removes duplicates based on columns that match the given keywords,
#       and saves the result to a new Excel file.
#     - Ensure that the input file is in Excel format (.xlsx, .xls).
#     - The script uses pandas for data manipulation and tqdm for a progress bar.
# ------------------------------------------------------------------------------------ #

import argparse
from tqdm import tqdm
import pandas as pd

def remove_duplicates_and_save(input_file, output_file, column_keywords):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Remove duplicates based on columns that match the given keywords
    df_duplicates_removed = df.drop_duplicates(subset=[column for column in df.columns if any(keyword in column for keyword in column_keywords)])

    # Save the result to a new Excel file
    df_duplicates_removed.to_excel(output_file, index=False)

# Use argparse to parse command-line arguments
parser = argparse.ArgumentParser(description='Remove duplicates and save data as an Excel file')
parser.add_argument('input_file', type=str, help='Path to the input Excel file')
parser.add_argument('output_file', type=str, help='Path to the output Excel file')
parser.add_argument('column_keywords', type=str, nargs='+', help='Keywords to match column names')
args = parser.parse_args()

# Use tqdm to display a progress bar
with tqdm(total=1) as pbar:
    remove_duplicates_and_save(args.input_file, args.output_file, args.column_keywords)
    pbar.update(1)

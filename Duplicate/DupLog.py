# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2023-12-30
# This module is mainly designed to record duplicate samples
# Use add parse to run code on the terminal
# ------------------------------------------------------------------------------------ #
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm

def duplicate_check_log(excel_file):
   # Read data from Excel files and store it in num, txt, and raw1
   df = pd.read_excel(excel_file, engine='openpyxl', sheet_name=1)

   # Initialize counter
   n_repeat = 0
   n_no_repeat = 0

   # Define variables for storing indexes of duplicate rows
   index_repeat1 = []
   index_repeat2 = []

   # Define variables for storing indexes of non repeating rows
   index_no_repeat = []

# Loop through data rows
   for i in tqdm(range(2, len(df) - 1)):  # Use tqdm to display progress
      repeat = 0
      # Compare with subsequent rows to find duplicate data
      for j in range(i + 1, len(df)):
          # Compare the values of column 7 (title), column 12 (sample), and column 41 (point)
          if (df.iloc[i, 7] == df.iloc[j, 7]) and (df.iloc[i, 12] == df.iloc[j, 12]) and (df.iloc[i, 41] == df.iloc[j, 41]):
              # If the value of column 8 is included in another row of column 8 (DOI), mark it as duplicate
              if ((df.iloc[i, 8].apply(lambda x: np.isin(x, df.iloc[j, 8]).any())).any()) or ((df.iloc[j, 8].apply(lambda x: np.isin(x, df.iloc[i, 8]).any())).any()):
                  repeat = 1
                  n_repeat += 1

                  # Index for storing duplicate rows
                  index_repeat1.append(i)
                  index_repeat2.append(j)
                  break
      # If no duplicate rows are found, mark them as non duplicate rows
      if not repeat:
          n_no_repeat += 1
          # Index for storing non repeating rows
          index_no_repeat.append(i)

   # Add row number column to data
   row_numbers = np.arange(1, len(df) + 1)
   df_repeat = pd.concat([pd.DataFrame(index_repeat1), df.iloc[index_repeat1, :]], axis=1)
   df_repeat.columns = ['row_number'] + list(df.columns)
   df_repeat.insert(1, 'row_number', row_numbers[index_repeat1])

   df_no_repeat = pd.concat([pd.DataFrame(index_no_repeat), df.iloc[index_no_repeat, :]], axis=1)
   df_no_repeat.columns = ['row_number'] + list(df.columns)
   df_no_repeat.insert(1, 'row_number', row_numbers[index_no_repeat])

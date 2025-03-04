# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2023-11-15
# This module is mainly designed to remove duplicate samples
# Use add parse to run code on the terminal
# ------------------------------------------------------------------------------------ #
import pandas as pd

# Read Excel file
df = pd.read_excel('./all_combined_data.xlsx')

# Filter duplicate items based on the three columns of "Web Lin", "Published Sample-ID", and "Sample&Rain"
df_duplicates_removed = df.drop_duplicates(subset=['Web Link', 'Published Sample_ID', 'Sample&Grain'])

# Save the filtered results to a new Excel file
df_duplicates_removed.to_excel('duplicates_removed_all_data.xlsx', index=False)
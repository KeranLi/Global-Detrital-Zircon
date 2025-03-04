# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2023-12-18
# This module is mainly designed to remove duplicate samples
# Use add parse to run code on the terminal
# ------------------------------------------------------------------------------------ #

import argparse
from tqdm import tqdm
import pandas as pd

def remove_duplicates_and_save(input_file, output_file, column_keywords):
  # 读取Excel文件
  df = pd.read_excel(input_file)

  # 根据传入的列名关键词进行重复项筛选
  df_duplicates_removed = df.drop_duplicates(subset=[column for column in df.columns if any(keyword in column for keyword in column_keywords)])

  # 保存筛选后的结果到新的Excel文件
  df_duplicates_removed.to_excel(output_file, index=False)

# 使用argparse解析命令行参数
parser = argparse.ArgumentParser(description='Remove duplicates and save data as an Excel file')
parser.add_argument('input_file', type=str, help='Path to the input Excel file')
parser.add_argument('output_file', type=str, help='Path to the output Excel file')
parser.add_argument('column_keywords', type=str, nargs='+', help='Keywords to match column names')
args = parser.parse_args()

# 使用tqdm显示进度条
with tqdm(total=1) as pbar:
  remove_duplicates_and_save(args.input_file, args.output_file, args.column_keywords)
  pbar.update(1)
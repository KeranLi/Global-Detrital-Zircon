# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2023-12-27
# Description: This file contains functions for reading, cleaning, saving CSV files, and calling a local script.
# ------------------------------------------------------------------------------------ #
import pandas as pd
import subprocess

# Function to read CSV file
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        return str(e)

# Function to clean CSV file data
def clean_data(df):
    # Example: Remove empty rows and columns
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    return df

# Function to save CSV file
def save_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        return f"File saved successfully to {file_path}"
    except Exception as e:
        return str(e)

# Function to chat with GPT-4
def chat_with_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response['choices'][0]['message']['content'].strip()

# Function to call local google_scholar_spider.py script
def call_google_scholar_spider(kw, nresults, csvpath, sortby, plotresults):
    command = [
        "python", "google_scholar_spider.py",
        "--kw", kw,
        "--nresults", str(nresults),
        "--csvpath", csvpath,
        "--sortby", sortby,
        "--plotresults", str(plotresults)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr
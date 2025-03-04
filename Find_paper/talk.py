# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------ #
# Author: Keran Li, Nanjing University, keranli98@outlook.com
# Date: 2023-12-27
# Description: This script is used to interact with GPT-4 for data analysis.
# ------------------------------------------------------------------------------------ #
import openai
from Tools.collector import *
from Tools.actions import *

# Function to call local google_scholar_spider.py script

# Set OpenAI API key
openai.api_key = 'your-api-key-here'

# Main program
if __name__ == "__main__":
    file_path = 'collected.csv'  # Specify the initial CSV file name
    
    # Step 1: Read and clean the CSV file
    df = read_csv(file_path)
    if isinstance(df, str):
        print(f"Error reading CSV file: {df}")
        df = None
    else:
        print("CSV file read successfully.")
        df = clean_data(df)
        print("Data cleaned successfully.")
        save_csv(df, file_path)
    
    # Initialize conversation messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant proficient in data analysis."},
        {"role": "user", "content": "I have cleaned a CSV file. Here are the first few rows:\n" + df.head().to_string() if df is not None else "Failed to read the CSV file."}
    ]

    # Initial conversation
    gpt_response = chat_with_gpt(messages)
    print("GPT-4 response:", gpt_response)

    # Loop for continuous conversation
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the conversation.")
            break
        
        # Check if the user input contains a command to update the CSV file
        if user_input.lower().startswith("update csv"):
            try:
                command = user_input.split(" ", 2)[2]
                exec(command)
                print(f"Executed command: {command}")
                if df is not None:
                    save_result = save_csv(df, file_path)
                    print(save_result)
            except Exception as e:
                print(f"Error executing command: {e}")
                continue
        
        # Check if the user input contains a command to call google_scholar_spider
        elif "google_scholar_spider" in user_input:
            try:
                kw = user_input.split("--kw")[1].split()[0].strip('"')
                nresults = int(user_input.split("--nresults")[1].split()[0])
                csvpath = user_input.split("--csvpath")[1].split()[0].strip('"')
                sortby = user_input.split("--sortby")[1].split()[0].strip('"')
                plotresults = int(user_input.split("--plotresults")[1].split()[0])
                
                # Call google_scholar_spider.py
                spider_output = call_google_scholar_spider(kw, nresults, csvpath, sortby, plotresults)
                print("Google Scholar Spider output:", spider_output)
                
                # Add the result of the call to the conversation
                messages.append({"role": "user", "content": user_input})
                messages.append({"role": "assistant", "content": spider_output})
            except Exception as e:
                print(f"Error processing the google_scholar_spider command: {e}")
                continue
        
        messages.append({"role": "user", "content": user_input})
        gpt_response = chat_with_gpt(messages)
        print("GPT-4:", gpt_response)
        messages.append({"role": "assistant", "content": gpt_response})

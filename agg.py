import os
import pandas as pd
from pathlib import Path

import os
import pandas as pd
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples_path", "-p", type=str, required=True)
    parser.add_argument("--out_name", '-n', type=str, default="./drafts/aggregated.csv")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # Path to the main directory containing subfolders with CSV files
    args = get_args()
    # Initialize an empty list to store DataFrames
    
    if "cifar" in args.samples_path:
        name = args.out_name.replace(".csv","_cifar.csv")
    elif "ffhq" in args.samples_path:
        name = args.out_name.replace(".csv","_ffhq.csv")
    elif "afhqv2" in args.samples_path:
        name = args.out_name.replace(".csv","_afhqv2.csv")
    else:
        name = args.out_name
    name = Path(name)
    # Loop through subfolders
    dfs = []
    for subdir, _, files in os.walk(args.samples_path):
        for file in files:
            # Check if the file is a CSV
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)
                # Extract the filename without extension to use as row name
                #filename = os.path.splitext(file)[0]
                # Set the filename as a new column or index in the DataFrame
                df['Filename'] = (subdir.split("/")[-1] + "_" + file).replace("-","_")  # Change 'Filename' to the desired column name
                df["path"] = subdir
                # Append the DataFrame to the list
                dfs.append(df)

    # Concatenate all DataFrames into a single DataFrame
    final_df = pd.concat(dfs, ignore_index=True)  # Change 'ignore_index' as needed
    #soft by Filename column
    final_df.sort_values(by=['Filename'], inplace=True)
    # Save the aggregated DataFrame to a new CSV file
    os.makedirs(name.parent, exist_ok=True)
    final_df.to_csv(name, index=False)
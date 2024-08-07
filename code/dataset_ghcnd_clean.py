'''
Dataset:
    Global Historical Climatology Network daily https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily

Path on my project: 
    datasets/ghcnd/ghcnd

What it includes:
    Historical Weather Observations, from 18xx to 2024, 127,470 csv files, 131GB

'''

import os
import pandas as pd

input_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\ghcnd'
output_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\cleaned'

# Columns to retain
columns_to_retain = ['STATION', 'DATE', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'NAME', 'TMAX', 'TMAX_ATTRIBUTES', 'TMIN', 'TMIN_ATTRIBUTES']

# Iterate through all CSV files in the input directory
i=0
missed=0
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        # Construct full file path
        file_path = os.path.join(input_directory, filename)
        
        # Read CSV
        try:
            df = pd.read_csv(file_path, low_memory=False)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
        
        missing_columns = [col for col in columns_to_retain if col not in df.columns]
        if missing_columns:
            missed += 1
            print(f"{file_path} missing col: {', '.join(missing_columns)}, skip this file")
            continue

        # only in the list
        df_cleaned = df[columns_to_retain]
        
        # save to output directory
        output_path = os.path.join(output_directory, filename)
        try:
            df_cleaned.to_csv(output_path, index=False)
            i+=1
            print(f"{i} file saved: {output_path}")
        except Exception as e:
            print(f"Error writing to {output_path}: {e}")

print(f"Cleaning complete, {i} saved, {missed} skiped.")

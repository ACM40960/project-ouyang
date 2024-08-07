'''
Dataset:
    CEDA MIADS https://catalogue.ceda.ac.uk/uuid/77910bcec71c820d4c92f40d3ed3f249

Path on my project: 
    \datasets\ceda_miads\yearly_files

What it includes:
    Global Marine Weather Observations, from 18xx to 2024, 1594 txt files, 83.2GB
    ** AND A INDIVIDUAL HEADER FILE! ** \datasets\ceda_miads\MO_Column_Headers.txt

'''

import os
import pandas as pd
from datetime import datetime


input_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ceda_miads\yearly_files'
header_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ceda_miads\MO_Column_Headers.txt'
output_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ceda_miads\cleaned'

# read headers and remove spaces
with open(header_directory, 'r') as f:
    headers = [header.strip() for header in f.readline().strip().split(',')]

# columns
required_columns = ["OB_TIME", "LATITUDE", "LONGITUDE", "AIR_TEMPERATURE", "AIR_TEMPERATURE_J", "SEA_TEMPERATURE", "SEA_TEMPERATURE_J"]


# dictionary to store indices of the required columns
required_indices = {col: headers.index(col) for col in required_columns}

total_num = 1594
count = 0

for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):
        input_file_path = os.path.join(input_directory, filename)
        
        with open(input_file_path, 'r') as file:
            count += 1
            print(f'Processing {count}/{total_num}')
            for line in file:
                columns = [col.strip() for col in line.strip().split(',')]
                
                # Extract values
                ob_time = columns[required_indices["OB_TIME"]]
                latitude = columns[required_indices["LATITUDE"]]
                longitude = columns[required_indices["LONGITUDE"]]
                air_temp = columns[required_indices["AIR_TEMPERATURE"]]
                air_temp_j = columns[required_indices["AIR_TEMPERATURE_J"]]
                sea_temp = columns[required_indices["SEA_TEMPERATURE"]]
                sea_temp_j = columns[required_indices["SEA_TEMPERATURE_J"]]
                
                # check if AIR_TEMPERATURE is missing, skip the row if it is
                if air_temp == '':
                    continue
                
                # parse the ob_time to get year and month
                ob_time_dt = datetime.strptime(ob_time, '%Y-%m-%d %H:%M')
                year = ob_time_dt.year
                month = ob_time_dt.month
                
                # output file path
                output_file_path = os.path.join(output_directory, f'{year}_{month}.csv')
                
                # check if file exists and append data to the output file
                if not os.path.isfile(output_file_path):
                    with open(output_file_path, 'w') as output_file:
                        output_file.write('LATITUDE,LONGITUDE,AIR_TEMPERATURE,AIR_TEMPERATURE_J,SEA_TEMPERATURE,SEA_TEMPERATURE_J\n')
                
                with open(output_file_path, 'a') as output_file:
                    output_file.write(f'{latitude},{longitude},{air_temp},{air_temp_j},{sea_temp},{sea_temp_j}\n')
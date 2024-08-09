'''
Input: \datasets\ceda_miads\cleaned
Output: \datasets\ceda_miads\output_sea_air.csv
        \datasets\ceda_miads\output_sea.csv

What it does:
    Combine all the cleaned files into a single file

Input columns explanation:
    OB_TIME: Observation time
    LATITUDE: Latitude
    LONGITUDE: Longitude
    AIR_TEMPERATURE: Air temperature
    AIR_TEMPERATURE_J: Air temperature quality
    SEA_TEMPERATURE: Sea temperature
    SEA_TEMPERATURE_J: Sea temperature quality

element name _j and weight
This attribute is a single character code which either describes the method of measurement, or further qualifies the meteorological values. The meaning of any value depends on the element being qualified.
A - Reading from autographic instrument: 1.0
B - Original measured in degrees Fahrenheit: 0.8
C - Original measured to nearest whole degree Fahrenheit: 0.7
D - Original measured to nearest 0.5 degree Fahrenheit: 0.9
E - Original measured to nearest whole degree Celsius: 0.8
F - Original measured to nearest 0.5 degree Celsius: 0.9
G - Iced Wetbulb (previously Spare): 0.5
H - Wet bulb not frozen, registering below 0.0 degrees Celsius: 0.5
J - Wet bulb wick is assumed to have dried out: 0.4
K - Wet bulb is derived from air temperature and dew point: 0.6
L - Iced Wetbulb derived from air/dewpoint temp (previously Spare): 0.5
M - Aspirated: 0.9
N - Aspirated and original in degrees Fahrenheit: 0.8
P - Aspirated and original to nearest whole degree Fahrenheit: 0.7
Q - Aspirated and original to nearest 0.5 degree Fahrenheit: 0.9
R - Aspirated and original to nearest whole degree Celsius: 0.8
S - Aspirated and original to nearest 0.5 degree Celsius: 0.9
T - Max/min obtained from SAWS hourly values: 0.7
U - Original temperature measured in 0.1 degrees F, and depth in inches: 0.8
V - Original temperature measured in whole degrees F, and depth in inches: 0.7
W - Original temperature measured in 0.1 degrees F, and depth at 24 inches: 0.8
X - Original temperature measured in whole degrees F, and depth at 24 inches: 0.7
Y - Original temperature measured in 0.1 degrees F, and depth at 48 inches: 0.8
Z - Original temperature measured in whole degrees F, and depth at 48 inches: 0.7


How do I process the data:
    Take a weighted average and sum the global temperatures for each month

'''

import pandas as pd
import numpy as np
import os

input_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ceda_miads\cleaned'
output_directory_sea_air = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ceda_miads\output_sea_air.csv'
output_directory_sea = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ceda_miads\output_sea.csv'

weights = {
    'A': 1.0, 'B': 0.8, 'C': 0.7, 'D': 0.9, 'E': 0.8, 'F': 0.9,
    'G': 0.5, 'H': 0.5, 'J': 0.4, 'K': 0.6, 'L': 0.5, 'M': 0.9,
    'N': 0.8, 'P': 0.7, 'Q': 0.9, 'R': 0.8, 'S': 0.9, 'T': 0.7,
    'U': 0.8, 'V': 0.7, 'W': 0.8, 'X': 0.7, 'Y': 0.8, 'Z': 0.7
}


sea_air_df = pd.DataFrame(columns=['TIME', 'TEMPERATURE'])
sea_df = pd.DataFrame(columns=['TIME', 'TEMPERATURE'])

total_file = 2038
count = 0

# Iterate through all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        count += 1
        print(f'Processing {count}/{total_file}, {filename}')
        file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(file_path)
        
        # Extract time information from the filename
        time_info = filename.replace('.csv', '')

        # Process air temperature data
        df['AIR_TEMPERATURE_J'] = df['AIR_TEMPERATURE_J'].fillna('A')  
        df['AIR_WEIGHT'] = df['AIR_TEMPERATURE_J'].map(weights)
        df['AIR_WEIGHTED_TEMP'] = df['AIR_TEMPERATURE'] * df['AIR_WEIGHT']
        air_temp = df['AIR_WEIGHTED_TEMP'].mean()
        # append the result to the sea_air_df and take a 2 round decimal
        sea_air_df = pd.concat([sea_air_df, pd.DataFrame({'TIME': [time_info], 'TEMPERATURE': [air_temp]})], ignore_index=True) 

        # Process sea temperature data
        df['SEA_TEMPERATURE_J'] = df['SEA_TEMPERATURE_J'].fillna(np.nan)  # Fill NaN values
        df['SEA_TEMPERATURE'] = df['SEA_TEMPERATURE'].fillna(0)  # Fill NaN values
        df['SEA_WEIGHT'] = df['SEA_TEMPERATURE_J'].map(weights)
        df['SEA_WEIGHTED_TEMP'] = df['SEA_TEMPERATURE'] * df['SEA_WEIGHT']
        sea_temp = df['SEA_WEIGHTED_TEMP'].mean()
        sea_df = pd.concat([sea_df, pd.DataFrame({'TIME': [time_info], 'TEMPERATURE': [sea_temp]})], ignore_index=True)

sea_air_df['TEMPERATURE'] = sea_air_df['TEMPERATURE'].round(2)  
sea_df['TEMPERATURE'] = sea_df['TEMPERATURE'].round(2)

sea_air_df.to_csv(output_directory_sea_air, index=False)
sea_df.to_csv(output_directory_sea, index=False)





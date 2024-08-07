'''
spilt the cleaned dataset by month

'''
import os
import pandas as pd

input_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\cleaned'
output_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\by_month'

def process_file(root, file):

    print(f"Processing {file}")
    file_path = os.path.join(root, file)
    df = pd.read_csv(file_path, delimiter=',')

    # Process each row
    for index, row in df.iterrows():
        date = row['DATE']
        # print(f"{date}:Processing")
        
        # Skip rows where TMAX or TMIN is missing
        if pd.isnull(row['TMAX']) or pd.isnull(row['TMIN']):
            # print(f"{date}:Missing TMAX or TMIN")
            continue
        
        if '/' in date:
            year, month, _ = date.split('/')
        elif '-' in date:
            year, month, _ = date.split('-')
        else:
            # print(f"{date}:Unexpected date format")
            continue

        year_month = f"{year}_{month}"
        
        # temperature in Celsius, and need to be divided by 10 first and then calculate the average
        temperature = (row['TMAX'] + row['TMIN']) / 20
        
        output_df = pd.DataFrame({
            'LATITUDE': [row['LATITUDE']],
            'LONGITUDE': [row['LONGITUDE']],
            'TAVG': [temperature]
        })
        
        output_file = os.path.join(output_directory, f"{year_month}.csv")
        
        # create a new file if it does not exist
        if not os.path.isfile(output_file):
            output_df.to_csv(output_file, index=False)
            #print(f"{date}:Created {output_file}")
        else:
            output_df.to_csv(output_file, mode='a', header=False, index=False)
            #print(f"{date}:Appended to {output_file}")

# Iterate through all CSV files in the input directory
for root, _, files in os.walk(input_directory):
    for file in files:
        if file.endswith('.csv'):
            process_file(root, file)

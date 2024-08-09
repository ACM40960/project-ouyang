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
import numpy as np

def clean(input_directory, output_directory):
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

def generate_station_summary(input_directory, output_filepath):
    summary_data = []
    abnormal_stations = []
    total_files = len(os.listdir(input_directory))
    count = 0

    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            count += 1

            if count ==30:
                break
            print(f"Processing {count}/{total_files}, {os.path.basename(filename)}")

            filepath = os.path.join(input_directory, filename)
            
            df = pd.read_csv(filepath)
            
            station_name = df['STATION'].iloc[0]
            latitude = df['LATITUDE'].iloc[0]
            longitude = df['LONGITUDE'].iloc[0]
            
            df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.strftime('%Y/%m/%d')
            df = df.dropna(subset=['DATE'])
            df = df.sort_values(by='DATE')
            
            start_date = pd.to_datetime(df['DATE'].iloc[0])
            end_date = pd.to_datetime(df['DATE'].iloc[-1])
            total_days = (end_date - start_date).days + 1
            num_records = len(df)
            
            # if number of records is less than 90% of total days, consider it as abnormal
            if num_records >= 0.8 * total_days:
                date_ranges = [f"{start_date.strftime('%Y/%m/%d')}-{end_date.strftime('%Y/%m/%d')}"]
                summary_data.append([station_name, latitude, longitude, date_ranges, num_records])
            else:
                is_continuous = True
                date_ranges = []
                previous_month = start_date.month
                start_segment = start_date

                for i in range(10, len(df), 10):
                    current_date = pd.to_datetime(df['DATE'].iloc[i])
                    current_month = current_date.month
                    current_year = current_date.year
                    previous_date = pd.to_datetime(df['DATE'].iloc[i-10])
                    previous_month = previous_date.month
                    previous_year = previous_date.year

                    month_diff = (current_year - previous_year) * 12 + (current_month - previous_month)

                    # check if the month difference is greater than 2
                    if month_diff > 18 :
                        date_ranges.append(f"{start_segment.strftime('%Y/%m/%d')}-{previous_date.strftime('%Y/%m/%d')}")
                        start_segment = current_date
                        is_continuous = False
                    
                    previous_month = current_month
                
                # append the last segment
                date_ranges.append(f"{start_segment.strftime('%Y/%m/%d')}-{end_date.strftime('%Y/%m/%d')}")

                if is_continuous:
                    summary_data.append([station_name, latitude, longitude, date_ranges, num_records])
                else:
                    abnormal_stations.append([station_name])
                    summary_data.append([station_name, latitude, longitude, date_ranges, num_records])
                    print(f"Abnormal station: {station_name}, with segmented dates")
    
    summary_df = pd.DataFrame(summary_data, columns=['STATION', 'LATITUDE', 'LONGITUDE', 'TIME', 'NUM'])
    summary_df.to_csv(os.path.join(output_filepath, 'station_summary.csv'), index=False)
    
    if abnormal_stations:
        abnormal_df = pd.DataFrame(abnormal_stations, columns=['STATION'])
        abnormal_df.to_csv(os.path.join(output_filepath, 'station_abnormal.csv'), index=False)




if __name__ == '__main__':
    
    
    input_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\ghcnd'
    cleaned_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\cleaned'
    output_summary = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd'

    # clean(input_directory, cleaned_directory)
    generate_station_summary(cleaned_directory, output_summary)



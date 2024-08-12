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


from concurrent.futures import ThreadPoolExecutor

def process_file(filepath):
    summary_data = []
    abnormal_stations = []

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
    
    if num_records >= 0.8 * total_days:
        date_ranges = [f"{start_date.strftime('%Y/%m/%d')}-{end_date.strftime('%Y/%m/%d')}"]
        summary_data.append([station_name, latitude, longitude, date_ranges, num_records])
        print(f"Normal station: {station_name}")
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

            if month_diff > 24:
                date_ranges.append(f"{start_segment.strftime('%Y/%m/%d')}-{previous_date.strftime('%Y/%m/%d')}")
                start_segment = current_date
                is_continuous = False
            
            previous_month = current_month
        
        date_ranges.append(f"{start_segment.strftime('%Y/%m/%d')}-{end_date.strftime('%Y/%m/%d')}")

        if is_continuous:
            summary_data.append([station_name, latitude, longitude, date_ranges, num_records])
        else:
            abnormal_stations.append([station_name])
            summary_data.append([station_name, latitude, longitude, date_ranges, num_records])
            print(f"Abnormal station: {station_name}, with segmented dates")
    
    return summary_data, abnormal_stations

def generate_station_summary(input_directory, output_filepath):
    summary_data = []
    abnormal_stations = []
    total_files = len(os.listdir(input_directory))
    count = 0

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for filename in os.listdir(input_directory):
            if filename.endswith(".csv"):

                print(f"Processing {count}/{total_files}, {os.path.basename(filename)}")

                filepath = os.path.join(input_directory, filename)
                futures.append(executor.submit(process_file, filepath))
        
        for future in futures:
            data, abnormal = future.result()
            summary_data.extend(data)
            abnormal_stations.extend(abnormal)
    
    summary_df = pd.DataFrame(summary_data, columns=['STATION', 'LATITUDE', 'LONGITUDE', 'TIME', 'NUM'])
    summary_df.to_csv(os.path.join(output_filepath, 'station_summary.csv'), index=False)
    
    if abnormal_stations:
        abnormal_df = pd.DataFrame(abnormal_stations, columns=['STATION'])
        abnormal_df.to_csv(os.path.join(output_filepath, 'station_abnormal.csv'), index=False)


def station_summary(input_folder, inventory_file_path, output_file_path):
    # Step 1: Read the inventory CSV file
    inventory_df = pd.read_csv(inventory_file_path, encoding='ISO-8859-1')

    # Initialize the list to store the results
    results = []
    total_files = len([f for f in os.listdir(input_folder) if f.endswith('.csv')])
    count = 0
    
    # Step 2: Read each CSV file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            
            station_id = os.path.splitext(filename)[0]  # Get station ID from filename

            # Step 3: Find the corresponding row in the inventory DataFrame
            station_info = inventory_df[inventory_df['Station_ID'] == station_id]

            if not station_info.empty:
                count += 1
                print(f'Processing {filename} ({count}/{total_files})')
                longitude = station_info['Longitude'].values[0]
                latitude = station_info['Latitude'].values[0]
                elevation = station_info['Elevation'].values[0]
                start_date = str(station_info['Data_start'].values[0])
                end_date = str(station_info['Data_end'].values[0])

                # Step 4: Check for invalid start dates and correct if necessary
                if len(start_date) < 4 or int(start_date) < 1500 or len(end_date) < 4 or int(end_date) < 1500:
                    print(f"Invalid start date for {station_id}, determining from file")
                    
                    # Open the station's CSV file to determine date range
                    station_file_path = os.path.join(input_folder, filename)
                    station_data = pd.read_csv(station_file_path)
                    
                    # Convert 'date' column to datetime format
                    station_data['DATE'] = pd.to_datetime(station_data['DATE'])
                    
                    # Determine the actual start and end dates
                    actual_start_date = station_data['DATE'].min().year
                    actual_end_date = station_data['DATE'].max().year
                    
                    # Update start_date and end_date based on actual data
                    start_date = str(actual_start_date)
                    end_date = str(actual_end_date)

                # Step 5: Calculate the number of years and format the date range
                num_years = int(end_date) - int(start_date) + 1
                date_range = f'{start_date}-{end_date}'

                # Append the result for this station
                results.append([station_id, longitude, latitude, elevation, date_range, num_years])

    # Step 6: Convert results into a DataFrame and save to CSV
    results_df = pd.DataFrame(results, columns=['station_id', 'longitude', 'latitude', 'elevation', 'date', 'num_years'])
    results_df.to_csv(output_file_path, index=False)

    print(f'Summary file created successfully at {output_file_path}')


if __name__ == '__main__':
    input_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\ghcnd'
    cleaned_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\cleaned'
    output_summary = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd'
    inventory_file_path = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\Monthly_station_inventory.csv'
    output_summary_path = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\station_summary.csv'

    station_summary(cleaned_directory, inventory_file_path, output_summary_path)




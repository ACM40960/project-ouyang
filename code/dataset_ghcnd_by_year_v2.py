'''
spilt the cleaned dataset by year and month
multiple threads are used to speed up the process
'''
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

input_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\cleaned'
output_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\by_month'
station_list_path = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\station_list.csv'


def process_files(file_batch, batch_num, total_batches):
    output_data = {}
    file_count = len(file_batch)
    i=0
    for file_path in file_batch:
        i +=1
        print(f"Processing batch {i}/{batch_num}, file {os.path.basename(file_path)}")
        df = pd.read_csv(file_path, delimiter=',')

        # Process each row
        for index, row in df.iterrows():
            date = row['DATE']
            
            if pd.isnull(row['TMAX']) or pd.isnull(row['TMIN']):
                continue
            
            if '/' in date:
                year, month, _ = date.split('/')
            elif '-' in date:
                year, month, _ = date.split('-')
            else:
                continue

            year_month = f"{year}_{month}"
            
            temperature = (row['TMAX'] + row['TMIN']) / 20
            
            if year_month not in output_data:
                output_data[year_month] = []
            
            output_data[year_month].append({
                'STATION_ID': row['STATION'],
                'LATITUDE': row['LATITUDE'],
                'LONGITUDE': row['LONGITUDE'],
                'TAVG': temperature
            })
    
    for year_month, data in output_data.items():
        output_df = pd.DataFrame(data)
        output_file = os.path.join(output_directory, f"{year_month}.csv")
        
        if not os.path.isfile(output_file):
            output_df.to_csv(output_file, index=False)
        else:
            output_df.to_csv(output_file, mode='a', header=False, index=False)
    
    print(f"Finished processing batch {batch_num}/{total_batches} with {file_count} files")


batch_size = 50
num_threads = 4

input_files = os.listdir(input_directory)
input_station_names = [os.path.splitext(file)[0] for file in input_files]

# Read station list
station_list = pd.read_csv(station_list_path)
station_list = station_list["station_id"]

# filter out stations that are not in the station list
station_remained = [station for station in input_station_names if station in station_list.values]
# add the .csv extension back
station_remained = [os.path.join(input_directory, f"{station}.csv") for station in station_remained]

num_files = len(station_remained)

batches = [station_remained[i:i + batch_size] for i in range(0, num_files, batch_size)]
total_batches = len(batches)
print(f"Total files to process: {num_files}, total batches: {total_batches}")


with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(process_files, batch, batch_num, total_batches) for batch_num, batch in enumerate(batches, 1)]
    for future in futures:
        future.result()

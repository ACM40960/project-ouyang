'''
spilt the cleaned dataset by month

'''
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

input_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\test_2'
output_directory = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\by_month_2'

def process_files(file_batch, batch_num, total_batches):
    output_data = {}
    file_count = len(file_batch)

    for file_path in file_batch:
        print(f"Processing {file_path}")
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

files = [os.path.join(root, file) for root, _, files in os.walk(input_directory) for file in files if file.endswith('.csv')]
num_files = len(files)
print(f"Total files to process: {num_files}")

batches = [files[i:i + batch_size] for i in range(0, len(files), batch_size)]
total_batches = len(batches)

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(process_files, batch, batch_num, total_batches) for batch_num, batch in enumerate(batches, 1)]
    for future in futures:
        future.result()

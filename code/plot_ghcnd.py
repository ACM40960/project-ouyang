import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
output_directory_ground_air = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\output_ground_air.csv'


import os
import pandas as pd
import numpy as np

# 输入和输出文件夹路径
input_folder = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\by_month'
output_file = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ghcnd\output_ground_air.csv'
"""
# 获取输入文件夹中的所有CSV文件名并排序
files = os.listdir(input_folder)

# 初始化结果列表
results = []

# 遍历每个CSV文件并计算TAVG列的平均值
for file in files:
    file_path = os.path.join(input_folder, file)
    
    # 读取CSV文件
    df = pd.read_csv(file_path)
    

    # 计算TAVG列的平均值
    avg_tavg = df['TAVG'].mean()
    
    # 添加到结果列表
    results.append({'TIME': file.replace('.csv', ''), 'T': avg_tavg})
    print(f"Processed {file}")

# 创建结果的DataFrame
result_df = pd.DataFrame(results)

# 保存结果到CSV文件
result_df.to_csv(output_file, index=True)

print(f"计算结果已保存至 {output_file}")

"""
# next is to plot the data
# Read the output file
df = pd.read_csv(output_file)


# Extract the year from the TIME column
df['YEAR'] = df['TIME'].apply(lambda x: int(x.split('_')[0]))

# Group by year and calculate min, avg, and max temperatures
yearly_data = df.groupby('YEAR')['T'].agg(['min', 'mean', 'max']).reset_index()

# Round the values to one decimal place
yearly_data = yearly_data.round(1)
# cut the yearly_data, only after 1775
yearly_data = yearly_data[yearly_data['YEAR'] > 1760]

# Convert the yearly data to a dictionary
data_dict = {
    year: {'min': row['min'], 'avg': row['mean'], 'max': row['max']}
    for year, row in yearly_data.iterrows()
}

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(yearly_data['YEAR'], yearly_data['min'], label='Min Temperature', color='blue')
plt.plot(yearly_data['YEAR'], yearly_data['mean'], label='Avg Temperature')
plt.plot(yearly_data['YEAR'], yearly_data['max'], label='Max Temperature', color='red')

plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.title('Yearly Temperature Trends')
plt.legend()
plt.grid(True)
plt.show()

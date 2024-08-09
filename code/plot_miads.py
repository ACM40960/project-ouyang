import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
output_directory_sea_air = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ceda_miads\output_sea_air.csv'
output_directory_sea = r'C:\mod\University\ucd1s\Project\project-ouyang\datasets\ceda_miads\output_sea.csv'

# Read the CSV files
sea_air_df = pd.read_csv(output_directory_sea_air)
sea_df = pd.read_csv(output_directory_sea)

# Convert TIME column to datetime format
sea_air_df['TIME'] = pd.to_datetime(sea_air_df['TIME'], format='%Y_%m')
sea_df['TIME'] = pd.to_datetime(sea_df['TIME'], format='%Y_%m')

# Extract year and month for grouping
sea_air_df['YEAR'] = sea_air_df['TIME'].dt.year
sea_air_df['MONTH'] = sea_air_df['TIME'].dt.month
sea_df['YEAR'] = sea_df['TIME'].dt.year
sea_df['MONTH'] = sea_df['TIME'].dt.month

# Calculate yearly statistics
sea_air_stats = sea_air_df.groupby('YEAR')['TEMPERATURE'].agg(['mean', 'std'])
sea_stats = sea_df.groupby('YEAR')['TEMPERATURE'].agg(['mean', 'std'])

# Plot the data with error bars
plt.figure(figsize=(12, 6))
plt.errorbar(sea_air_stats.index, sea_air_stats['mean'], yerr=sea_air_stats['std'], fmt='-o', label='Sea Air Temperature', capsize=5)
plt.errorbar(sea_stats.index, sea_stats['mean'], yerr=sea_stats['std'], fmt='-o', label='Sea Temperature', capsize=5)

# Add titles and labels
plt.title('Yearly Average Temperature with Error Bars')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()

# Show plot
plt.show()
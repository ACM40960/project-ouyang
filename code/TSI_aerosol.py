import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

superdataset_path = '..\datasets\superdataset.csv'
superdataset_df = pd.read_csv(superdataset_path)

tsi_df = superdataset_df[['year', 'TSI']]
aerogsol_df = superdataset_df[['year', 'aerosol']]


tsi_df = tsi_df[tsi_df['year'] > 1750]

tsi_values = tsi_df['TSI'].values
tsi_years = tsi_df['year'].values
tsi_rolling_avg = tsi_df['TSI'].rolling(window=11, center=True).mean()

aerosol_values = aerogsol_df['aerosol'].values
aerosol_years = aerogsol_df['year'].values

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# TSI on the first subplot
ax1.plot(tsi_years, tsi_values, color='red')
ax1.set_yticks([1360.5, 1361, 1361.5, 1362])
ax1.tick_params(axis='y', labelsize=20)
ax1.grid(True)
ax1.set_title('Total Solar Irradiance and Aerogel Concentration Over Time', fontsize=22)
ax1.plot(tsi_years, tsi_rolling_avg, color='blue', linestyle='-', linewidth=2, label='10-Year Rolling Avg')
ax1.legend(fontsize=20, loc='lower right')
# Aerosol on the second subplot
ax2.plot(aerosol_years, aerosol_values, color='blue')
ax2.set_xlabel('Year', fontsize=20)
ax2.tick_params(axis='x', labelsize=20)
ax2.tick_params(axis='y', labelsize=20)
ax2.grid(True)

ax1.set_ylabel('')
ax2.set_ylabel('')

plt.subplots_adjust(hspace=0)  

plt.show()
import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Project\project-ouyang\code\granger_causality_results.csv'
data = pd.read_csv(file_path)

data.set_index('Lag', inplace=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

ax1.plot(data.index, data['CH4 Spline (ppb)'], label='CH4', marker='o')
ax1.plot(data.index, data['CO2 Spline (ppm)'], label='CO2', marker='o')
ax1.plot(data.index, data['N2O Spline (ppb)'], label='N2O', marker='o')
ax1.set_title('Granger Causality Results for Gases', fontsize=18)
ax1.set_xlabel('Lag', fontsize=18)
ax1.axhline(y=0.05, color='red', linestyle='--')
ax1.set_ylabel('P-Value',fontsize=18)
ax1.tick_params(axis='both', which='major', labelsize=18)
ax1.set_ylim(0, 1)
ax1.legend(fontsize=18)
ax1.grid(True)

ax2.plot(data.index, data['TSI'], label='TSI', marker='o')
ax2.plot(data.index, data['aerosol'], label='Aerosol', marker='o')
ax2.set_title('Granger Causality Results for TSI and Aerosol', fontsize=18)
ax2.set_xlabel('Lag', fontsize=18)
ax2.axhline(y=0.05, color='red', linestyle='--')
ax2.set_ylim(0, 1)
ax2.legend(fontsize=18)
ax2.tick_params(axis='both', which='major', labelsize=18)
ax2.grid(True)

plt.tight_layout()
plt.show()
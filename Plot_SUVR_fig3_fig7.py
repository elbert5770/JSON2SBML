import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Load the datasets
try:
    df_fig7 = pd.read_csv('Geerts 2023 Figure 7.csv')
    df_fig3 = pd.read_csv('Geerts 2023 Figure 3 units.csv')
except FileNotFoundError as e:
    print(f"Error loading CSV file: {e}")
    # Exit if files are not found
    exit()

# Filter data for Figure 7
fig7_suvr_placebo = df_fig7[(df_fig7['observation'] == 'SUVR') & (df_fig7['series'] == 'Placebo')]

# Filter data for Figure 3
fig3_suvr_APOE4 = df_fig3[(df_fig3['observation'] == 'SUVR') & (df_fig3['series'] == 'APOE4')].copy()
fig3_suvr_APOE4['time'] = fig3_suvr_APOE4['time'] / (24 * 365)
fig3_suvr_APOE4 = fig3_suvr_APOE4.sort_values(by='time')

fig3_suvr_nonAPOE4 = df_fig3[(df_fig3['observation'] == 'SUVR') & (df_fig3['series'] == 'nonAPOE4')].copy()
fig3_suvr_nonAPOE4['time'] = fig3_suvr_nonAPOE4['time'] / (24 * 365)
fig3_suvr_nonAPOE4 = fig3_suvr_nonAPOE4.sort_values(by='time')

# Create interpolation functions
interp_APOE4 = interp1d(fig3_suvr_APOE4['time'], fig3_suvr_APOE4['measurement'], kind='linear', fill_value="extrapolate")
interp_nonAPOE4 = interp1d(fig3_suvr_nonAPOE4['time'], fig3_suvr_nonAPOE4['measurement'], kind='linear', fill_value="extrapolate")

# Create a common time axis for averaging
common_time = np.linspace(
    max(fig3_suvr_APOE4['time'].min(), fig3_suvr_nonAPOE4['time'].min()),
    min(fig3_suvr_APOE4['time'].max(), fig3_suvr_nonAPOE4['time'].max()),
    num=100
)

# Calculate interpolated values
interp_vals_APOE4 = interp_APOE4(common_time)
interp_vals_nonAPOE4 = interp_nonAPOE4(common_time)

# Calculate the weighted average
weighted_avg = 0.7 * interp_vals_APOE4 + 0.3 * interp_vals_nonAPOE4

# Create the plot
plt.figure(figsize=(10, 6))

# Plot Figure 7 data
plt.plot(fig7_suvr_placebo['time'], fig7_suvr_placebo['measurement'], linestyle='-', label='Figure 7 SUVR Placebo',color='black')

# Plot original Figure 3 data
plt.plot(fig3_suvr_APOE4['time'], fig3_suvr_APOE4['measurement'], 'x', label='Figure 3 SUVR APOE4 (original)', color='red')
plt.plot(fig3_suvr_nonAPOE4['time'], fig3_suvr_nonAPOE4['measurement'], '+', label='Figure 3 SUVR non-APOE4 (original)', color='blue')
plt.axvline(x=70, color='black', linestyle='--', linewidth=1)
plt.axvline(x=74, color='black', linestyle='--', linewidth=1)

# Plot the weighted average
plt.plot(common_time, weighted_avg, linestyle='-', color='green', label='Weighted Average (0.7*APOE4 + 0.3*non-APOE4)')

# Add labels and title
plt.xlabel('Time (years)')
plt.ylabel('SUVR Measurement')
plt.title('SUVR Measurement vs. Time')
plt.legend()
plt.grid(True)
plt.xlim(65, 85)


# To save the plot, uncomment the following line
plt.savefig('SUVR_fig3_fig7.png')

# Show the plot
plt.show()

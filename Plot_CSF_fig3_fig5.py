import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Load the datasets
try:
    df_fig5 = pd.read_csv('Geerts 2023 Figure 5C data.csv')
    df_fig3 = pd.read_csv('Geerts 2023 Figure 3 units.csv')
except FileNotFoundError as e:
    print(f"Error loading CSV file: {e}")
    # Exit if files are not found
    exit()

# Filter data for Figure 7
fig5_CSF_placebo = df_fig5[(df_fig5['observation'] == 'Placebo') & (df_fig5['series'] == 'Sim')]
fig5_CSF_placebo_data = df_fig5[(df_fig5['observation'] == 'Placebo') & (df_fig5['series'] == 'Data')]

# Filter data for Figure 3
fig3_CSF_APOE4 = df_fig3[(df_fig3['observation'] == 'CSF_AB42') & (df_fig3['series'] == 'APOE4')].copy()
fig3_CSF_APOE4['time'] = fig3_CSF_APOE4['time'] / (24 * 365)
fig3_CSF_APOE4 = fig3_CSF_APOE4.sort_values(by='time')

fig3_CSF_nonAPOE4 = df_fig3[(df_fig3['observation'] == 'CSF_AB42') & (df_fig3['series'] == 'nonAPOE4')].copy()
fig3_CSF_nonAPOE4['time'] = fig3_CSF_nonAPOE4['time'] / (24 * 365)
fig3_CSF_nonAPOE4 = fig3_CSF_nonAPOE4.sort_values(by='time')

# Create interpolation functions
interp_APOE4 = interp1d(fig3_CSF_APOE4['time'], fig3_CSF_APOE4['measurement'], kind='linear', fill_value="extrapolate")
interp_nonAPOE4 = interp1d(fig3_CSF_nonAPOE4['time'], fig3_CSF_nonAPOE4['measurement'], kind='linear', fill_value="extrapolate")

# Create a common time axis for averaging
common_time = np.linspace(
    max(fig3_CSF_APOE4['time'].min(), fig3_CSF_nonAPOE4['time'].min()),
    min(fig3_CSF_APOE4['time'].max(), fig3_CSF_nonAPOE4['time'].max()),
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
plt.plot(fig5_CSF_placebo['time']+0.3, fig5_CSF_placebo['measurement'], marker='o', linestyle='-', label='Figure 7 SUVR Placebo')
plt.plot(fig5_CSF_placebo_data['time']+0.3, fig5_CSF_placebo_data['measurement'], marker='o', label='Figure 7 SUVR Placebo Data')

# Plot original Figure 3 data
plt.plot(fig3_CSF_APOE4['time'], fig3_CSF_APOE4['measurement'], 'x', label='Figure 3 CSF APOE4 (original)')
plt.plot(fig3_CSF_nonAPOE4['time'], fig3_CSF_nonAPOE4['measurement'], '+', label='Figure 3 CSF non-APOE4 (original)')

# Plot the weighted average
plt.plot(common_time, weighted_avg, linestyle='-', color='purple', label='Weighted Average (0.7*APOE4 + 0.3*non-APOE4)')

# Add labels and title
plt.xlabel('Time (years)')
plt.ylabel('CSF Measurement (nM)')
plt.title('CSF Measurement vs. Time')
plt.legend()
plt.grid(True)
plt.xlim(65, 85)

# Show the plot
plt.show()

# To save the plot, uncomment the following line
plt.savefig('CSF_fig3_fig5.png')

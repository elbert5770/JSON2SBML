import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Load the datasets
try:
    df_fig5 = pd.read_csv('Geerts 2023 Figure 5B.csv')
    df_fig3 = pd.read_csv('Geerts 2023 Figure 3 units.csv')
    df_fig7 = pd.read_csv('Geerts 2023 Figure 7.csv')
except FileNotFoundError as e:
    print(f"Error loading CSV file: {e}")
    # Exit if files are not found
    exit()

# Filter data for Figure 7
fig5_SUVR_placebo = df_fig5[(df_fig5['observation'] == 'Placebo') & (df_fig5['series'] == 'Sim')]
fig5_SUVR_placebo_data = df_fig5[(df_fig5['observation'] == 'Placebo') & (df_fig5['series'] == 'Data')]
fig5_SUVR_placebo_data = fig5_SUVR_placebo_data.sort_values(by='time')

fig7_SUVR_placebo = df_fig7[(df_fig7['observation'] == 'SUVR') & (df_fig7['series'] == 'Placebo')]
fig7_SUVR_placebo = fig7_SUVR_placebo.sort_values(by='time')

# Filter data for Figure 3
fig3_SUVR_APOE4 = df_fig3[(df_fig3['observation'] == 'SUVR') & (df_fig3['series'] == 'APOE4')].copy()
fig3_SUVR_APOE4['time'] = fig3_SUVR_APOE4['time'] / (24 * 365)
fig3_SUVR_APOE4 = fig3_SUVR_APOE4.sort_values(by='time')

fig3_SUVR_nonAPOE4 = df_fig3[(df_fig3['observation'] == 'SUVR') & (df_fig3['series'] == 'nonAPOE4')].copy()
fig3_SUVR_nonAPOE4['time'] = fig3_SUVR_nonAPOE4['time'] / (24 * 365)
fig3_SUVR_nonAPOE4 = fig3_SUVR_nonAPOE4.sort_values(by='time')

# Create interpolation functions
interp_APOE4 = interp1d(fig3_SUVR_APOE4['time'], fig3_SUVR_APOE4['measurement'], kind='linear', fill_value="extrapolate")
interp_nonAPOE4 = interp1d(fig3_SUVR_nonAPOE4['time'], fig3_SUVR_nonAPOE4['measurement'], kind='linear', fill_value="extrapolate")

# Create a common time axis for averaging
common_time = np.linspace(
    max(fig3_SUVR_APOE4['time'].min(), fig3_SUVR_nonAPOE4['time'].min()),
    min(fig3_SUVR_APOE4['time'].max(), fig3_SUVR_nonAPOE4['time'].max()),
    num=100
)

# Calculate interpolated values
interp_vals_APOE4 = interp_APOE4(common_time)
interp_vals_nonAPOE4 = interp_nonAPOE4(common_time)

# Calculate the weighted average
weighted_avg = 0.7 * interp_vals_APOE4 + 0.3 * interp_vals_nonAPOE4

# Create the plot
plt.figure(figsize=(10, 6))

# Plot Figure 5 data
plt.plot(fig5_SUVR_placebo['time']+0.3, fig5_SUVR_placebo['measurement'], 'k-', label='Figure 5 SUVR Placebo')
plt.plot(fig5_SUVR_placebo_data['time']+0.3, fig5_SUVR_placebo_data['measurement'], 'ko', label='Figure 5 SUVR Placebo Data')
plt.plot(fig7_SUVR_placebo['time'], fig7_SUVR_placebo['measurement'], 'k--', linewidth=1, label='Figure 7 SUVR Placebo')

# Plot original Figure 3 data
plt.plot(fig3_SUVR_APOE4['time'], fig3_SUVR_APOE4['measurement'], 'rx', label='Figure 3 SUVR APOE4 (original)')
plt.plot(fig3_SUVR_nonAPOE4['time'], fig3_SUVR_nonAPOE4['measurement'], 'bx', label='Figure 3 SUVR non-APOE4 (original)')

# Plot the weighted average
plt.plot(common_time, weighted_avg, linestyle='-', color='green', label='Weighted Average (0.7*APOE4 + 0.3*non-APOE4)')

# Add labels and title
plt.xlabel('Time (years)')
plt.ylabel('SUVR Measurement')
plt.title('SUVR Measurement vs. Time')
plt.legend()
plt.grid(True)
plt.xlim(65, 85)
plt.savefig('SUVR_fig3_fig5_fig7.png')
# Show the plot
plt.show()

# To save the plot, call plt.savefig BEFORE plt.show, not after.
# Move this line above plt.show() in your script to avoid saving a blank (white) image.
# plt.savefig('SUVR_fig3_fig5.png')

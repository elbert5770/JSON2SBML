import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('Fagan2021_Figure2B.csv')

# Filter for DIAN_noncarrier series
dian_noncarrier_data = df[df['series'] == 'DIAN_noncarrier']

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(dian_noncarrier_data['time'], dian_noncarrier_data['measurement'], 
         marker='o', linewidth=2, markersize=6, color='blue', alpha=0.7)

# Customize the plot
plt.xlabel('Time (years)', fontsize=12)
plt.ylabel('Measurement (nM)', fontsize=12)
plt.title('DIAN Noncarrier - Time vs Measurement', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the plot
plt.savefig('DIAN_noncarrier_plot.png', dpi=300, bbox_inches='tight')
plt.show()

# Print some basic statistics
print(f"Number of data points: {len(dian_noncarrier_data)}")
print(f"Time range: {dian_noncarrier_data['time'].min():.2f} - {dian_noncarrier_data['time'].max():.2f} years")
print(f"Measurement range: {dian_noncarrier_data['measurement'].min():.4f} - {dian_noncarrier_data['measurement'].max():.4f} nM")
print(f"Mean measurement: {dian_noncarrier_data['measurement'].mean():.4f} nM") 
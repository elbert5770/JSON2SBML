import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
print("Reading CSV file...")
df = pd.read_csv('Chang2019_Figure5A.csv')
print(f"Successfully loaded {len(df)} data points")

# Create figure with subplots for plasma and CSF
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot Plasma data
plasma_data = df[df['observation'] == 'plasma']
plasma_sim = plasma_data[plasma_data['series'] == '36mgsim']
plasma_exp = plasma_data[plasma_data['series'] == '36mgdata']

print(f"Plasma simulation points: {len(plasma_sim)}")
print(f"Plasma experimental points: {len(plasma_exp)}")

ax1.plot(plasma_sim['Time (h)'], plasma_sim['Conc (nM)'], 'b-', linewidth=2, label='Simulation (36mg)')
ax1.scatter(plasma_exp['Time (h)'], plasma_exp['Conc (nM)'], color='red', s=50, marker='o', label='Experimental (36mg)')
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Concentration (nM)')
ax1.set_title('Plasma Concentration vs Time')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')  # Log scale for better visualization

# Plot CSF data
csf_data = df[df['observation'] == 'CSF']
csf_sim = csf_data[csf_data['series'] == '36mgsim']
csf_exp = csf_data[csf_data['series'] == '36mgdata']

print(f"CSF simulation points: {len(csf_sim)}")
print(f"CSF experimental points: {len(csf_exp)}")

ax2.plot(csf_sim['Time (h)'], csf_sim['Conc (nM)'], 'g-', linewidth=2, label='Simulation (36mg)')
ax2.scatter(csf_exp['Time (h)'], csf_exp['Conc (nM)'], color='orange', s=50, marker='s', label='Experimental (36mg)')
ax2.set_xlabel('Time (hours)')
ax2.set_ylabel('Concentration (nM)')
ax2.set_title('CSF Concentration vs Time')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_yscale('log')  # Log scale for better visualization

# Adjust layout and save
plt.tight_layout()
plt.savefig('Chang2019_Figure5A_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'Chang2019_Figure5A_plot.png'")

# Print summary statistics
print("\n" + "="*50)
print("DATA SUMMARY")
print("="*50)
print(f"Total data points: {len(df)}")
print(f"Plasma simulation points: {len(plasma_sim)}")
print(f"Plasma experimental points: {len(plasma_exp)}")
print(f"CSF simulation points: {len(csf_sim)}")
print(f"CSF experimental points: {len(csf_exp)}")

print("\nTime ranges:")
print(f"Plasma simulation: {plasma_sim['Time (h)'].min():.1f} - {plasma_sim['Time (h)'].max():.1f} hours")
print(f"Plasma experimental: {plasma_exp['Time (h)'].min():.1f} - {plasma_exp['Time (h)'].max():.1f} hours")
print(f"CSF simulation: {csf_sim['Time (h)'].min():.1f} - {csf_sim['Time (h)'].max():.1f} hours")
print(f"CSF experimental: {csf_exp['Time (h)'].min():.1f} - {csf_exp['Time (h)'].max():.1f} hours")

print("\nConcentration ranges:")
print(f"Plasma simulation: {plasma_sim['Conc (nM)'].min():.1f} - {plasma_sim['Conc (nM)'].max():.1f} nM")
print(f"Plasma experimental: {plasma_exp['Conc (nM)'].min():.1f} - {plasma_exp['Conc (nM)'].max():.1f} nM")
print(f"CSF simulation: {csf_sim['Conc (nM)'].min():.1f} - {csf_sim['Conc (nM)'].max():.1f} nM")
print(f"CSF experimental: {csf_exp['Conc (nM)'].min():.1f} - {csf_exp['Conc (nM)'].max():.1f} nM") 
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

r = te.loadSBMLModel('combined_master_model.xml')
antimony_model = r.exportToAntimony('combined_master_model.txt')
# save_path = 'combined_master_model.txt'
# with open(save_path, 'w') as f:
#     f.write(antimony_model)
print(r.getReactionIds())
print(r.getCurrentAntimony())
print(te.getODEsFromModel(r))
r.exportToSBML('Antimony_PBPK_model.xml') 

result = r.simulate(0, 100*365*24, 100,['time', '[AB42_Monomer]', '[AB42_Plaque_unbound]'])
# print(r['[AB42_O1_ISF]'],r['[AB42_O25_ISF]'])

# Load the CSV data
csv_data = pd.read_csv('Tellurium_results.csv')

# Create the plot
plt.figure(figsize=(12, 8))

# Plot simulation results
plt.subplot(2, 1, 1)
plt.plot(result['time']/24/365, result['[AB42_Monomer]'], 'b-', label='AB42_Monomer (Simulation)', linewidth=2)
# plt.plot(csv_data['Time']/24/365, csv_data['Ab42_monomer']/0.2505, 'r--', label='AB42_monomer (CSV)', linewidth=2)
# plt.plot(result['time']/24/365, result['[AB40_O1_PVS]'], 'r--', label='AB40_O1_PVS', linewidth=2)
plt.xlabel('Time (hours)')
plt.ylabel('Concentration')
plt.title('AB42 Monomer Comparison')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(result['time']/24/365, result['[AB42_Plaque_unbound]'], 'g-', label='AB42_Plaque (Simulation)', linewidth=2)
plt.plot(csv_data['Time']/24/365, csv_data['Ab42_plaque']/0.2505, 'm--', label='AB42_plaque (CSV)', linewidth=2)
plt.xlabel('Time (hours)')
plt.ylabel('Concentration')
plt.title('AB42 Plaque Comparison')
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig('AB42_comparison_plot.png')
plt.show()
# Also show the original Tellurium plot
# r.plot()
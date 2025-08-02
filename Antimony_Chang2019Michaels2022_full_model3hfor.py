import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def run_simulation():
    r = te.loada(__file__.replace('.py', '.txt'))
    r.setIntegrator('cvode')
    r.integrator.absolute_tolerance = 1e-8
    r.integrator.relative_tolerance = 1e-8
    r.integrator.setValue('stiff', True)
    #result = r.simulate(0, 1000, 10000)
    #result = r.simulate(0, 200000, 200000)
    result = r.simulate(0, 1300000, 1300000, ['time','[Antibody_Plasma]','[Antibody_BrainISF]','[Antibody_LiverVascular]',
    '[Antibody_LungVascular]','[Antibody_LymphNode]','[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_SAS]',
    '[Antibody_LV]','[APP_BrainISF]','[AB42_BrainISF]','[C99_BrainISF]','[AB42_Oligomer_BrainISF]','[AB42_FibrilNumber_BrainISF]','[AB42_FibrilMass_BrainISF]',
    '[AB42_Plasma]','[AB42_SAS]','Fibril_degree_polymerization','[AB42_PlaqueMass_BrainISF]','[AB42_PlaqueNumber_BrainISF]','Plaque_degree_polymerization'])
    
    # Create two-panel subplot layout
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    ax1, ax2 = axes[0]
    ax3, ax4 = axes[1]
    
    # Left panel - first two variables
    ax1.plot(result['time']/24/365, result['[AB42_BrainISF]'], label='AB42_BrainISF',color='red')
    ax1.plot(result['time']/24/365, result['[Antibody_BrainISF]'], label='Antibody_BrainISF',color='cyan')
    ax1.plot(result['time']/24/365, result['[AB42_SAS]'], label='AB42_CSF',color='blue')
    ax1.plot(result['time']/24/365, result['[AB42_Plasma]'], label='AB42_Plasma',color='green')
    # ax1.plot(result['time'], result['[Antibody_Plasma]'], label='Antibody_Plasma')
    # Read the CSV file
    df = pd.read_csv('Fagan2021_Figure2B.csv')
    dian_noncarrier_data = df[df['series'] == 'DIAN_noncarrier']
    ax1.plot(dian_noncarrier_data['time'], dian_noncarrier_data['measurement'], 
         marker='o', linewidth=2, markersize=6, color='blue', alpha=0.7,label='Fagan2021_Figure2B')

    ax1.set_xlabel('Time (years)')
    ax1.set_ylabel('Concentration (nM)')
    ax1.set_title('Panel 1: AB42 and Oligomer')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right panel - second two variables
    ax2.plot(result['time']/24/365, result['[AB42_Oligomer_BrainISF]'], label='AB42_Oligomer_BrainISF',color='red')
    
    ax2.plot(result['time']/24/365, result['[AB42_FibrilMass_BrainISF]'], label='AB42_FibrilMass_BrainISF',color='blue')
    ax2.plot(result['time']/24/365, result['[AB42_PlaqueMass_BrainISF]'], label='AB42_PlaqueMass_BrainISF',color='green')
    ax2.set_xlabel('Time (years)')
    ax2.set_ylabel('Concentration (nM)')
    ax2.set_title('Panel 2: Fibril Mass and Oligomer')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3.plot(result['time']/24/365, result['Fibril_degree_polymerization'], label='Fibril degree of polymerization',color='blue')
    ax3.plot(result['time']/24/365, result['Plaque_degree_polymerization'], label='Plaque degree of polymerization',color='green')
    ax3.set_xlabel('Time (years)')
    ax3.set_ylabel('Dimensionless')
    ax3.set_title('Panel 3: Fibril Degree of Polymerization')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    ax4.plot(result['time']/24/365, result['[AB42_FibrilNumber_BrainISF]'], label='AB42_FibrilNumber_BrainISF',color='blue')
    ax4.plot(result['time']/24/365, result['[AB42_PlaqueNumber_BrainISF]'], label='AB42_PlaqueNumber_BrainISF',color='green')
    ax4.set_xlabel('Time (years)')
    ax4.set_ylabel('Concentration (nM)')
    ax4.set_title('Panel 4: Fibril Number')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    
    plt.savefig(__file__.replace('.py', '.png'))
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    run_simulation()
    
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def add_to_plot1(ax, result,legend=False):
    if legend:
        ax.plot(result['time']/24/365, result['[AB42_BrainISF]'], label='AB42_BrainISF',color='red')
        ax.plot(result['time']/24/365, result['[Antibody_BrainISF]'], label='Antibody_BrainISF',color='cyan')
        ax.plot(result['time']/24/365, result['[AB42_SAS]'], label='AB42_CSF',color='blue')
        ax.plot(result['time']/24/365, result['[AB42_Plasma]'], label='AB42_Plasma',color='green')
    else:
        ax.plot(result['time']/24/365, result['[AB42_BrainISF]'], color='red')
        ax.plot(result['time']/24/365, result['[Antibody_BrainISF]'], color='cyan')
        ax.plot(result['time']/24/365, result['[AB42_SAS]'], color='blue')
        ax.plot(result['time']/24/365, result['[AB42_Plasma]'], color='green')
    return ax

def add_to_plot2(ax, result,legend=False):
    if legend:
        ax.plot(result['time']/24/365, result['[AB42_Oligomer_BrainISF]'], label='AB42_Oligomer_BrainISF',color='red')
        ax.plot(result['time']/24/365, result['[AB42_FibrilMass_BrainISF]'], label='AB42_FibrilMass_BrainISF',color='blue')
        ax.plot(result['time']/24/365, result['[AB42_PlaqueMass_BrainISF]'], label='AB42_PlaqueMass_BrainISF',color='green')
    else:
        ax.plot(result['time']/24/365, result['[AB42_Oligomer_BrainISF]'], color='red')
        ax.plot(result['time']/24/365, result['[AB42_FibrilMass_BrainISF]'], color='blue')
        ax.plot(result['time']/24/365, result['[AB42_PlaqueMass_BrainISF]'], color='green')
    return ax

def add_to_plot3(ax, result,legend=False):
    if legend:
        ax.plot(result['time']/24/365, result['Fibril_degree_polymerization'], label='Fibril degree of polymerization',color='blue')
        ax.plot(result['time']/24/365, result['Plaque_degree_polymerization'], label='Plaque degree of polymerization',color='green')
    else:
        ax.plot(result['time']/24/365, result['Fibril_degree_polymerization'], color='blue')
        ax.plot(result['time']/24/365, result['Plaque_degree_polymerization'], color='green')
    return ax

def add_to_plot4(ax, result,legend=False):
    if legend:
        ax.plot(result['time']/24/365, result['[AB42_FibrilNumber_BrainISF]'], label='AB42_FibrilNumber_BrainISF',color='blue')
        ax.plot(result['time']/24/365, result['[AB42_PlaqueNumber_BrainISF]'], label='AB42_PlaqueNumber_BrainISF',color='green')
    else:
        ax.plot(result['time']/24/365, result['[AB42_FibrilNumber_BrainISF]'], color='blue')
        ax.plot(result['time']/24/365, result['[AB42_PlaqueNumber_BrainISF]'], color='green')
    return ax

def run_simulation():
    r = te.loada(__file__.replace('.py', '.txt'))
    r.setIntegrator('cvode')
    r.integrator.absolute_tolerance = 1e-9
    r.integrator.relative_tolerance = 1e-10
    r.integrator.setValue('stiff', True)
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    ax1, ax2 = axes[0]
    ax3, ax4 = axes[1]


    result1 = r.simulate(0, 69*365*24, 100000, ['time','[Antibody_Plasma]','[Antibody_BrainISF]','[Antibody_LiverVascular]',
    '[Antibody_LungVascular]','[Antibody_LymphNode]','[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_SAS]',
    '[Antibody_LV]','[APP_BrainISF]','[AB42_BrainISF]','[C99_BrainISF]','[AB42_Oligomer_BrainISF]','[AB42_FibrilNumber_BrainISF]','[AB42_FibrilMass_BrainISF]',
    '[AB42_Plasma]','[AB42_SAS]','Fibril_degree_polymerization','[AB42_PlaqueMass_BrainISF]','[AB42_PlaqueNumber_BrainISF]','Plaque_degree_polymerization'])
    # ax1.plot(result1['time']/24/365, result1['[AB42_BrainISF]'], label='AB42_BrainISF',color='red')
    # ax1.plot(result1['time']/24/365, result1['[Antibody_BrainISF]'], label='Antibody_BrainISF',color='cyan')
    # ax1.plot(result1['time']/24/365, result1['[AB42_SAS]'], label='AB42_CSF',color='blue')
    # ax1.plot(result1['time']/24/365, result1['[AB42_Plasma]'], label='AB42_Plasma',color='green')

    # r.integrator.variable_step_size = True
    # result2 = r.simulate(1000, 200000, 200000)
    result2 = r.simulate(69*365*24, 71*365*24, 3000000, ['time','[Antibody_Plasma]','[Antibody_BrainISF]','[Antibody_LiverVascular]',
    '[Antibody_LungVascular]','[Antibody_LymphNode]','[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_SAS]',
    '[Antibody_LV]','[APP_BrainISF]','[AB42_BrainISF]','[C99_BrainISF]','[AB42_Oligomer_BrainISF]','[AB42_FibrilNumber_BrainISF]','[AB42_FibrilMass_BrainISF]',
    '[AB42_Plasma]','[AB42_SAS]','Fibril_degree_polymerization','[AB42_PlaqueMass_BrainISF]','[AB42_PlaqueNumber_BrainISF]','Plaque_degree_polymerization'])
    
    result3 = r.simulate(71*365*24, 71.6*365*24, 3000000, ['time','[Antibody_Plasma]','[Antibody_BrainISF]','[Antibody_LiverVascular]',
    '[Antibody_LungVascular]','[Antibody_LymphNode]','[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_SAS]',
    '[Antibody_LV]','[APP_BrainISF]','[AB42_BrainISF]','[C99_BrainISF]','[AB42_Oligomer_BrainISF]','[AB42_FibrilNumber_BrainISF]','[AB42_FibrilMass_BrainISF]',
    '[AB42_Plasma]','[AB42_SAS]','Fibril_degree_polymerization','[AB42_PlaqueMass_BrainISF]','[AB42_PlaqueNumber_BrainISF]','Plaque_degree_polymerization'])
    
    result4 = r.simulate(71.6*365*24, 100*365*24, 100000, ['time','[Antibody_Plasma]','[Antibody_BrainISF]','[Antibody_LiverVascular]',
    '[Antibody_LungVascular]','[Antibody_LymphNode]','[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_SAS]',
    '[Antibody_LV]','[APP_BrainISF]','[AB42_BrainISF]','[C99_BrainISF]','[AB42_Oligomer_BrainISF]','[AB42_FibrilNumber_BrainISF]','[AB42_FibrilMass_BrainISF]',
    '[AB42_Plasma]','[AB42_SAS]','Fibril_degree_polymerization','[AB42_PlaqueMass_BrainISF]','[AB42_PlaqueNumber_BrainISF]','Plaque_degree_polymerization'])
    
    # Create two-panel subplot layout
    
    
    # Left panel - first two variables
    # ax1.plot(result2['time']/24/365, result2['[AB42_BrainISF]'], label='AB42_BrainISF',color='red')
    # ax1.plot(result2['time']/24/365, result2['[Antibody_BrainISF]'], label='Antibody_BrainISF',color='cyan')
    # ax1.plot(result2['time']/24/365, result2['[AB42_SAS]'], label='AB42_CSF',color='blue')
    # ax1.plot(result2['time']/24/365, result2['[AB42_Plasma]'], label='AB42_Plasma',color='green')
    ax1 = add_to_plot1(ax1, result1,legend=True)
    ax1 = add_to_plot1(ax1, result2)
    ax1 = add_to_plot1(ax1, result3)
    ax1 = add_to_plot1(ax1, result4)
    # ax1.plot(result2['time']/24/365, result2['Anti_ABeta_ISF_sum'], label='Total_Antibody_BrainISF',color='purple')
    # ax1.plot(result2['time'], result2['[Antibody_Plasma]'], label='Antibody_Plasma')
    # Read the CSV file
    df = pd.read_csv('Fagan2021_Figure2B.csv')
    dian_noncarrier_data = df[df['series'] == 'DIAN_noncarrier']
    ax1.plot(dian_noncarrier_data['time'], dian_noncarrier_data['measurement'], 
         marker='o', linewidth=2, markersize=6, color='blue', alpha=0.7,label='Fagan2021_Figure2B')

    ax1.set_xlabel('Time (years)')
    ax1.set_ylabel('Concentration (nM)')
    ax1.set_title('AB42 and Antibody in the CNS and plasma')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right panel - second two variables
    ax2 = add_to_plot2(ax2, result1,legend=True)
    ax2 = add_to_plot2(ax2, result2)
    ax2 = add_to_plot2(ax2, result3)
    ax2 = add_to_plot2(ax2, result4)
    ax2.set_xlabel('Time (years)')
    ax2.set_ylabel('Concentration (nM)')
    ax2.set_title('Fibril and Plaque Mass and Oligomers')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

   
    ax3 = add_to_plot3(ax3, result1,legend=True)
    ax3 = add_to_plot3(ax3, result2)
    ax3 = add_to_plot3(ax3, result3)
    ax3 = add_to_plot3(ax3, result4)
    ax3.set_xlabel('Time (years)')
    ax3.set_ylabel('Dimensionless')
    ax3.set_title('Fibril and Plaque Degree of Polymerization')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    
    ax4 = add_to_plot4(ax4, result1,legend=True)
    ax4 = add_to_plot4(ax4, result2)
    ax4 = add_to_plot4(ax4, result3)
    ax4 = add_to_plot4(ax4, result4)
    ax4.set_xlabel('Time (years)')
    ax4.set_ylabel('Concentration (nM)')
    ax4.set_title('Fibril and Plaque Number')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    
    plt.savefig(__file__.replace('.py', '.png'))
    plt.tight_layout()

    plt.show()


def run_simulation_with_flexible_plot():
    """Example of using the flexible plotting function"""
    r = te.loada(__file__.replace('.py', '.txt'))
    r.setIntegrator('cvode')
    r.integrator.absolute_tolerance = 1e-8
    r.integrator.relative_tolerance = 1e-8
    r.integrator.setValue('stiff', True)
    
    # Run simulation
    result = r.simulate(69*365*24, 74*365*24, 1000000, ['time','[Antibody_Plasma]','[Antibody_BrainISF]','[Antibody_LiverVascular]',
    '[Antibody_LungVascular]','[Antibody_LymphNode]','[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_SAS]',
    '[Antibody_LV]','[APP_BrainISF]','[AB42_BrainISF]','[C99_BrainISF]','[AB42_Oligomer_BrainISF]','[AB42_FibrilNumber_BrainISF]','[AB42_FibrilMass_BrainISF]',
    '[AB42_Plasma]','[AB42_SAS]','Fibril_degree_polymerization','[AB42_PlaqueMass_BrainISF]','[AB42_PlaqueNumber_BrainISF]','Plaque_degree_polymerization'])
    
    # Example 1: Use default settings
    fig1, axes1 = plot_results_flexible(result)
    plt.savefig(__file__.replace('.py', '_flexible_default.png'))
    plt.show()
    
    # Example 2: Custom variables and colors
    custom_variables = [
        ['[AB42_BrainISF]', '[AB42_Plasma]'],
        ['[Antibody_BrainISF]', '[Antibody_Plasma]'],
        ['[AB42_FibrilMass_BrainISF]', '[AB42_PlaqueMass_BrainISF]']
    ]
    
    custom_colors = [
        ['red', 'blue'],
        ['green', 'orange'],
        ['purple', 'brown']
    ]
    
    custom_titles = [
        'AB42 Comparison',
        'Antibody Comparison', 
        'Mass Comparison'
    ]
    
    experimental_data = {
        'file': 'Fagan2021_Figure2B.csv',
        'series': 'DIAN_noncarrier',
        'color': 'blue',
        'label': 'Fagan2021_Figure2B'
    }
    
    fig2, axes2 = plot_results_flexible(
        result, 
        variables_to_plot=custom_variables,
        colors=custom_colors,
        titles=custom_titles,
        experimental_data=experimental_data
    )
    plt.savefig(__file__.replace('.py', '_flexible_custom.png'))
    plt.show()


if __name__ == "__main__":
    run_simulation()
    # Uncomment to test the flexible plotting function
    # run_simulation_with_flexible_plot()
    
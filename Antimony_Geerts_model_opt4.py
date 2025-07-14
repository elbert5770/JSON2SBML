import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize
from K_rates_extrapolate import calculate_k_rates

def calculate_suvr_at_70_years(result, suvr_func):
    """
    Find the model time points closest to 70*365*24 and interpolate AB42 oligomer values
    to calculate SUVR at that specific timepoint.
    
    Parameters:
    result: Simulation result containing time series data
    suvr_func: SUVR calculation function
    
    Returns:
    dict: Dictionary containing interpolated values and calculated SUVR
    """
    target_time = 70 * 365 * 24  # 70 years in hours
    
    # Find the two closest time points
    model_times = result['time']
    time_diffs = np.abs(model_times - target_time)
    closest_indices = np.argsort(time_diffs)[:2]
    
    # Get the two closest time points
    t1, t2 = model_times[closest_indices[0]], model_times[closest_indices[1]]
    print(f"Closest time points to 70 years: {t1/24/365:.2f} years and {t2/24/365:.2f} years")
    
    # Interpolate values for all AB42 oligomers (O2 through O25)
    interpolated_values = {}
    
    for i in range(2, 26):  # O2 through O25
        species_name = f'[AB42_O{i}_ISF]'
        if species_name in result.colnames:
            v1, v2 = result[species_name][closest_indices[0]], result[species_name][closest_indices[1]]
            
            # Linear interpolation
            if t1 != t2:
                interpolated_value = v1 + (v2 - v1) * (target_time - t1) / (t2 - t1)
            else:
                interpolated_value = v1
                
            interpolated_values[species_name] = interpolated_value
            # print(f"{species_name}: {interpolated_value:.6f}")
        else:
            # If species not available, set to 0
            interpolated_values[species_name] = 0.0
            print(f"{species_name}: Not available in simulation result")
    
    # Calculate oligomer weighted sum (O2-O17)
    oligomer_weighted_sum = interpolated_values['[AB42_O2_ISF]'] * 1
    for i in range(3, 18):
        oligomer_weighted_sum += interpolated_values[f'[AB42_O{i}_ISF]'] * (i-1)
    
    # Calculate proto weighted sum (O18-O24)
    proto_weighted_sum = interpolated_values['[AB42_O18_ISF]'] * 17
    for i in range(19, 25):
        proto_weighted_sum += interpolated_values[f'[AB42_O{i}_ISF]'] * (i-1)
    
    # Get plaque value (O25)
    plaque_sum = interpolated_values['[AB42_O25_ISF]']
    
    # Calculate SUVR at 70 years
    suvr_at_70 = suvr_func(oligomer_weighted_sum, proto_weighted_sum, plaque_sum)
    
    # Ensure SUVR is a scalar value
    if hasattr(suvr_at_70, '__len__'):
        suvr_at_70 = suvr_at_70[0] if len(suvr_at_70) > 0 else 1.0
    
    print(f"\nCalculated values at 70 years:")
    print(f"Oligomer weighted sum: {oligomer_weighted_sum:.6f}")
    print(f"Proto weighted sum: {proto_weighted_sum:.6f}")
    print(f"Plaque sum: {plaque_sum:.6f}")
    print(f"SUVR at 70 years: {suvr_at_70:.6f}")
    
    return {
        'interpolated_values': interpolated_values,
        'oligomer_weighted_sum': oligomer_weighted_sum,
        'proto_weighted_sum': proto_weighted_sum,
        'plaque_sum': plaque_sum,
        'suvr_at_70': suvr_at_70,
        'closest_times': [t1, t2]
    }

def run_optimization_and_simulation():
    """
    Main function to run optimization and simulation.
    Wraps all functionality to avoid global variables.
    """
    
    # Helper to interpolate model output to data times
    def interpolate_model_to_data_times(model_times, model_values, data_times):
        return np.interp(data_times, model_times, model_values)

    # Objective function for optimization
    def create_objective(csv_data, r):
        def objective(params):
            IDE_activity_ISF_val, k_APP_production_val, k_O1_O2_AB42_ISF_val, k_O2_O3_AB42_ISF_val, k_O2_O1_AB42_ISF_val, k_O3_O2_AB42_ISF_val, IDE_conc_ISF_val, k_O24_O12_AB42_ISF_val, Baseline_AB42_O_P_val = params

            # Reload model and set parameters
            r.reset()
            r['Microglia'] = IDE_activity_ISF_val
            r['k_APP_production'] = k_APP_production_val
            r['k_O1_O2_AB42_ISF'] = k_O1_O2_AB42_ISF_val
            r['k_O2_O3_AB42_ISF'] = k_O2_O3_AB42_ISF_val
            r['k_O2_O1_AB42_ISF'] = k_O2_O1_AB42_ISF_val
            r['k_O3_O2_AB42_ISF'] = k_O3_O2_AB42_ISF_val
            r['IDE_conc_ISF'] = IDE_conc_ISF_val
            r['k_O24_O12_AB42_ISF'] = k_O24_O12_AB42_ISF_val
            r['Baseline_AB42_O_P'] = Baseline_AB42_O_P_val
            rates = calculate_k_rates(k_O1_O2_AB42_ISF_val, k_O2_O3_AB42_ISF_val, k_O2_O1_AB42_ISF_val, k_O3_O2_AB42_ISF_val)
            # print(rates)
            oligomer_sizes = list(range(4, 25))
            for i, size in enumerate(oligomer_sizes):
        
                # Oligomer rates (size < 17)
                # rates[f'k_O{size-1}_O{size}_AB40_ISF'] = kf_forty[i]
                # rates[f'k_O{size}_O{size-1}_AB40_ISF'] = kb_forty[i]
                r[f'k_O{size-1}_O{size}_AB42_ISF'] = rates[f'k_O{size-1}_O{size}_AB42_ISF'] 
                r[f'k_O{size}_O{size-1}_AB42_ISF'] = rates[f'k_O{size}_O{size-1}_AB42_ISF']
            
            # Simulate
            try:
                result = r.simulate(0, 20*365*24, 1000)
            except:
                print("Error in simulation")
                return 100
            try:
                result = r.simulate(20*365*24, 100*365*24, 1000, ['time', '[AB42_O1_ISF]', '[AB42_O2_ISF]', '[AB42_O3_ISF]', '[AB42_O4_ISF]', '[AB42_O5_ISF]', '[AB42_O6_ISF]', '[AB42_O7_ISF]', '[AB42_O8_ISF]', '[AB42_O9_ISF]', '[AB42_O10_ISF]', '[AB42_O11_ISF]', '[AB42_O12_ISF]', '[AB42_O13_ISF]', '[AB42_O14_ISF]', '[AB42_O15_ISF]', '[AB42_O16_ISF]', '[AB42_O17_ISF]', '[AB42_O18_ISF]', '[AB42_O19_ISF]', '[AB42_O20_ISF]', '[AB42_O21_ISF]', '[AB42_O22_ISF]', '[AB42_O23_ISF]', '[AB42_O24_ISF]', '[AB42_O25_ISF]'])
            except:
                print("Error in simulation")
                return 100
            model_times = result['time']
            model_values = result['[AB42_O1_ISF]']

            # Interpolate model output to data times
            data_times = csv_data['time'].values
            data_measurements = csv_data['measurement'].values
            model_at_data_times = interpolate_model_to_data_times(model_times, model_values, data_times)
            # print(model_at_data_times, data_measurements)
            # Compute mean squared error
            mse = np.mean((model_at_data_times - data_measurements) ** 2)
            
            suvr_70_results = calculate_suvr_at_70_years(result, suvr)
            suvr_70_mse = suvr_70_results['suvr_at_70']
            mse = mse + ((suvr_70_mse - 1.4) ** 2)*5
            mse = mse + (suvr_70_results['plaque_sum']-5000)**2 / 50000
            print(suvr_70_results['plaque_sum'])
            print(mse, IDE_activity_ISF_val, k_APP_production_val, k_O1_O2_AB42_ISF_val, IDE_conc_ISF_val, k_O2_O3_AB42_ISF_val, k_O2_O1_AB42_ISF_val, k_O3_O2_AB42_ISF_val, k_O24_O12_AB42_ISF_val, Baseline_AB42_O_P_val)
            
            return mse
        return objective

    # SUVR calculation function
    def suvr(oligo, proto, plaque, C1=2.5, C2=400000, C3=1.3, Hill=3.5):
        """
        Calculate SUVR using the provided formula.
        
        Parameters:
        oligo, proto, plaque: input oligomer values
        C1, C2, C3, Hill: constants from the formula
        
        Returns:
        SUVR: predicted SUVR value
        """
        numerator = oligo + proto + C3 * 24.0 * plaque
        denominator = numerator**Hill + C2**Hill
        
        # Handle scalar values properly
        if hasattr(denominator, '__len__'):
            # If it's an array
            if denominator.any() == 0:
                return 1.0  # Avoid division by zero
        else:
            # If it's a scalar
            if denominator == 0:
                return 1.0  # Avoid division by zero
                
        suvr = 1.0 + C1 * (numerator**Hill) / denominator
        return suvr

    # Load model
    r = te.loada("./Antimony_Geerts_model_opt1.txt")
    print(r.getReactionIds())
    print(r.getCurrentAntimony())
    print(te.getODEsFromModel(r))
    r.exportToSBML('Antimony_PBPK_model.xml') 

    # Load the CSV data
    csv_data = pd.read_csv('Geerts 2023 Figure 3C.csv')

    # Create objective function with data
    objective = create_objective(csv_data, r)

    # Initial guess (use current values)
    initial_guess = [r['Microglia'], r['k_APP_production'],r['k_O1_O2_AB42_ISF'],r['k_O2_O3_AB42_ISF'],r['k_O2_O1_AB42_ISF'],r['k_O3_O2_AB42_ISF'],r['IDE_conc_ISF'],r['k_O24_O12_AB42_ISF'],r['Baseline_AB42_O_P']]
    print(initial_guess)
    # [1.0, 75.0, 0.003564, 0.01368, 45.72, 1e-05, 3.0, 100.0, 5e-05]
    # Bounds (set as appropriate)
    bounds = [(1e-3, 1000), (1e-3, 1000), (1e-6, 1), (1e-6, 1), (1e-3, 100), (1e-8, 1), (1e-3, 100), (1, 1000), (1e-8, 1)]  # Adjust as needed

    # Run optimization
    opt_result = minimize(objective, initial_guess, bounds=bounds, method='Nelder-Mead')
    print("Optimized Microglia:", opt_result.x[0])
    print("Optimized k_APP_production:", opt_result.x[1])
    print("Optimized k_O1_O2_AB42_ISF:", opt_result.x[2])
    print("Optimized k_O2_O3_AB42_ISF:", opt_result.x[3])
    print("Optimized k_O2_O1_AB42_ISF:", opt_result.x[4])
    print("Optimized k_O3_O2_AB42_ISF:", opt_result.x[5])
    print("Optimized IDE_conc_ISF:", opt_result.x[6])
    print("Optimized k_O24_O12_AB42_ISF:", opt_result.x[7])
    print("Optimized Baseline_AB42_O_P:", opt_result.x[8])
    # Update model with optimized parameters
    r.reset()
    # rr = te.loada("./Antimony_Geerts_model_opt1.txt")
    r['Microglia'] = opt_result.x[0]
    r['k_APP_production'] = opt_result.x[1]
    r['k_O1_O2_AB42_ISF'] = opt_result.x[2]
    r['k_O2_O3_AB42_ISF'] = opt_result.x[3]
    r['k_O2_O1_AB42_ISF'] = opt_result.x[4]
    r['k_O3_O2_AB42_ISF'] = opt_result.x[5]
    r['IDE_conc_ISF'] = opt_result.x[6]
    r['k_O24_O12_AB42_ISF'] = opt_result.x[7]
    r['Baseline_AB42_O_P'] = opt_result.x[8]
    rates = calculate_k_rates(opt_result.x[2], opt_result.x[3], opt_result.x[4], opt_result.x[5])
    print(rates)
    oligomer_sizes = list(range(4, 25))
    for i, size in enumerate(oligomer_sizes):

        # Oligomer rates (size < 17)
        # rates[f'k_O{size-1}_O{size}_AB40_ISF'] = kf_forty[i]
        # rates[f'k_O{size}_O{size-1}_AB40_ISF'] = kb_forty[i]
        r[f'k_O{size-1}_O{size}_AB42_ISF'] = rates[f'k_O{size-1}_O{size}_AB42_ISF'] 
        r[f'k_O{size}_O{size-1}_AB42_ISF'] = rates[f'k_O{size}_O{size-1}_AB42_ISF']
    print(r['Microglia'], r['k_APP_production'], r['k_O1_O2_AB42_ISF'],  r['k_O2_O3_AB42_ISF'], r['k_O2_O1_AB42_ISF'], r['k_O3_O2_AB42_ISF'],r['IDE_conc_ISF'], r['k_O24_O12_AB42_ISF'], r['Baseline_AB42_O_P'], opt_result.x[0], opt_result.x[1], opt_result.x[2], opt_result.x[3], opt_result.x[4], opt_result.x[5], opt_result.x[6], opt_result.x[7], opt_result.x[8])
    # Simulate for 100 years like in Julia file
    result = r.simulate(0, 20*365*24, 1000)
    result = r.simulate(20*365*24, 100*365*24, 1000, ['time', 
        '[AB42_O1_ISF]', '[AB42_O25_ISF]', '[AB42_O1_SAS]',  '[IDE_activity_ISF]',
        '[AB42_O2_ISF]', '[AB42_O3_ISF]', '[AB42_O4_ISF]', '[AB42_O5_ISF]', '[AB42_O6_ISF]', '[AB42_O7_ISF]', 
        '[AB42_O8_ISF]', '[AB42_O9_ISF]', '[AB42_O10_ISF]', '[AB42_O11_ISF]', '[AB42_O12_ISF]', '[AB42_O13_ISF]',
        '[AB42_O14_ISF]', '[AB42_O15_ISF]', '[AB42_O16_ISF]', '[AB42_O17_ISF]', '[AB42_O18_ISF]', '[AB42_O19_ISF]',
        '[AB42_O20_ISF]', '[AB42_O21_ISF]', '[AB42_O22_ISF]', '[AB42_O23_ISF]', '[AB42_O24_ISF]'])
    print(r['[AB42_O1_ISF]'],r['[AB42_O25_ISF]'])

    return r, result, csv_data, suvr



def create_plots(r, result, csv_data, suvr):
    """
    Create plots using the simulation results.
    """
    # Create the figure with 6 subplots in 3x2 grid
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('Geerts Model Simulation Results', fontsize=16)

    # Get time in years
    time_years = result['time']/24/365

    # Plot 1: Oligomers
    ax1 = axes[0, 0]
    oligomer_sum = result['[AB42_O2_ISF]']
    for i in range(3, 18):
        oligomer_sum += result[f'[AB42_O{i}_ISF]']
    ax1.plot(time_years, oligomer_sum, label='Oligomers', linewidth=2)

    oligomer_weighted_sum = result['[AB42_O2_ISF]'] * 1
    for i in range(3, 18):
        oligomer_weighted_sum += result[f'[AB42_O{i}_ISF]'] * (i-1)
    ax1.plot(time_years, oligomer_weighted_sum, label='Oligomers weighted', linewidth=2)
    ax1.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax1.plot([70], [12000], 'o', color='orange', markersize=14)
    ax1.set_xlabel('Time (years)')
    ax1.set_ylabel('Concentration')
    ax1.set_title('Oligomers')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Plot 2: Proto
    ax2 = axes[0, 1]
    proto_sum = result['[AB42_O18_ISF]']
    for i in range(19, 25):
        proto_sum += result[f'[AB42_O{i}_ISF]']
    ax2.plot(time_years, proto_sum, label='Proto', linewidth=2)

    proto_weighted_sum = result['[AB42_O18_ISF]'] * 17
    for i in range(19, 25):
        proto_weighted_sum += result[f'[AB42_O{i}_ISF]'] * (i-1)
    ax2.plot(time_years, proto_weighted_sum, label='Proto weighted', linewidth=2)
    ax2.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax2.plot([70], [70000], 'o', color='orange', markersize=14)
    ax2.set_xlabel('Time (years)')
    ax2.set_ylabel('Concentration')
    ax2.set_title('Proto')
    ax2.legend(loc='upper left', fontsize=7)
    ax2.grid(True)

    # Plot 3: SUVR
    ax3 = axes[1, 0]
    plaque_sum = result['[AB42_O25_ISF]']
    suvr_values = suvr(oligomer_weighted_sum, proto_weighted_sum, plaque_sum)
    ax3.plot(time_years, suvr_values, label='SUVR', linewidth=2)
    ax3.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax3.plot([70], [1.4], 'o', color='blue', markersize=14)
    ax3.set_xlabel('Time (years)')
    ax3.set_ylabel('Concentration')
    ax3.set_title('SUVR')
    ax3.legend(loc='upper left')
    ax3.grid(True)

    # Plot 4: AB42_O1_ISF and AB42_O25_ISF
    ax4 = axes[1, 1]
    ax4.plot(time_years, result['[AB42_O1_ISF]'], label='AB42_O1_ISF', linewidth=2)
    ax4.plot(time_years, result['[AB42_O1_SAS]'], label='AB42_O1_CSF', linewidth=2)
    ax4.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax4.plot([70], [1.3], 'o', color='blue', markersize=14)
    ax4.plot(csv_data['time']/24/365, csv_data['measurement'], 'r.', label='Monomer', markersize=4)
    ax4.set_xlabel('Time (years)')
    ax4.set_ylabel('Concentration')
    ax4.set_title('AB42_O1_ISF and AB42_O1_CSF')
    ax4.legend(loc='upper right')
    ax4.grid(True)

    # Plot 5: IDE_activity_ISF
    ax5 = axes[2, 0]
    ax5.plot(time_years, result['[IDE_activity_ISF]'], label='IDE_activity_ISF', linewidth=2)
    ax5.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    # ax5.plot([70], [1.3], 'o', color='blue', markersize=14)
    ax5.set_xlabel('Time (years)')
    ax5.set_ylabel('Concentration')
    ax5.set_title('IDE_activity_ISF')
    ax5.legend(loc='upper right')
    ax5.grid(True)

    # Plot 6: AB40_O1_central
    ax6 = axes[2, 1]
    ax6.plot(time_years, result['[AB42_O25_ISF]'], label='AB42_O25_ISF', linewidth=2)
    ax6.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    # ax6.plot([70], [1.3], 'o', color='blue', markersize=14)
    ax6.set_xlabel('Time (years)')
    ax6.set_ylabel('Concentration')
    ax6.set_title('Plaque')
    ax6.legend(loc='upper right')
    ax6.grid(True)

    plt.tight_layout()
    plt.savefig(__file__.replace('.py', '.png'), dpi=300, bbox_inches='tight')
    plt.show()

# Main execution
if __name__ == "__main__":
    # Run optimization and simulation
    r, result, csv_data, suvr = run_optimization_and_simulation()
    
    # Calculate SUVR at 70 years and store interpolated values
    print("\n" + "="*50)
    print("CALCULATING SUVR AT 70 YEARS")
    print("="*50)
    suvr_70_results = calculate_suvr_at_70_years(result, suvr)
    
    # Store the results for further use
    interpolated_values = suvr_70_results['interpolated_values']
    oligomer_weighted_sum_70 = suvr_70_results['oligomer_weighted_sum']
    proto_weighted_sum_70 = suvr_70_results['proto_weighted_sum']
    plaque_sum_70 = suvr_70_results['plaque_sum']
    suvr_at_70 = suvr_70_results['suvr_at_70']
    
    print(f"\nFinal SUVR at 70 years: {suvr_at_70:.6f}")
    print("="*50)
    
    # Create plots
    create_plots(r, result, csv_data, suvr)




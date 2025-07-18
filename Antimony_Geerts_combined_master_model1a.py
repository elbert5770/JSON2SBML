import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize
from K_rates_extrapolate import calculate_k_rates

def calculate_suvr_at_year(result, suvr_func, year):
    """
    Find the model time points closest to year*365*24 and interpolate AB42 oligomer values
    to calculate SUVR at that specific timepoint.
    
    Parameters:
    result: Simulation result containing time series data
    suvr_func: SUVR calculation function
    year: The target year to calculate SUVR for.
    
    Returns:
    dict: Dictionary containing interpolated values and calculated SUVR
    """
    target_time = year * 365 * 24  # target years in hours
    
    # Find the two closest time points
    model_times = result['time']
    time_diffs = np.abs(model_times - target_time)
    closest_indices = np.argsort(time_diffs)[:2]
    
    # Get the two closest time points
    t1, t2 = model_times[closest_indices[0]], model_times[closest_indices[1]]
    # print(f"Closest time points to {year} years: {t1/24/365:.2f} years and {t2/24/365:.2f} years")
    
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
    
    # Calculate SUVR at specified year
    suvr_at_year = suvr_func(oligomer_weighted_sum, proto_weighted_sum, plaque_sum)
    
    # Ensure SUVR is a scalar value
    if hasattr(suvr_at_year, '__len__'):
        suvr_at_year = suvr_at_year[0] if len(suvr_at_year) > 0 else 1.0
    
    # print(f"\nCalculated values at {year} years:")
    # print(f"Oligomer weighted sum: {oligomer_weighted_sum:.6f}")
    # print(f"Proto weighted sum: {proto_weighted_sum:.6f}")
    # print(f"Plaque sum: {plaque_sum:.6f}")
    # print(f"SUVR at {year} years: {suvr_at_year:.6f}")
    
    return {
        'interpolated_values': interpolated_values,
        'oligomer_weighted_sum': oligomer_weighted_sum,
        'proto_weighted_sum': proto_weighted_sum,
        'plaque_sum': plaque_sum,
        'suvr_at_year': suvr_at_year,
        'closest_times': [t1, t2]
    }

def run_optimization_and_simulation():
    """
    Main function to run optimization and simulation.
    Wraps all functionality to avoid global variables.
    """
    # Define the parameters
    Microglia_EC50_AB42_APOE4 = 300 #Not APOE4; Microglia_EC50_AB42 has nanomol / L
    Microglia_Vmax_AB42_APOE4 = 0.0001 #Not APOE4; Microglia_Vmax_AB42 has nanomol / L / h
    Microglia_EC50_AB42_nonAPOE4 = 120 #Not APOE4; Microglia_EC50_AB42 has nanomol / L
    Microglia_Vmax_AB42_nonAPOE4 = 0.00015 #Not APOE4; Microglia_Vmax_AB42 has nanomol / L / h

    def run_simulation_and_calculate_mse(r, param_values, csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, interpolate_model_to_data_times,Microglia_EC50_AB42_type,Microglia_Vmax_AB42_type):
        """
        Runs the simulation with given parameters and calculates the mean squared error.
        """
        r.reset()
        for name, value in param_values.items():
            r[name] = value
        r['Microglia_EC50_AB42'] = Microglia_EC50_AB42_type
        r['Microglia_Vmax_AB42'] = Microglia_Vmax_AB42_type
        rates = calculate_k_rates(r['k_O1_O2_AB42_ISF'], r['k_O2_O3_AB42_ISF'], r['k_O2_O1_AB42_ISF'], r['k_O3_O2_AB42_ISF'])
        oligomer_sizes = list(range(4, 25))
        for i, size in enumerate(oligomer_sizes):
            r[f'k_O{size-1}_O{size}_AB42_ISF'] = rates[f'k_O{size-1}_O{size}_AB42_ISF']
            r[f'k_O{size}_O{size-1}_AB42_ISF'] = rates[f'k_O{size}_O{size-1}_AB42_ISF']

        try:
            result = r.simulate(0, 20*365*24, 1000)
            result = r.simulate(20*365*24, 100*365*24, 1000, ['time', '[AB42_O1_ISF]', '[AB42_O2_ISF]', '[AB42_O3_ISF]', '[AB42_O4_ISF]', '[AB42_O5_ISF]', '[AB42_O6_ISF]', '[AB42_O7_ISF]', '[AB42_O8_ISF]', '[AB42_O9_ISF]', '[AB42_O10_ISF]', '[AB42_O11_ISF]', '[AB42_O12_ISF]', '[AB42_O13_ISF]', '[AB42_O14_ISF]', '[AB42_O15_ISF]', '[AB42_O16_ISF]', '[AB42_O17_ISF]', '[AB42_O18_ISF]', '[AB42_O19_ISF]', '[AB42_O20_ISF]', '[AB42_O21_ISF]', '[AB42_O22_ISF]', '[AB42_O23_ISF]', '[AB42_O24_ISF]', '[AB42_O25_ISF]'])
        except:
            print("Error in simulation")
            return None, 100

        model_times = result['time']
        model_values = result['[AB42_O1_ISF]']

        ISF_times_ApoE = csv_data_3C_ApoE['time'].values
        ISF_measurements_ApoE = csv_data_3C_ApoE['measurement'].values
        ISF_model_ApoE_at_data_times = interpolate_model_to_data_times(model_times, model_values, ISF_times_ApoE)
        mse = np.sum((ISF_model_ApoE_at_data_times - ISF_measurements_ApoE) ** 2)

        ISF_times_nonApoE = csv_data_3C_nonApoE['time'].values
        ISF_measurements_nonApoE = csv_data_3C_nonApoE['measurement'].values
        ISF_model_nonApoE_at_data_times = interpolate_model_to_data_times(model_times, model_values, ISF_times_nonApoE)
        mse = mse + np.sum((ISF_model_nonApoE_at_data_times - ISF_measurements_nonApoE) ** 2)

        suvr_times = csv_data_3A_ApoE['time'].values
        suvr_measurements = csv_data_3A_ApoE['measurement'].values
        suvr_model_ApoE_at_data_times = interpolate_model_to_data_times(model_times, model_values, suvr_times)
        mse = mse + np.sum((suvr_model_ApoE_at_data_times - suvr_measurements) ** 2)
        
        suvr_times = csv_data_3A_nonApoE['time'].values
        suvr_measurements = csv_data_3A_nonApoE['measurement'].values
        suvr_model_nonApoE_at_data_times = interpolate_model_to_data_times(model_times, model_values, suvr_times)
        mse = mse + np.sum((suvr_model_nonApoE_at_data_times - suvr_measurements) ** 2)
        return result, mse

    # Helper to interpolate model output to data times
    def interpolate_model_to_data_times(model_times, model_values, data_times):
        return np.interp(data_times, model_times, model_values)

    # Objective function for optimization
    def create_objective(csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, csv_data_3A_nonApoE, r, param_names):
        def objective(params):
            param_values = dict(zip(param_names, params))

            result1, mse1 = run_simulation_and_calculate_mse(r, param_values, csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, interpolate_model_to_data_times,Microglia_EC50_AB42_APOE4,Microglia_Vmax_AB42_APOE4)

            if result1 is None:
                return 0
            
            time = 70
            suvr_results = calculate_suvr_at_year(result1, suvr, time)
            mse1 = mse1 + (suvr_results['suvr_at_year']-1.394)**2 / 1.394
            mse1 = mse1 + (suvr_results['plaque_sum']-5102)**2 / 5102 /10
            mse1 = mse1 + (suvr_results['oligomer_weighted_sum']-12211)**2 / 12211 / 10
            mse1 = mse1 + (suvr_results['proto_weighted_sum']-70000)**2 / 70000 / 10
            
            # suvr_70_results = calculate_suvr_at_year(result1, suvr, 70)
            # mse1 = mse1 + ((suvr_70_results['suvr_at_year'] - 1.4) ** 2)/1.4
            # mse1 = mse1 + (suvr_70_results['plaque_sum']-5000)**2 / 5000 
            # mse1 = mse1 + (suvr_70_results['oligomer_weighted_sum']-12000)**2 / 12000 /10
            # mse1 = mse1 + (suvr_70_results['proto_weighted_sum']-70000)**2 / 70000 /10


            # print(suvr_70_results['plaque_sum'])
            print(f"mse1: {mse1}, params: {param_values}")
            
            result2, mse2 = run_simulation_and_calculate_mse(r, param_values, csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, interpolate_model_to_data_times,Microglia_EC50_AB42_nonAPOE4,Microglia_Vmax_AB42_nonAPOE4)

            if result2 is None:
                return 0
            
            time = 74
            suvr_results = calculate_suvr_at_year(result2, suvr, time)
            mse2 = mse2 + (suvr_results['suvr_at_year']-1.623)**2 / 1.623
            mse2 = mse2 + (suvr_results['plaque_sum']-6028)**2 / 6028 /10
            mse2 = mse2 + (suvr_results['oligomer_weighted_sum']-12307)**2 / 12307 /10
            mse2 = mse2 + (suvr_results['proto_weighted_sum']-70168)**2 / 70168 / 10

            # suvr_70_results = calculate_suvr_at_year(result2, suvr, 70)
            # mse2 = mse2 + (suvr_70_results['plaque_sum']-5000)**2 / 5000 
            # mse2 = mse2 + (suvr_70_results['oligomer_weighted_sum']-12000)**2 / 12000 /10
            # mse2 = mse2 + (suvr_70_results['proto_weighted_sum']-70000)**2 / 70000 /10

            mse = mse1 + mse2
            # print(suvr_70_results['plaque_sum'])
            print(f"mse: {mse}, params: {param_values}")
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
    r = te.loada(__file__.replace('.py', '.txt'))
    print(r.getReactionIds())
    print(r.getCurrentAntimony())
    print(te.getODEsFromModel(r))
    # r.exportToSBML('Antimony_PBPK_model.xml') 

    # Load the CSV data
    csv_data_3 = pd.read_csv('Geerts 2023 Figure 3 units.csv')
    csv_data_3C = csv_data_3[csv_data_3['observation'].str.lower() == 'isf_ab42'].copy()
    csv_data_3A = csv_data_3[csv_data_3['observation'].str.lower() == 'suvr'].copy()
    # For csv_data_3C
    
    csv_data_3C_ApoE = csv_data_3C[csv_data_3C['series'].str.lower() == 'apoe4'].copy()
    csv_data_3C_nonApoE = csv_data_3C[csv_data_3C['series'].str.lower() == 'nonapoe4'].copy()
    
    # For csv_data_3A
   
    csv_data_3A_ApoE = csv_data_3A[csv_data_3A['series'].str.lower() == 'apoe4'].copy()
    csv_data_3A_nonApoE = csv_data_3A[csv_data_3A['series'].str.lower() == 'nonapoe4'].copy()
    

    # Define parameters to be optimized, with their bounds
    params_to_optimize = {
        'k_APP_production': (1e-3, 1000),
        'k_O1_O2_AB42_ISF': (1e-6, 1),
        'k_O2_O3_AB42_ISF': (1e-6, 1),
        'k_O2_O1_AB42_ISF': (1e-3, 200),
        'k_O3_O2_AB42_ISF': (1e-15, 1),
        'IDE_conc_ISF': (1e-3, 100),
        'k_O24_O12_AB42_ISF': (1, 1000),
        'Baseline_AB42_O_P': (1e-8, 1)
    }
    param_names = list(params_to_optimize.keys())
    bounds = list(params_to_optimize.values())
    # Read 'Geerts 2023 Figure 7.csv'
    # csv_data_7 = pd.read_csv('Geerts 2023 Figure 7.csv')

    # csv_data_7_proto = csv_data_7[csv_data_7['observation'].str.lower() == 'proto'].copy()
    # csv_data_7_plaque = csv_data_7[csv_data_7['observation'].str.lower() == 'plaque'].copy()
    # csv_data_7_suvr = csv_data_7[csv_data_7['observation'].str.lower() == 'suvr'].copy()
    # csv_data_7_oligomer = csv_data_7[csv_data_7['observation'].str.lower() == 'oligomer'].copy()
    # csv_data_7_proto_placebo = csv_data_7_proto[csv_data_7_proto['series'].str.lower() == 'placebo'].copy()
    # csv_data_7_plaque_placebo = csv_data_7_plaque[csv_data_7_plaque['series'].str.lower() == 'placebo'].copy()
    # csv_data_7_suvr_placebo = csv_data_7_suvr[csv_data_7_suvr['series'].str.lower() == 'placebo'].copy()
    # csv_data_7_oligomer_placebo = csv_data_7_oligomer[csv_data_7_oligomer['series'].str.lower() == 'placebo'].copy()
 


    # # Create objective function with data
    # objective = create_objective(csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, csv_data_3A_nonApoE, r, param_names)

    # # Initial guess (use current values from model)
    # initial_guess = [r[name] for name in param_names]
    # print(f"Initial guess: {initial_guess}")
    
    # # Run optimization
    # opt_result = minimize(objective, initial_guess, bounds=bounds, method='Nelder-Mead')
    
    # print("\nOptimized Parameters:")
    # for i, name in enumerate(param_names):
    #     print(f"  {name}: {opt_result.x[i]}")


    # Update model with optimized parameters
    r.reset()
    # for i, name in enumerate(param_names):
    #     r[name] = opt_result.x[i]
    # r['Microglia_EC50_AB42'] = Microglia_EC50_AB42_APOE4
    # r['Microglia_Vmax_AB42'] = Microglia_Vmax_AB42_APOE4
    rates = calculate_k_rates(r['k_O1_O2_AB42'], r['k_O2_O3_AB42'], r['k_O2_O1_AB42'], r['k_O3_O2_AB42'])
    print(rates)
    oligomer_sizes = list(range(4, 25))
    for i, size in enumerate(oligomer_sizes):

        # Oligomer rates (size < 17)
        # rates[f'k_O{size-1}_O{size}_AB40_ISF'] = kf_forty[i]
        # rates[f'k_O{size}_O{size-1}_AB40_ISF'] = kb_forty[i]
        r[f'k_O{size-1}_O{size}_AB42'] = rates[f'k_O{size-1}_O{size}_AB42_ISF'] 
        r[f'k_O{size}_O{size-1}_AB42'] = rates[f'k_O{size}_O{size-1}_AB42_ISF']
    
    # print("\nFinal parameter values in model:")
    # for name in param_names:
    #     print(f"  {name}: {r[name]}")

    # Simulate for 100 years like in Julia file
    result1 = r.simulate(0, 20*365*24, 1000)
    result1 = r.simulate(20*365*24, 100*365*24, 1000, ['time', 
        '[AB42_O1_ISF]', '[AB42_O25_ISF]',
        '[AB42_O2_ISF]', '[AB42_O3_ISF]', '[AB42_O4_ISF]', '[AB42_O5_ISF]', '[AB42_O6_ISF]', '[AB42_O7_ISF]', 
        '[AB42_O8_ISF]', '[AB42_O9_ISF]', '[AB42_O10_ISF]', '[AB42_O11_ISF]', '[AB42_O12_ISF]', '[AB42_O13_ISF]',
        '[AB42_O14_ISF]', '[AB42_O15_ISF]', '[AB42_O16_ISF]', '[AB42_O17_ISF]', '[AB42_O18_ISF]', '[AB42_O19_ISF]',
        '[AB42_O20_ISF]', '[AB42_O21_ISF]', '[AB42_O22_ISF]', '[AB42_O23_ISF]', '[AB42_O24_ISF]'])
    print(r['[AB42_O1_ISF]'],r['[AB42_O25_ISF]'])

# Update model with optimized parameters
    r.reset()
    # for i, name in enumerate(param_names):
    #     r[name] = opt_result.x[i]
    # r['Microglia_EC50_AB42'] = Microglia_EC50_AB42_nonAPOE4
    # r['Microglia_Vmax_AB42'] = Microglia_Vmax_AB42_nonAPOE4
    rates = calculate_k_rates(r['k_O1_O2_AB42'], r['k_O2_O3_AB42'], r['k_O2_O1_AB42'], r['k_O3_O2_AB42'])
    print(rates)
    oligomer_sizes = list(range(4, 25))
    for i, size in enumerate(oligomer_sizes):

        # Oligomer rates (size < 17)
        # rates[f'k_O{size-1}_O{size}_AB40_ISF'] = kf_forty[i]
        # rates[f'k_O{size}_O{size-1}_AB40_ISF'] = kb_forty[i]
        r[f'k_O{size-1}_O{size}_AB42'] = rates[f'k_O{size-1}_O{size}_AB42_ISF'] 
        r[f'k_O{size}_O{size-1}_AB42'] = rates[f'k_O{size}_O{size-1}_AB42_ISF']
    
    # print("\nFinal parameter values in model:")
    # for name in param_names:
    #     print(f"  {name}: {r[name]}")

    # Simulate for 100 years like in Julia file
    result2 = r.simulate(0, 20*365*24, 1000)
    result2 = r.simulate(20*365*24, 100*365*24, 1000, ['time', 
        '[AB42_O1_ISF]', '[AB42_O25_ISF]',  
        '[AB42_O2_ISF]', '[AB42_O3_ISF]', '[AB42_O4_ISF]', '[AB42_O5_ISF]', '[AB42_O6_ISF]', '[AB42_O7_ISF]', 
        '[AB42_O8_ISF]', '[AB42_O9_ISF]', '[AB42_O10_ISF]', '[AB42_O11_ISF]', '[AB42_O12_ISF]', '[AB42_O13_ISF]',
        '[AB42_O14_ISF]', '[AB42_O15_ISF]', '[AB42_O16_ISF]', '[AB42_O17_ISF]', '[AB42_O18_ISF]', '[AB42_O19_ISF]',
        '[AB42_O20_ISF]', '[AB42_O21_ISF]', '[AB42_O22_ISF]', '[AB42_O23_ISF]', '[AB42_O24_ISF]'])
    print(r['[AB42_O1_ISF]'],r['[AB42_O25_ISF]'])

    return r, result1,result2, csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, csv_data_3A_nonApoE, suvr



def create_plots(r, result1, result2, csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, csv_data_3A_nonApoE, suvr):
    """
    Create plots using the simulation results.
    """
    # Create the figure with 6 subplots in 3x2 grid
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('Geerts Model Simulation Results', fontsize=16)

    # Get time in years
    time_years1 = result1['time']/24/365
    time_years2 = result2['time']/24/365
    # Plot 1: Oligomers
    ax1 = axes[0, 0]
    oligomer_sum1 = result1['[AB42_O2_ISF]']
    for i in range(3, 18):
        oligomer_sum1 += result1[f'[AB42_O{i}_ISF]']
    ax1.plot(time_years1, oligomer_sum1, label='Oligomers ApoE', linewidth=2,linestyle='--',color='red')

    oligomer_weighted_sum1 = result1['[AB42_O2_ISF]'] * 1
    for i in range(3, 18):
        oligomer_weighted_sum1 += result1[f'[AB42_O{i}_ISF]'] * (i-1)

    oligomer_sum2 = result2['[AB42_O2_ISF]']
    for i in range(3, 18):
        oligomer_sum2 += result2[f'[AB42_O{i}_ISF]']
    ax1.plot(time_years2, oligomer_sum2, label='Oligomers non-ApoE', linewidth=2,linestyle='--',color='blue')

    oligomer_weighted_sum2 = result2['[AB42_O2_ISF]'] * 1
    for i in range(3, 18):
        oligomer_weighted_sum2 += result2[f'[AB42_O{i}_ISF]'] * (i-1)
    ax1.plot(time_years1, oligomer_weighted_sum1, label='Oligomers weighted ApoE', linewidth=2,color='red')
    ax1.plot(time_years2, oligomer_weighted_sum2, label='Oligomers weighted non-ApoE', linewidth=2,color='blue')
    ax1.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax1.axvline(x=74, color='black', linestyle='--', linewidth=1.5)
    ax1.plot([70], [12211], 'o', color='green', markersize=6)
    ax1.plot([74], [12307], 'o', color='green', markersize=6)
    ax1.set_xlabel('Time (years)')
    ax1.set_ylabel('Concentration')
    ax1.set_title('Oligomers')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Plot 2: Proto
    ax2 = axes[0, 1]
    proto_sum1 = result1['[AB42_O18_ISF]']
    for i in range(19, 25):
        proto_sum1 += result1[f'[AB42_O{i}_ISF]']
    ax2.plot(time_years1, proto_sum1, label='Proto ApoE', linewidth=2,linestyle='--',color='red')

    proto_weighted_sum1 = result1['[AB42_O18_ISF]'] * 17
    for i in range(19, 25):
        proto_weighted_sum1 += result1[f'[AB42_O{i}_ISF]'] * (i-1)
    ax2.plot(time_years1, proto_weighted_sum1, label='Proto weighted ApoE', linewidth=2,color='red')

    proto_sum2 = result2['[AB42_O18_ISF]']
    for i in range(19, 25):
        proto_sum2 += result2[f'[AB42_O{i}_ISF]']
    ax2.plot(time_years2, proto_sum2, label='Proto non-ApoE', linewidth=2,linestyle='--',color='blue')

    proto_weighted_sum2 = result2['[AB42_O18_ISF]'] * 17
    for i in range(19, 25):
        proto_weighted_sum2 += result2[f'[AB42_O{i}_ISF]'] * (i-1)
    ax2.plot(time_years2, proto_weighted_sum2, label='Proto weighted non-ApoE', linewidth=2,color='blue')

    ax2.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax2.axvline(x=74, color='black', linestyle='--', linewidth=1.5)
    ax2.plot([70], [70000], 'o', color='green', markersize=6)
    ax2.plot([74], [70168], 'o', color='green', markersize=6)
    ax2.set_xlabel('Time (years)')
    ax2.set_ylabel('Concentration')
    ax2.set_title('Proto')
    ax2.legend(loc='upper left', fontsize=7)
    ax2.grid(True)

    # Plot 3: SUVR
    ax3 = axes[1, 0]
    plaque_sum1 = result1['[AB42_O25_ISF]']
    suvr_values1 = suvr(oligomer_weighted_sum1, proto_weighted_sum1, plaque_sum1)
    ax3.plot(time_years1, suvr_values1, label='SUVR ApoE', linewidth=2,color='red')

    plaque_sum2 = result2['[AB42_O25_ISF]']
    suvr_values2 = suvr(oligomer_weighted_sum2, proto_weighted_sum2, plaque_sum2)
    ax3.plot(time_years2, suvr_values2, label='SUVR non-ApoE', linewidth=2,color='blue')

    ax3.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax3.axvline(x=74, color='black', linestyle='--', linewidth=1.5)
    ax3.plot([70], [1.394], 'o', color='green', markersize=6)
    ax3.plot([74], [1.623], 'o', color='green', markersize=6)
    ax3.plot(csv_data_3A_ApoE['time']/24/365, csv_data_3A_ApoE['measurement'], 'r.', label='ApoE published', markersize=4)
    ax3.plot(csv_data_3A_nonApoE['time']/24/365, csv_data_3A_nonApoE['measurement'], 'b.', label='non-ApoE published', markersize=4)
    ax3.set_xlabel('Time (years)')
    ax3.set_ylabel('Concentration')
    ax3.set_title('SUVR')
    ax3.legend(loc='upper left')
    ax3.grid(True)

    # Plot 4: AB42_O1_ISF and AB42_O25_ISF
    ax4 = axes[1, 1]
    ax4.plot(time_years1, result1['[AB42_O1_ISF]'], label='AB42_O1_ISF ApoE', linewidth=2,color='red')
    ax4.plot(time_years2, result2['[AB42_O1_ISF]'], label='AB42_O1_ISF non-ApoE', linewidth=2,color='blue')
    ax4.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax4.plot(csv_data_3C_ApoE['time']/24/365, csv_data_3C_ApoE['measurement'], 'r.', label='ApoE published', markersize=4)
    ax4.plot(csv_data_3C_nonApoE['time']/24/365, csv_data_3C_nonApoE['measurement'], 'b.', label='non-ApoE published', markersize=4)
    ax4.set_xlabel('Time (years)')
    ax4.set_ylabel('Concentration')
    ax4.set_title('AB42_O1_ISF and AB42_O1_CSF')
    ax4.legend(loc='upper right')
    ax4.grid(True)

    # # Plot 5: IDE_activity_ISF
    # ax5 = axes[2, 0]
    # ax5.plot(time_years1, result1['[IDE_activity_ISF]'], label='IDE_activity_ISF ApoE', linewidth=2,color='red')
    # ax5.plot(time_years2, result2['[IDE_activity_ISF]'], label='IDE_activity_ISF non-ApoE', linewidth=2,color='blue')
    # ax5.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    # # ax5.plot([70], [1.3], 'o', color='blue', markersize=14)
    # ax5.set_xlabel('Time (years)')
    # ax5.set_ylabel('Concentration')
    # ax5.set_title('IDE_activity_ISF')
    # ax5.legend(loc='upper right')
    # ax5.grid(True)

    # Plot 6: AB40_O1_central
    ax6 = axes[2, 1]
    ax6.plot(time_years1, result1['[AB42_O25_ISF]'], label='AB42_O25_ISF ApoE', linewidth=2,color='red')
    ax6.plot(time_years2, result2['[AB42_O25_ISF]'], label='AB42_O25_ISF non-ApoE', linewidth=2,color='blue')
    ax6.axvline(x=70, color='black', linestyle='--', linewidth=1.5)
    ax6.axvline(x=74, color='black', linestyle='--', linewidth=1.5)
    ax6.plot([70], [5102], 'o', color='green', markersize=6)
    ax6.plot([74], [6028], 'o', color='green', markersize=6)
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
    r, result1,result2, csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, csv_data_3A_nonApoE, suvr = run_optimization_and_simulation()
    
    # Calculate SUVR at 70 years and store interpolated values
    print("\n" + "="*50)
    print("CALCULATING SUVR AT 70 YEARS")
    print("="*50)
    suvr_70_results = calculate_suvr_at_year(result1, suvr, 70)
    
    # Store the results for further use
    interpolated_values = suvr_70_results['interpolated_values']
    oligomer_weighted_sum_70 = suvr_70_results['oligomer_weighted_sum']
    proto_weighted_sum_70 = suvr_70_results['proto_weighted_sum']
    plaque_sum_70 = suvr_70_results['plaque_sum']
    suvr_at_70 = suvr_70_results['suvr_at_year']
    
    print(f"\nFinal SUVR at 70 years: {suvr_at_70:.6f}")
    print("="*50)
    
    # Create plots
    create_plots(r, result1,result2, csv_data_3C_ApoE,csv_data_3C_nonApoE, csv_data_3A_ApoE, csv_data_3A_nonApoE, suvr) 
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import os

def read_matlab_file(filename):
    """
    Read a MATLAB .mat file and return its contents.
    
    Parameters:
    filename (str): Path to the .mat file
    
    Returns:
    dict: Dictionary containing all variables from the .mat file
    """
    try:
        # Load the MATLAB file
        mat_contents = scipy.io.loadmat(filename)
        
        print(f"Successfully loaded {filename}")
        print(f"Number of variables in the file: {len(mat_contents)}")
        
        # Print information about each variable
        print("\nVariables in the file:")
        print("-" * 50)
        for key, value in mat_contents.items():
            # Skip MATLAB's internal variables that start with '__'
            if not key.startswith('__'):
                if isinstance(value, np.ndarray):
                    print(f"{key}: {type(value).__name__} with shape {value.shape}")
                    if value.size <= 10:  # Show small arrays
                        print(f"  Values: {value}")
                else:
                    print(f"{key}: {type(value).__name__}")
        
        return mat_contents
        
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None

def analyze_matlab_data(mat_contents):
    """
    Analyze the contents of the MATLAB file and provide detailed information.
    
    Parameters:
    mat_contents (dict): Dictionary containing MATLAB variables
    """
    if mat_contents is None:
        return
    
    print("\n" + "="*60)
    print("DETAILED ANALYSIS")
    print("="*60)
    
    for key, value in mat_contents.items():
        if key.startswith('__'):  # Skip MATLAB internal variables
            continue
            
        print(f"\nVariable: {key}")
        print("-" * 30)
        
        if isinstance(value, np.ndarray):
            print(f"Type: numpy.ndarray")
            print(f"Shape: {value.shape}")
            print(f"Data type: {value.dtype}")
            print(f"Size: {value.size}")
            
            if value.size > 0:
                if value.ndim == 1:
                    print(f"Min value: {np.min(value)}")
                    print(f"Max value: {np.max(value)}")
                    print(f"Mean value: {np.mean(value)}")
                    if value.size <= 20:
                        print(f"All values: {value}")
                elif value.ndim == 2:
                    print(f"Min value: {np.min(value)}")
                    print(f"Max value: {np.max(value)}")
                    print(f"Mean value: {np.mean(value)}")
                    if value.shape[0] <= 5 and value.shape[1] <= 10:
                        print(f"First few rows:\n{value}")
                else:
                    print(f"Multi-dimensional array")
                    print(f"Min value: {np.min(value)}")
                    print(f"Max value: {np.max(value)}")
                    print(f"Mean value: {np.mean(value)}")
        else:
            print(f"Type: {type(value)}")
            print(f"Value: {value}")

def plot_data_if_appropriate(mat_contents):
    """
    Create plots for numerical data if appropriate.
    
    Parameters:
    mat_contents (dict): Dictionary containing MATLAB variables
    """
    if mat_contents is None:
        return
    
    print("\n" + "="*60)
    print("CREATING PLOTS")
    print("="*60)
    
    # Find numerical arrays that might be suitable for plotting
    plotable_vars = []
    for key, value in mat_contents.items():
        if key.startswith('__'):
            continue
        if isinstance(value, np.ndarray) and value.ndim <= 2 and value.size > 1:
            plotable_vars.append((key, value))
    
    if not plotable_vars:
        print("No suitable variables found for plotting.")
        return
    
    print(f"Found {len(plotable_vars)} variables that can be plotted.")
    
    # Create plots for each suitable variable
    for i, (key, value) in enumerate(plotable_vars):
        plt.figure(figsize=(10, 6))
        
        if value.ndim == 1:
            plt.plot(value)
            plt.title(f'{key} (1D array)')
            plt.xlabel('Index')
            plt.ylabel('Value')
        elif value.ndim == 2:
            if value.shape[0] == 1 or value.shape[1] == 1:
                # 1D array stored as 2D
                plt.plot(value.flatten())
                plt.title(f'{key} (flattened 2D array)')
                plt.xlabel('Index')
                plt.ylabel('Value')
            else:
                # 2D array - show as heatmap
                plt.imshow(value, aspect='auto', cmap='viridis')
                plt.colorbar()
                plt.title(f'{key} (2D array)')
                plt.xlabel('Column')
                plt.ylabel('Row')
        
        plt.tight_layout()
        plt.savefig(f'plot_{key}.png', dpi=150, bbox_inches='tight')
        print(f"Saved plot for {key} as plot_{key}.png")
        plt.close()

def main():
    """
    Main function to read and analyze the MATLAB file.
    """
    filename = 'FullPBPKSim_Human.mat'
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found in current directory.")
        print("Please make sure the file is in the same directory as this script.")
        return
    
    print(f"Reading MATLAB file: {filename}")
    print("="*60)
    
    # Read the MATLAB file
    mat_contents = read_matlab_file(filename)
    
    # Analyze the data
    analyze_matlab_data(mat_contents)
    
    # Create plots if appropriate
    plot_data_if_appropriate(mat_contents)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("The MATLAB file has been successfully read and analyzed.")
    print("Check the generated plot files for visualizations of the data.")

if __name__ == "__main__":
    main()

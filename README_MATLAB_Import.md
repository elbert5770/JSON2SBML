# MATLAB File Importer for Julia

This repository contains Julia code to import and analyze MATLAB `.mat` files.

## Files

- `Read_mat_file.jl` - Main program to import MATLAB files
- `setup_and_run.jl` - Setup script to install dependencies and run the importer
- `README_MATLAB_Import.md` - This documentation file

## Requirements

- Julia 1.6 or later
- Required Julia packages:
  - `MAT.jl` - For reading MATLAB files
  - `DataFrames.jl` - For data manipulation
  - `Printf.jl` - For formatted output

## Usage

### Option 1: Run the setup script (Recommended)
```bash
julia setup_and_run.jl
```

### Option 2: Manual setup and run
```julia
# In Julia REPL or script
using Pkg
Pkg.add("MAT")
Pkg.add("DataFrames")
Pkg.add("Printf")

# Then run the main script
include("Read_mat_file.jl")
```

### Option 3: Use as a module
```julia
include("Read_mat_file.jl")

# Import a specific MATLAB file
data = import_matlab_file("your_file.mat")

# Explore a specific variable
explore_variable(data, "variable_name")
```

## Features

The program provides:

1. **Automatic file detection** - Looks for `FullPBPKSim_Human.mat` in the current directory
2. **Comprehensive file analysis** - Shows all variables, their types, and sizes
3. **Error handling** - Graceful handling of file reading errors
4. **Variable exploration** - Detailed analysis of specific variables
5. **Flexible output** - Returns data for further processing

## Output

The program will display:
- List of all variables in the MATLAB file
- Type and size of each variable
- Sample values for arrays
- Total number of variables found

## Example Output

```
Julia MATLAB File Importer
=========================
Importing MATLAB file: FullPBPKSim_Human.mat

File contents:
==============
Variable: time
  Type: Array{Float64,1}
  Size: (1000,)
  Values: [showing first 10 elements] [0.0, 0.1, 0.2, ...]

Variable: concentration
  Type: Array{Float64,2}
  Size: (1000, 5)
  Values: [showing first 10 elements] [1.0, 0.95, 0.9, ...]

Import successful!
Total variables found: 15
```

## Customization

To explore specific variables, uncomment and modify the line in the `main()` function:

```julia
# explore_variable(mat_data, "your_variable_name")
```

## Troubleshooting

1. **File not found**: Ensure `FullPBPKSim_Human.mat` is in the current directory
2. **Package errors**: Run the setup script to install required packages
3. **Memory issues**: For large files, consider processing variables individually

## License

This code is provided as-is for educational and research purposes. 
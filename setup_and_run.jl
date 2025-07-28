# Setup script for MATLAB file importer
# This script installs required packages and runs the importer

println("Setting up Julia environment for MATLAB file import...")

# Add packages to the current environment
using Pkg

# Add required packages
println("Installing required packages...")
Pkg.add("MAT")
Pkg.add("DataFrames")
Pkg.add("Printf")

println("Packages installed successfully!")
println("Now running the MATLAB file importer...")

# Include and run the main script
include("Read_mat_file.jl") 
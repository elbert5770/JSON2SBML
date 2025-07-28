using MAT
using DataFrames
using Printf

# Function to import MATLAB file
function import_matlab_file(filename::String)
    println("Importing MATLAB file: $filename")
    
    try
        # Read the MATLAB file
        mat_data = matread(filename)
        
        # Print information about the file contents
        println("\nFile contents:")
        println("==============")
        
        for (key, value) in mat_data
            println("Variable: $key")
            if typeof(value) <: AbstractArray
                println("  Type: $(typeof(value))")
                println("  Size: $(size(value))")
                if length(value) <= 10
                    println("  Values: $value")
                else
                    println("  Values: [showing first 10 elements] $(value[1:min(10, length(value))])")
                end
            else
                println("  Type: $(typeof(value))")
                println("  Value: $value")
            end
            println()
        end
        
        return mat_data
        
    catch e
        println("Error reading MATLAB file: $e")
        return nothing
    end
end

# Function to explore specific variables in more detail
function explore_variable(data::Dict, var_name::String)
    if haskey(data, var_name)
        value = data[var_name]
        println("Detailed information for variable: $var_name")
        println("==========================================")
        println("Type: $(typeof(value))")
        println("Size: $(size(value))")
        
        if typeof(value) <: AbstractArray
            if length(value) <= 20
                println("All values: $value")
            else
                println("First 10 values: $(value[1:min(10, length(value))])")
                println("Last 10 values: $(value[end-min(9, length(value)-1):end])")
            end
        else
            println("Value: $value")
        end
    else
        println("Variable '$var_name' not found in the MATLAB file.")
        println("Available variables: $(keys(data))")
    end
end

# Main execution
function main()
    filename = "FullPBPKSim_Human.mat"
    
    println("Julia MATLAB File Importer")
    println("=========================")
    
    # Import the MATLAB file
    mat_data = import_matlab_file(filename)
    
    if mat_data !== nothing
        println("\nImport successful!")
        println("Total variables found: $(length(mat_data))")
        
        # Example: Explore a specific variable (uncomment and modify as needed)
        # explore_variable(mat_data, "variable_name")
        
        # Return the data for further use
        return mat_data
    else
        println("Failed to import MATLAB file.")
        return nothing
    end
end


main()


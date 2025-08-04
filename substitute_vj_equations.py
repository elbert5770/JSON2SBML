import re

def substitute_vj_equations(filename):
    """
    Read a file containing v_J* definitions and differential equations,
    then substitute the v_J* expressions into the differential equations.
    
    Args:
        filename (str): Path to the input file
        
    Returns:
        tuple: (vj_definitions, substituted_equations)
    """
    # Dictionary to store v_J* definitions
    vj_definitions = {}
    
    # List to store differential equations
    diff_equations = []
    
    # Read the file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Process each line
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line starts with v_J* (using regex to match v_J followed by numbers)
        if re.match(r'^v_J\d+\s*=', line):
            # Extract v_J* name and its expression
            parts = line.split('=', 1)
            if len(parts) == 2:
                vj_name = parts[0].strip()
                expression = parts[1].strip()
                vj_definitions[vj_name] = expression
        
        # Check if line is a differential equation (starts with 'd' and contains '/dt')
        elif line.startswith('d') and '/dt' in line:
            diff_equations.append(line)
    
    # Substitute v_J* expressions into differential equations
    substituted_equations = []
    
    for equation in diff_equations:
        substituted_equation = equation
        
        # Replace each v_J* with its expression
        for vj_name, expression in vj_definitions.items():
            # Use word boundaries to ensure we replace the exact v_J* name
            pattern = r'\b' + re.escape(vj_name) + r'\b'
            substituted_equation = re.sub(pattern, f"({expression})", substituted_equation)
        
        substituted_equations.append(substituted_equation)
    
    return vj_definitions, substituted_equations

def write_output_to_file(vj_definitions, substituted_equations, output_filename):
    """
    Write the v_J* definitions and substituted equations to a text file.
    
    Args:
        vj_definitions (dict): Dictionary of v_J* definitions
        substituted_equations (list): List of substituted differential equations
        output_filename (str): Name of the output file
    """
    with open(output_filename, 'w') as file:
        file.write("V_J* DEFINITIONS:\n")
        file.write("=" * 80 + "\n")
        
        for vj_name, expression in vj_definitions.items():
            file.write(f"{vj_name} = {expression}\n")
        
        file.write(f"\nFound {len(vj_definitions)} v_J* definitions\n")
        file.write(f"Found {len(substituted_equations)} differential equations\n")
        
        file.write("\n" + "=" * 80 + "\n")
        file.write("SUBSTITUTED DIFFERENTIAL EQUATIONS:\n")
        file.write("=" * 80 + "\n")
        
        for i, equation in enumerate(substituted_equations, 1):
            file.write(f"{i:2d}. {equation}\n")

def main():
    """Main function to run the substitution"""
    input_filename = "Bloomingdale_diffEQ.txt"
    output_filename = "substituted_equations.txt"
    
    try:
        vj_definitions, substituted_equations = substitute_vj_equations(input_filename)
        
        write_output_to_file(vj_definitions, substituted_equations, output_filename)
        
        print(f"Processing complete!")
        print(f"Found {len(vj_definitions)} v_J* definitions")
        print(f"Found {len(substituted_equations)} differential equations")
        print(f"Output written to: {output_filename}")
            
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 
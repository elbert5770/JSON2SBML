import json
import itertools
import re

def extract_species_and_parameters_from_reactions(reaction_string):
    """
    Extract unique species and parameters from reaction string (excluding compartment declarations).
    
    Args:
        reaction_string (str): The reaction string to analyze
        
    Returns:
        tuple: (species_list, parameters_list)
    """
    # Sets to store unique species and parameters
    species = set()
    parameters = set()
    
    # Split into lines and process each line
    lines = reaction_string.split('\n')
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        
        # Skip compartment declarations
        if line.startswith('compartment '):
            continue
                
        # Split at semicolon
        parts = line.split(';')
        if len(parts) != 2:
            continue
                
        # Extract species from left side
        left_side = parts[0].strip()
        # Split by + and -> to get individual species
        species_parts = re.split(r'[+\->]+', left_side)
        for part in species_parts:
            part = part.strip()
            # Remove leading digits and whitespace (e.g., '2 AB40_O12_ISF' -> 'AB40_O12_ISF')
            part = re.sub(r'^\d+\s*', '', part)
            # Skip empty strings and pure numbers
            if part and not part.isdigit():
                # Only add if it contains at least one letter (to avoid lone numbers)
                if re.search(r'[A-Za-z]', part):
                    species.add(part)
            
        # Extract parameters from right side
        right_side = parts[1].strip()
        # Find all words that look like parameters (containing letters, numbers, and underscores)
        param_matches = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', right_side)
        parameters.update(param_matches)
    
    # Remove species from parameters
    parameters = parameters - species
    
    # Clean up species list - remove any that look like parameters
    species = {s for s in species if not re.match(r'^[a-z]', s)}
    
    return sorted(list(species)), sorted(list(parameters))

def write_list_to_file(items, filename):
    """Write a list of items to a file, one per line."""
    with open(filename, 'w') as f:
        for item in items:
            f.write(f"{item}\n")

def generate_species_declarations(species_list):
    """
    Generate species declarations in the format 'species species_X in compartment X'
    where X is the text after the final '_' in the species name.
    
    Args:
        species_list (list): List of species names
        
    Returns:
        str: Formatted species declarations
    """
    declarations = []
    for species in species_list:
        # Find the last underscore and get the compartment
        if '_' in species:
            compartment = species.split('_')[-1]
            declarations.append(f"substanceOnly species {species} in {compartment}")
        else:
            # If no underscore, use the species name as compartment
            declarations.append(f"substanceOnly species {species} in {species}")
    
    return '\n'.join(declarations)

def clean_json_content(content):
    """
    Remove comments from JSON content to make it valid JSON.
    
    Args:
        content (str): JSON content with comments
        
    Returns:
        str: Cleaned JSON content
    """
    # Remove single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    
    # Remove empty lines
    content = re.sub(r'^\s*$\n', '', content, flags=re.MULTILINE)
    
    return content

def collect_unique_compartments(json_file_path):
    """
    Reads a JSON file with reaction templates and collects all unique compartment names.
    
    Args:
        json_file_path (str): The path to the JSON file.
        
    Returns:
        set: A set containing all unique compartment names.
    """
    with open(json_file_path, 'r') as f:
        content = f.read()
    
    # Clean the JSON content
    cleaned_content = clean_json_content(content)
    
    # Parse the cleaned JSON
    reaction_templates = json.loads(cleaned_content)
    
    unique_compartments = set()
    
    for template in reaction_templates:
        # Handle Comp key
        comp_str = template.get("Comp", "[]")
        if comp_str.startswith('[') and comp_str.endswith(']'):
            comp_cleaned = comp_str.strip('[]')
            if comp_cleaned:
                compartments = [item.strip() for item in comp_cleaned.split(',')]
                unique_compartments.update(compartments)
        else:
            unique_compartments.add(comp_str)
    
    return unique_compartments

def generate_antimony_script(json_file_path):
    """
    Reads a JSON file with reaction templates and generates an Antimony script.
    Handles the new schema with compartments and new rate types.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        str: A string containing the generated Antimony reactions.
    """
    with open(json_file_path, 'r') as f:
        content = f.read()
    
    # Clean the JSON content
    cleaned_content = clean_json_content(content)
    
    # Parse the cleaned JSON
    reaction_templates = json.loads(cleaned_content)

    # Collect all unique compartments first
    unique_compartments = set()
    for template in reaction_templates:
        comp_str = template.get("Comp", "[]")
        if comp_str.startswith('[') and comp_str.endswith(']'):
            comp_cleaned = comp_str.strip('[]')
            if comp_cleaned:
                compartments = [item.strip() for item in comp_cleaned.split(',')]
                unique_compartments.update(compartments)
        else:
            unique_compartments.add(comp_str)
    
    # Start with empty reaction string (compartments will be added separately)
    reaction_string = ""

    for template in reaction_templates:
        # Validate required keys
        required_keys = {"Reactants", "Products", "Rate_type", "Rate_eqtn_prototype", "Comp"}
        missing_keys = required_keys - set(template.keys())
        if missing_keys:
            raise ValueError(f"Reaction '{template.get('Reaction_name', 'UNKNOWN')}' is missing required keys: {missing_keys}")
        
        # Validate rate type
        rate_type = template["Rate_type"]
        valid_rate_types = {"MA", "RMA", "UDF", "BDF", "custom_conc_per_time", "custom_amt_per_time"}
        if rate_type not in valid_rate_types:
            raise ValueError(f"Reaction '{template.get('Reaction_name', 'UNKNOWN')}' has invalid Rate_type: '{rate_type}'. Valid types are: {valid_rate_types}")
        
        known_keys = {"Reaction_name", "Reactants", "Products", "Rate_type", "Rate_eqtn_prototype", "Comp", "Paired"}
        variable_keys = [k for k in template.keys() if k not in known_keys]

        variables = {}
        for key in variable_keys:
            value_str = template[key]
            if ' for ' in value_str and 'in range' in value_str:
                # Handle list comprehensions
                variables[key] = eval(value_str)
            else:
                # Handle simple lists of strings like "[ISF]" or "[AB40,AB42]"
                cleaned_str = value_str.strip('[]')
                if cleaned_str:
                    variables[key] = [item.strip() for item in cleaned_str.split(',')]
                else:
                    variables[key] = []
        
        # Handle Comp key
        comp_str = template.get("Comp", "[]")
        if comp_str.startswith('[') and comp_str.endswith(']'):
            comp_cleaned = comp_str.strip('[]')
            if comp_cleaned:
                variables["Comp"] = [item.strip() for item in comp_cleaned.split(',')]
            else:
                variables["Comp"] = []
        else:
            variables["Comp"] = [comp_str]
        
        paired_keys = set()
        if "Paired" in template:
            paired_keys = set(template["Paired"].strip('{}').split(','))
        
        unpaired_keys = [k for k in variable_keys if k not in paired_keys]
        
        iterators = []
        if unpaired_keys:
            iterators.extend([variables[k] for k in unpaired_keys])
        
        sorted_paired_keys = sorted(list(paired_keys))
        if sorted_paired_keys:
            iterators.append(zip(*[variables[k] for k in sorted_paired_keys]))

        for combination in itertools.product(*iterators):
            context = {}
            combo_idx = 0
            for key in unpaired_keys:
                context[key] = combination[combo_idx]
                combo_idx += 1
            
            if sorted_paired_keys:
                pair_tuple = combination[combo_idx]
                for i, key in enumerate(sorted_paired_keys):
                    context[key] = pair_tuple[i]

            # Handle compartment substitutions
            comp_values = variables["Comp"]
            
            # For each compartment combination, generate reactions
            if len(comp_values) == 1:
                # Single compartment - replace {Comp} with the compartment name
                comp_context = context.copy()
                comp_context["Comp"] = comp_values[0]
                
                # Handle Comp1 and Comp2 for single compartment (they're the same)
                comp_context["Comp1"] = comp_values[0]
                comp_context["Comp2"] = comp_values[0]
                
                reaction_string += generate_single_reaction(template, comp_context)
                
            elif len(comp_values) == 2:
                # Two compartments - replace {Comp1} and {Comp2} with the respective compartments
                comp_context = context.copy()
                comp_context["Comp1"] = comp_values[0]
                comp_context["Comp2"] = comp_values[1]
                
                # Also handle {Comp} - use the first compartment for single compartment references
                comp_context["Comp"] = comp_values[0]
                
                reaction_string += generate_single_reaction(template, comp_context)
                
            else:
                # Multiple compartments - generate reactions for each pair
                for i in range(len(comp_values) - 1):
                    comp_context = context.copy()
                    comp_context["Comp1"] = comp_values[i]
                    comp_context["Comp2"] = comp_values[i + 1]
                    comp_context["Comp"] = comp_values[i]
                    
                    reaction_string += generate_single_reaction(template, comp_context)
            
    return reaction_string

def generate_single_reaction(template, context):
    """
    Generate a single reaction string for the given template and context.
    
    Args:
        template (dict): The reaction template
        context (dict): The substitution context
        
    Returns:
        str: The generated reaction string
    """
    # Perform substitutions
    reactants_str = template["Reactants"].format(**context)
    products_str = template["Products"].format(**context)
    rate_proto_str = template["Rate_eqtn_prototype"].format(**context)
    
    if reactants_str == "0" or reactants_str == "[0]":
        reactants = []
    else:
        reactants_str = reactants_str.strip('[]')
        if reactants_str:
            reactants = [item.strip() for item in reactants_str.split(',')]
        else:
            reactants = []

    if products_str == "0" or products_str == "[0]":
        products = []
    else:
        # Products can be a single item or a list
        prod_cleaned = products_str.strip('[]')
        if prod_cleaned:
            products = [item.strip() for item in prod_cleaned.split(',')]
        else:
            products = []

    rate_type = template["Rate_type"]
    reaction_string = ""

    if rate_type == "RMA":
        # RMA (reversible mass action) needs two rate constants
        rate_constants = [item.strip() for item in rate_proto_str.strip('[]').split(',')]
        if len(rate_constants) < 2:
            raise ValueError(f"RMA reaction '{template.get('Reaction_name', 'UNKNOWN')}' requires two rate constants in Rate_eqtn_prototype, got: '{template['Rate_eqtn_prototype']}'")
        # Forward
        reactants_fwd_str = " + ".join(reactants)
        products_fwd_str = " + ".join(products)
        if reactants:
            rate_fwd = f"{rate_constants[0]} * {' * '.join(reactants)}"
        else:
            rate_fwd = rate_constants[0]  # Zero-order reaction
        # Multiply by compartment volume for MA/RMA/custom_conc_per_time
        rate_fwd = f"{rate_fwd} * V_{context['Comp']}"
        reaction_string += f"{reactants_fwd_str} -> {products_fwd_str}; {rate_fwd}\n"
        # Reverse
        reactants_rev_str = " + ".join(products)
        products_rev_str = " + ".join(reactants)
        if products:
            rate_rev = f"{rate_constants[1]} * {' * '.join(products)}"
        else:
            rate_rev = rate_constants[1]  # Zero-order reaction
        # Multiply by compartment volume for MA/RMA/custom_conc_per_time
        rate_rev = f"{rate_rev} * V_{context['Comp']}"
        reaction_string += f"{reactants_rev_str} -> {products_rev_str}; {rate_rev}\n"
    elif rate_type == "BDF":
        # BDF (bidirectional flow) uses the same rate constant for both directions
        rate_constants = [item.strip() for item in rate_proto_str.strip('[]').split(',')]
        if len(rate_constants) < 1:
            raise ValueError(f"BDF reaction '{template.get('Reaction_name', 'UNKNOWN')}' requires at least one rate constant in Rate_eqtn_prototype, got: '{template['Rate_eqtn_prototype']}'")
        # Forward
        reactants_fwd_str = " + ".join(reactants)
        products_fwd_str = " + ".join(products)
        if reactants:
            rate_fwd = f"{rate_constants[0]} * {' * '.join(reactants)}"
        else:
            rate_fwd = rate_constants[0]  # Zero-order reaction
        reaction_string += f"{reactants_fwd_str} -> {products_fwd_str}; {rate_fwd}\n"
        # Reverse (same rate constant)
        reactants_rev_str = " + ".join(products)
        products_rev_str = " + ".join(reactants)
        if products:
            rate_rev = f"{rate_constants[0]} * {' * '.join(products)}"
        else:
            rate_rev = rate_constants[0]  # Zero-order reaction
        reaction_string += f"{reactants_rev_str} -> {products_rev_str}; {rate_rev}\n"
    elif rate_type == "MA" or rate_type == "UDF":
        # UDF is treated the same as MA (unidirectional flow)
        rate_constants = [item.strip() for item in rate_proto_str.strip('[]').split(',')]
        # Forward
        reactants_fwd_str = " + ".join(reactants)
        products_fwd_str = " + ".join(products)
        if reactants:
            rate_fwd = f"{rate_constants[0]} * {' * '.join(reactants)}"
        else:
            rate_fwd = rate_constants[0]  # Zero-order reaction
        # Multiply by compartment volume for MA/RMA/custom_conc_per_time
        if rate_type == "MA":
            rate_fwd = f"{rate_fwd} * V_{context['Comp']}"
        reaction_string += f"{reactants_fwd_str} -> {products_fwd_str}; {rate_fwd}\n"
        
    elif rate_type == "custom_conc_per_time":
        reactants_side = " + ".join(reactants)
        products_side = " + ".join(products) if products else ""
        
        rate_eqtn = rate_proto_str
        # if it was a list-like string, take the content.
        if rate_eqtn.startswith('[') and rate_eqtn.endswith(']'):
            rate_eqtn = rate_eqtn.strip('[]')
        
        # Multiply by compartment volume for custom_conc_per_time
        rate_eqtn = f"{rate_eqtn} * V_{context['Comp']}"
        
        reaction_string += f"{reactants_side} -> {products_side}; {rate_eqtn}\n"
        
    elif rate_type == "custom_amt_per_time":
        reactants_side = " + ".join(reactants)
        products_side = " + ".join(products) if products else ""
        
        rate_eqtn = rate_proto_str
        # if it was a list-like string, take the content.
        if rate_eqtn.startswith('[') and rate_eqtn.endswith(']'):
            rate_eqtn = rate_eqtn.strip('[]')
        
        # No multiplication for custom_amt_per_time
        
        reaction_string += f"{reactants_side} -> {products_side}; {rate_eqtn}\n"
    
    return reaction_string

def convert_species_to_concentrations(reaction_string, species_list):
    """
    Convert species in rate equations from amounts to concentrations by dividing by compartment volumes.
    This is needed for MTK solver where species names refer to amounts but rate equations need concentrations.
    
    Args:
        reaction_string (str): The reaction string with species as amounts
        species_list (list): List of species names
        
    Returns:
        str: Modified reaction string with species converted to concentrations in rate equations
    """
    # Create a mapping of species to their compartments
    species_to_compartment = {}
    for species in species_list:
        if '_' in species:
            compartment = species.split('_')[-1]
            species_to_compartment[species] = compartment
        else:
            # If no underscore, use the species name as compartment
            species_to_compartment[species] = species
    
    # Process each line
    lines = reaction_string.split('\n')
    modified_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            modified_lines.append(line)
            continue
        
        # Skip compartment declarations
        if line.startswith('compartment '):
            modified_lines.append(line)
            continue
        
        # Split at semicolon to separate reactants/products from rate
        parts = line.split(';')
        if len(parts) != 2:
            modified_lines.append(line)
            continue
        
        reactants_products = parts[0].strip()
        rate_equation = parts[1].strip()
        
        # Modify the rate equation to convert species to concentrations
        modified_rate = rate_equation
        
        # Find all species in the rate equation and replace them with species/V_compartment
        for species in species_list:
            if species in modified_rate:
                compartment = species_to_compartment[species]
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(species) + r'\b'
                replacement = f"({species}/V_{compartment})"
                modified_rate = re.sub(pattern, replacement, modified_rate)
        
        # Reconstruct the line
        modified_line = f"{reactants_products}; {modified_rate}"
        modified_lines.append(modified_line)
    
    return '\n'.join(modified_lines)

if __name__ == "__main__":
    # Collect unique compartments
    unique_compartments = collect_unique_compartments("Geerts_reactions_microglia.json")
    
    # Write unique compartments to file
    with open("unique_compartments.txt", "w") as f:
        for compartment in sorted(unique_compartments):
            f.write(f"{compartment}\n")
    
    print(f"Found {len(unique_compartments)} unique compartments:")
    for compartment in sorted(unique_compartments):
        print(f"  - {compartment}")
    print(f"Unique compartments written to 'unique_compartments.txt'")
    print()
    
    # Generate Antimony script (reactions only, without compartments)
    reactions_only = generate_antimony_script("Geerts_reactions_microglia.json")
    
    # Extract species and parameters from reactions
    species, parameters = extract_species_and_parameters_from_reactions(reactions_only)
    
    # Write species and parameters to files
    write_list_to_file(species, 'unique_species.txt')
    write_list_to_file(parameters, 'unique_parameters.txt')
    
    print(f"Found {len(species)} unique species and {len(parameters)} unique parameters")
    print(f"Species written to 'unique_species.txt'")
    print(f"Parameters written to 'unique_parameters.txt'")
    print()
    
    # Convert species in rate equations to concentrations for MTK solver
    reactions_mtk = convert_species_to_concentrations(reactions_only, species)
    
    # Generate the complete script with compartments, species, and reactions
    complete_script = ""
    
    # Add compartment declarations
    for compartment in sorted(unique_compartments):
        complete_script += f"compartment {compartment} = V_{compartment}\n"
    complete_script += "\n"  # Add blank line after compartments
    
    # Add species declarations
    species_declarations = generate_species_declarations(species)
    complete_script += species_declarations
    complete_script += "\n\n"  # Add blank lines after species
    
    # Add reactions (MTK version with species converted to concentrations in rate equations)
    complete_script += reactions_mtk
    
    print(complete_script)
    
    # Write complete script to file
    with open("New_reactions_microglia.txt", "w") as f:
        f.write(complete_script) 
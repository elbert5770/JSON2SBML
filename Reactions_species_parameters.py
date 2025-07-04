import re

def extract_species_and_parameters(filename):
    # Sets to store unique species and parameters
    species = set()
    parameters = set()
    
    # Read the file
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
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
    with open(filename, 'w') as f:
        for item in items:
            f.write(f"{item}\n")

def main():
    filename = 'generated_reactions3.txt'
    species, parameters = extract_species_and_parameters(filename)
    
    # Write species to file
    write_list_to_file(species, 'unique_species.txt')
    print(f"Wrote {len(species)} species to unique_species.txt")
    
    # Write parameters to file
    write_list_to_file(parameters, 'unique_parameters.txt')
    print(f"Wrote {len(parameters)} parameters to unique_parameters.txt")
    
    print(f"\nTotal unique species: {len(species)}")
    print(f"Total unique parameters: {len(parameters)}")

if __name__ == "__main__":
    main() 
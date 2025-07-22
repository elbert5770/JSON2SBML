# TXT to Antimony Converter

A Python script for converting reaction dictionaries stored in text files to Antimony format, specifically designed for systems biology modeling with ModelToolKit (MTK) compatibility.

## Overview

This script reads reaction data from a text file where each line contains a Python dictionary representation of a biochemical reaction, and converts it into a complete Antimony script. The generated Antimony code is optimized for use with the ModelToolKit solver, which requires species to be defined as amounts but rate equations to use concentrations.

## Features

- **Multi-format reaction support**: Handles various reaction types including:
  - **RMA** (Reversible Mass Action): Requires two rate constants for forward and reverse reactions
  - **BDF** (Bidirectional Flow): Uses the same rate constant for both directions
  - **MA** (Mass Action): Unidirectional mass action kinetics
  - **UDF** (Unidirectional Flow): Treated the same as MA
  - **custom_conc_per_time**: Custom rate equations with concentration units
  - **custom_amt_per_time**: Custom rate equations with amount units
  - **custom**: Custom rate equations used as-is (no multiplication by species or volume)

- **Automatic compartment detection**: Extracts compartment information from species names (assumes format `SpeciesName_CompartmentName`)

- **MTK compatibility**: Automatically converts species in rate equations from amounts to concentrations by dividing by compartment volumes

- **Error detection and reporting**: Identifies and reports malformed species names, compartment names, and other parsing errors

- **Comprehensive output**: Generates multiple output files for analysis and debugging

## Input Format

The script expects a text file where each line contains a Python dictionary with the following structure:

```python
{
    "Reaction_name": "string",
    "Reactants": "[reactant1, reactant2, ...]" or "[0]" for no reactants,
    "Products": "[product1, product2, ...]" or "[0]" for no products,
    "Rate_eqtn_prototype": "rate_expression" or "[rate1, rate2]" for reversible reactions,
    "Rate_type": "RMA|BDF|MA|UDF|custom_conc_per_time|custom_amt_per_time|custom"
}
```

### Example Input Line:
```python
{"Reaction_name": "AB40_aggregation", "Reactants": "[AB40_ISF]", "Products": "[AB40_O12_ISF]", "Rate_eqtn_prototype": "k_agg", "Rate_type": "MA"}
```

## Output Files

When run, the script generates several output files:

1. **`Antimony_Geerts_all_reactions.txt`**: Complete Antimony script
2. **`unique_compartments.txt`**: List of all unique compartments found
3. **`unique_species.txt`**: List of all unique species found
4. **`unique_parameters.txt`**: List of all unique parameters found
5. **`conversion_errors.log`**: Any errors encountered during conversion

## Usage

### Basic Usage
```bash
python txt_to_antimony.py
```

The script will read from `Geerts_all_reactions.txt` by default.

### Programmatic Usage
```python
from txt_to_antimony import generate_antimony_from_txt

# Generate Antimony script from a text file
complete_script, species, parameters, unique_compartments, errors = generate_antimony_from_txt("your_reactions.txt")

# Access the results
print(f"Found {len(species)} species")
print(f"Found {len(parameters)} parameters")
print(f"Found {len(unique_compartments)} compartments")
```

## Generated Antimony Format

The script generates Antimony code in the following structure:

```antimony
# Compartment declarations
compartment ISF = V_ISF
compartment CSF = V_CSF

# Species declarations
substanceOnly species AB40_ISF in ISF
substanceOnly species AB40_CSF in CSF

# Reactions (with MTK-compatible rate equations)
AB40_ISF -> AB40_O12_ISF; k_agg * (AB40_ISF/V_ISF) * V_ISF
```

## Key Functions

### `generate_antimony_from_txt(txt_file_path)`
Main function that orchestrates the entire conversion process.

### `read_reactions_from_txt(txt_file_path)`
Reads and parses reaction dictionaries from a text file.

### `generate_single_reaction_from_dict(reaction_dict)`
Converts a single reaction dictionary to Antimony format.

### `convert_species_to_concentrations(reaction_string, species_list)`
Converts species in rate equations from amounts to concentrations for MTK compatibility.

### `extract_species_and_parameters_from_reactions(reaction_string)`
Extracts unique species and parameters from reaction strings.

### `collect_unique_compartments_from_reactions(reactions)`
Identifies all unique compartments from reaction data.

## Rate Type Handling

### RMA (Reversible Mass Action)
- Requires two rate constants: `[k_forward, k_reverse]`
- Generates two separate reactions (forward and reverse)
- Automatically multiplies by compartment volume

### BDF (Bidirectional Flow)
- Uses single rate constant for both directions
- Generates two reactions with the same rate constant
- No compartment volume multiplication

### MA (Mass Action)
- Unidirectional reaction
- Automatically multiplies by compartment volume
- Supports zero-order reactions (no reactants)

### Custom Rate Types
- **custom_conc_per_time**: Multiplies by compartment volume
- **custom_amt_per_time**: No volume multiplication
- **custom**: Uses rate expression as-is, no multiplication by species or volume

## Error Handling

The script includes comprehensive error detection for:
- Malformed species names (containing brackets or quotes)
- Malformed compartment names
- Missing rate constants for reversible reactions
- Parsing errors in input file

All errors are logged to `conversion_errors.log` and displayed in the console output.

## Dependencies

- Python 3.x
- Standard library modules: `json`, `re`

## Notes

- Species names are assumed to follow the pattern `SpeciesName_CompartmentName`
- Compartment volumes are automatically added as parameters with the format `V_CompartmentName`
- The script is specifically designed for MTK solver compatibility
- Zero-order reactions (no reactants) are supported
- All rate equations are automatically converted to concentration-based for MTK compatibility

## Example Output

```
Found 5 unique compartments:
  - CSF
  - ISF
  - Plasma
  - SAS
  - Tissue

Found 15 unique species and 25 unique parameters
Species written to 'unique_species.txt'
Parameters written to 'unique_parameters.txt'

Antimony script written to 'Antimony_Geerts_all_reactions.txt'

No errors found during conversion.
``` 
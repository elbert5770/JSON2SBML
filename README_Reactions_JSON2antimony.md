# Reactions JSON to Antimony Converter

## Overview

This program converts reaction templates defined in JSON format to Antimony reaction syntax. It's designed to handle complex multi-compartment biochemical models with various reaction types and automatic parameter generation.

The general philosophy is that species should have their comparment in their name if more than one compartment exists.  The species name should also reference oligomers and isotopes if applicable.  Parameter names should reflect the reactants, products and compartments as much as possible. Mass action that results in compartment transfer is treated differently from flow and clearance reactions with units of vol/time. Initial conditions should be in amounts.

Antimony expects that the RHS provides values with units of amount/time, while species units are always concentrations.  For example, a first order reaction within a compartment should have the form: k * species * V_compartment.  Flow or clearance reactions would have the form: Q * species.  In both cases, a species referenced by its name always refers to a concentration.  The exception is if the species is defined in Antimony as substanceOnly - in that case species always have units of amounts.

If all compartment volumes have a value of 1, volumes do not need to be included in reactions.  If more than one compartment is present, the same species in different compartments must have distinct names.

See the Antimony help for additional information: 

## Features

- **Multi-compartment support**: Handles reactions across different compartments
- **Multiple reaction types**: Supports MA, RMA, UDF, BDF, and custom rate types
- **Automatic parameter generation**: Generates all combinations of parameters based on templates
- **JSON comment support**: Automatically removes comments from JSON files
- **Comprehensive validation**: Validates required fields and rate type specifications
- **Compartment volume handling**: Automatically multiplies appropriate reactions by compartment volume

## Installation

No additional dependencies beyond Python standard library:
- `json`
- `itertools` 
- `re`

## Usage

```bash
python Reactions_JSON2antimony_4.py
```

The program reads `Geerts_reactions2.json` and outputs to `generated_reactions3.txt`.

## JSON Schema

### Required Fields

Each reaction template must contain:

```json
{
  "Reaction_name": "string",
  "Reactants": "string or array of strings",
  "Products": "string or array of strings", 
  "Rate_type": "string",
  "Rate_eqtn_prototype": "string or array of strings",
  "Comp": "string or array of strings"
}
```

### Optional Fields

- `"Paired"`: Specifies which parameters should be paired together

### Variable Fields

Any field not in the known keys list is treated as a variable for parameter generation.

## Rate Types

### Valid Rate Types

1. **MA** (Mass Action): Unidirectional reaction with mass action kinetics
2. **RMA** (Reversible Mass Action): Bidirectional reaction requiring two rate constants
3. **UDF** (Unidirectional Flow): Treated same as MA
4. **BDF** (Bidirectional Flow): Bidirectional reaction using same rate constant for both directions
5. **custom_conc_per_time**: Custom rate equation (given equation yields units of concentration/time)
6. **custom_amt_per_time**: Custom rate equation (given equation yields units of amount/time)

### Compartment Volume Multiplication

- **MA**, **RMA**, **custom_conc_per_time**: Automatically multiplied by `V_{Comp}`
- **UDF**, **BDF**, **custom_amt_per_time**: No volume multiplication

## Template Syntax

### Reactants and Products

- Use `[0]` or `"0"` for zero-order reactions (no reactants)
- Use `[{Abeta}_{O_n0}_{Comp}]` for single reactant
- Use `[{Abeta}_{O_n0}_{Comp},{Abeta}_O1_{Comp}]` for multiple reactants

### Compartment Handling

- **Single compartment**: `"Comp": "[ISF]"`
- **Two compartments**: `"Comp": "[ISF,PVS]"` (for flow between compartments)
- **Multiple compartments**: `"Comp": "[ISF,PVS,central]"` (generates reactions for each pair)

### Parameter Substitution

- `{Comp}`: Replaced with compartment name
- `{Comp1}`: First compartment in multi-compartment reactions
- `{Comp2}`: Second compartment in multi-compartment reactions
- `{X}`: Replaced with contents of "X": ["X1","X2"] of "X": "[f\"X{i}\" for i in range(1,3)]"

### List Comprehensions

Support for Python-style list comprehensions:
```json
"X_n0": "[f\"X{i}\" for i in range(1,24)]"
"X_n1": "[f\"X{i}\" for i in range(2,25)]"
```

### Paired Parameters

Use the `"Paired"` field to ensure parameters are generated together. By default,
all combinations with variable lists are generated unless the two lists (of equal length) are "Paired".
```json
"Paired": "{X_n0,X_n1}"
```

## Examples

### Simple Mass Action Reaction

```json
{
  "Reaction_name": "Production APP ISF",
  "Reactants": "[0]",
  "Products": "[APP]",
  "Rate_type": "MA",
  "Rate_eqtn_prototype": "k_APP_production",
  "Comp": "[ISF]"
}
```

Generated output:
```
 -> APP; k_APP_production * V_ISF
```

### Reversible Reaction with Paired Parameters

```json
{
  "Reaction_name": "Monomer Addition and Dissociation",
  "Reactants": "[{Abeta}_{O_n0}_{Comp},{Abeta}_O1_{Comp}]",
  "Products": "[{Abeta}_{O_n1}_{Comp}]",
  "Rate_type": "RMA",
  "Rate_eqtn_prototype": "[k_{O_n0}_{O_n1}_{Abeta}_{Comp},k_{O_n1}_{O_n0}_{Abeta}_{Comp}]",
  "Comp": "[ISF]",
  "Abeta": "[AB40,AB42]",
  "O_n0": "[f\"O{i}\" for i in range(1,24)]",
  "O_n1": "[f\"O{i}\" for i in range(2,25)]",
  "Paired": "{O_n0,O_n1}"
}
```

### Multi-compartment Flow

```json
{
  "Reaction_name": "Flow ISF to PVS Abeta",
  "Reactants": "[{Abeta}_{O_n0}_{Comp1}]",
  "Products": "[{Abeta}_{O_n0}_{Comp2}]",
  "Rate_type": "UDF",
  "Rate_eqtn_prototype": "(1.0 - sigma_{Comp}_{O_n0}) * Q_PVS",
  "Comp": "[ISF,PVS]",
  "Abeta": "[AB40,AB42]",
  "O_n0": "[f\"O{i}\" for i in range(1,25)]"
}
```

## Error Handling

The program provides clear error messages for:

- Missing required fields
- Invalid rate types
- Insufficient rate constants for RMA reactions
- JSON parsing errors

## Output Format

The generated Antimony reactions follow the format:
```
reactants -> products; rate_equation
```

Where:
- `reactants` and `products` are space-separated species names
- `rate_equation` includes the rate constant and any necessary volume multipliers

## File Structure

- `Reactions_JSON2antimony_4.py`: Main program
- `Geerts_reactions2.json`: Input JSON file with reaction templates
- `generated_reactions3.txt`: Output Antimony reactions
- `clean_json.py`: Utility for cleaning JSON comments (optional)

## Version History

- **v4**: Added rate type validation, compartment volume multiplication, and custom rate type support
- **v3**: Added compartment support and new rate types (UDF, BDF)
- **v2**: Basic JSON to Antimony conversion with parameter generation

## Contributing

When modifying the program:
1. Update the version number in the output filename
2. Add new rate types to the validation list
3. Update this README with any new features
4. Test with sample JSON files

## License

This program is provided without a license or copyright. 

## Authorship
The program was written in Cursor 'Auto Agent' July 1, 2025, with instructions and feedback from Donald L. Elbert.
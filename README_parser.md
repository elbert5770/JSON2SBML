# Reaction Parser for combined_master_model_reactions.txt

This Python program parses the `combined_master_model_reactions.txt` file and extracts structured information about each chemical reaction.

## File Format

The input file contains reactions in the following format:
```
reaction_name: reactants => products; rate_expression;
```

Where:
- `reaction_name:` is a comment describing the reaction
- `reactants` are the input species (can be separated by `+`)
- `=>` separates reactants from products
- `products` are the output species (can be separated by `+`)
- `rate_expression` is the mathematical expression for the reaction rate
- Each line ends with `;`

## Features

The parser handles:
- ✅ Reaction names (comments)
- ✅ Multiple reactants separated by `+`
- ✅ Multiple products separated by `+`
- ✅ Stoichiometric coefficients (e.g., `2 AB40_Monomer`)
- ✅ Complex rate expressions with mathematical operators
- ✅ Special species like `$Source_` and `$Sink_` prefixes
- ✅ JSON output for easy data processing

## Usage

### Basic Usage

```python
from parse_reactions import ReactionParser

# Create parser and parse file
parser = ReactionParser('combined_master_model_reactions.txt')
reactions = parser.parse_file()

# Print summary
parser.print_summary()

# Save to JSON
parser.save_to_json('parsed_reactions.json')
```

### Running the Parser

```bash
python parse_reactions.py
```

This will:
1. Parse all 657 reactions from the file
2. Display a summary of the first 5 reactions
3. Save the parsed data to `parsed_reactions.json`
4. Show statistics about the reactions

### Running the Test Script

```bash
python test_parser.py
```

This demonstrates various ways to analyze the parsed data.

## Output Structure

Each reaction is parsed into a dictionary with the following structure:

```python
{
    'line_number': 1,
    'comment': 'APP_to_C99',
    'reactants': [
        {'coefficient': 1, 'species': 'APP'}
    ],
    'products': [
        {'coefficient': 1, 'species': 'C99'}
    ],
    'rate_expression': 'k_C99*APP*VIS_brain'
}
```

## Example Reactions

### Simple Reaction
```
APP_to_C99: APP => C99; k_C99*APP*VIS_brain;
```
- **Reactants**: 1 APP
- **Products**: 1 C99
- **Rate**: k_C99*APP*VIS_brain

### Reaction with Stoichiometry
```
AB40_dimer_formation: 2 AB40_Monomer => AB40_Oligomer02; k_M_O2_forty*AB40_Monomer*AB40_Monomer*VIS_brain;
```
- **Reactants**: 2 AB40_Monomer
- **Products**: 1 AB40_Oligomer02
- **Rate**: k_M_O2_forty*AB40_Monomer*AB40_Monomer*VIS_brain

### Reaction with Multiple Reactants
```
AB40_antibody_dimer_binding: AB40_Oligomer02 + Ab_t => AB40_Oligomer02_Antibody_bound; fta1*AB40_Oligomer02*Ab_t*VIS_brain;
```
- **Reactants**: 1 AB40_Oligomer02, 1 Ab_t
- **Products**: 1 AB40_Oligomer02_Antibody_bound
- **Rate**: fta1*AB40_Oligomer02*Ab_t*VIS_brain

## Statistics

From the parsed file:
- **Total reactions**: 657
- **Unique reactants**: 263
- **Unique products**: 467
- **Production reactions**: 1
- **Clearance reactions**: 198
- **Binding reactions**: 120

## Files

- `parse_reactions.py` - Main parser implementation
- `test_parser.py` - Example usage and analysis
- `parsed_reactions.json` - Output file with all parsed reactions
- `README_parser.md` - This documentation file

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Error Handling

The parser includes error handling for:
- Missing input file
- Malformed reaction lines
- Empty lines
- File encoding issues

Any lines that cannot be parsed will generate a warning message but won't stop the parsing process. 
#!/usr/bin/env python3
"""
Parser for combined_master_model_reactions.txt

This program reads the file and parses each line into a structured format:
- Comment (reaction name ending in ':')
- Reactants (before '=>')
- Products (after '=>' but before ';')
- Reaction rate expression (after first ';' but before final ';')
"""

import re
from typing import List, Dict, Optional

class ReactionParser:
    def __init__(self, filename: str):
        self.filename = filename
        self.reactions = []
    
    def parse_line(self, line: str) -> Optional[Dict]:
        """
        Parse a single line from the reactions file.
        
        Returns:
            Dictionary with keys: 'comment', 'reactants', 'products', 'rate_expression'
            or None if line is empty/invalid
        """
        # Skip empty lines
        line = line.strip()
        if not line:
            return None
        
        # Pattern to match the structure:
        # comment: reactants => products; rate_expression;
        # or: reactants => products; rate_expression; (no comment)
        # or: reactants -> products; rate_expression (no final semicolon)
        # Supports both => and -> arrows
        pattern = r'^(.+?):\s*(.+?)\s*(?:=>|->)\s*(.+?);\s*(.+?);$'
        
        match = re.match(pattern, line)
        if not match:
            # Try pattern without comment (arrow before colon)
            pattern_no_comment = r'^(.+?)\s*(?:=>|->)\s*(.+?);\s*(.+?);$'
            match = re.match(pattern_no_comment, line)
            if match:
                reactants_str = match.group(1).strip()
                products_str = match.group(2).strip()
                rate_expression = match.group(3).strip()
                comment = ""  # No comment
            else:
                # Try pattern without final semicolon (most common format)
                pattern_no_final_semicolon = r'^(.+?)\s*(?:=>|->)\s*(.+?);\s*(.+)$'
                match = re.match(pattern_no_final_semicolon, line)
                if match:
                    reactants_str = match.group(1).strip()
                    products_str = match.group(2).strip()
                    rate_expression = match.group(3).strip()
                    comment = ""  # No comment
                else:
                    # Try pattern for blank products field (e.g., "reactants -> ; rate_expression")
                    pattern_blank_products = r'^(.+?)\s*(?:=>|->)\s*;\s*(.+)$'
                    match = re.match(pattern_blank_products, line)
                    if match:
                        reactants_str = match.group(1).strip()
                        products_str = ""  # Blank products field
                        rate_expression = match.group(2).strip()
                        comment = ""  # No comment
                    else:
                        # Try pattern for zero-order reactions (no reactants, e.g., "-> products; rate_expression")
                        pattern_zero_order = r'^(?:=>|->)\s*(.+?);\s*(.+)$'
                        match = re.match(pattern_zero_order, line)
                        if match:
                            reactants_str = ""  # No reactants
                            products_str = match.group(1).strip()
                            rate_expression = match.group(2).strip()
                            comment = ""  # No comment
                        else:
                            print(f"Warning: Could not parse line: {line}")
                            return None
        else:
            comment = match.group(1).strip()
            reactants_str = match.group(2).strip()
            products_str = match.group(3).strip()
            rate_expression = match.group(4).strip()
        
        # Parse reactants (split by '+' and handle stoichiometry)
        reactants = self._parse_species(reactants_str)
        
        # Parse products (split by '+' and handle stoichiometry)
        products = self._parse_species(products_str)
        
        return {
            'comment': comment,
            'reactants': reactants,
            'products': products,
            'rate_expression': rate_expression
        }
    
    def _parse_species(self, species_str: str) -> List[Dict]:
        """
        Parse a string of species (reactants or products) separated by '+'
        Handles stoichiometric coefficients.
        
        Returns:
            List of dictionaries with 'coefficient' and 'species' keys
        """
        if not species_str or species_str.strip() == '0':
            # Return a special entry for zero-order (no species)
            return [{'coefficient': 1, 'species': '0'}]
        
        species_list = []
        # Split by '+' but be careful about spaces
        parts = [part.strip() for part in species_str.split('+')]
        
        for part in parts:
            if not part:
                continue
                
            # Check for stoichiometric coefficient (number at the beginning)
            coefficient_match = re.match(r'^(\d+)\s+(.+)$', part)
            if coefficient_match:
                coefficient = int(coefficient_match.group(1))
                species = coefficient_match.group(2).strip()
            else:
                coefficient = 1
                species = part.strip()
            
            species_list.append({
                'coefficient': coefficient,
                'species': species
            })
        
        return species_list
    
    def parse_file(self) -> List[Dict]:
        """
        Parse the entire file and return a list of reaction dictionaries.
        """
        self.reactions = []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    reaction = self.parse_line(line)
                    if reaction:
                        reaction['line_number'] = line_num
                        self.reactions.append(reaction)
        
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
        
        return self.reactions
    
    def print_summary(self):
        """Print a summary of parsed reactions."""
        print(f"Parsed {len(self.reactions)} reactions from '{self.filename}'")
        print("\nFirst 5 reactions:")
        for i, reaction in enumerate(self.reactions[:5]):
            print(f"\nReaction {i+1} (Line {reaction['line_number']}):")
            print(f"  Comment: {reaction['comment']}")
            reactants_str = [f"{r['coefficient']} {r['species']}" for r in reaction['reactants']]
            products_str = [f"{p['coefficient']} {p['species']}" for p in reaction['products']]
            print(f"  Reactants: {reactants_str}")
            print(f"  Products: {products_str}")
            print(f"  Rate Expression: {reaction['rate_expression']}")
    
    def save_to_json(self, output_filename: str):
        """Save parsed reactions to a JSON file."""
        import json
        
        # Convert to JSON-serializable format
        json_data = []
        for reaction in self.reactions:
            json_reaction = {
                'line_number': reaction['line_number'],
                'comment': reaction['comment'],
                'reactants': reaction['reactants'],
                'products': reaction['products'],
                'rate_expression': reaction['rate_expression']
            }
            json_data.append(json_reaction)
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(json_data)} reactions to '{output_filename}'")
        except Exception as e:
            print(f"Error saving to JSON: {e}")

def main():
    """Main function to run the parser."""
    filename = 'Antimony_Geerts_all_reactions_rxnonly.txt'
    
    # Create parser and parse file
    parser = ReactionParser(filename)
    reactions = parser.parse_file()
    
    if reactions:
        # Print summary
        parser.print_summary()
        
        # Save to JSON
        parser.save_to_json('Antimony_Geerts_all_parsed_reactions.json')
        
        # Print some statistics
        print(f"\nStatistics:")
        print(f"Total reactions: {len(reactions)}")
        
        # Count unique reactants and products
        all_reactants = set()
        all_products = set()
        
        for reaction in reactions:
            for reactant in reaction['reactants']:
                all_reactants.add(reactant['species'])
            for product in reaction['products']:
                all_products.add(product['species'])
        
        print(f"Unique reactants: {len(all_reactants)}")
        print(f"Unique products: {len(all_products)}")
        
        # Show some examples of complex reactions
        print(f"\nExamples of reactions with multiple reactants:")
        multi_reactant_reactions = [r for r in reactions if len(r['reactants']) > 1]
        for i, reaction in enumerate(multi_reactant_reactions[:3]):
            print(f"  {i+1}. {reaction['comment']}")
            reactants_str = [f"{r['coefficient']} {r['species']}" for r in reaction['reactants']]
            print(f"     Reactants: {reactants_str}")
    
    else:
        print("No reactions were parsed successfully.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Construct differential equations from parsed reactions.

This program reads the parsed_reactions.json file and constructs
differential equations for each unique species in the reaction network.
"""

import json
import csv
from collections import defaultdict
from typing import List, Dict, Set

class DifferentialEquationBuilder:
    def __init__(self, json_filename: str):
        self.json_filename = json_filename
        self.reactions = []
        self.unique_species = set()
        self.species_equations = defaultdict(list)
    
    def load_reactions(self) -> bool:
        """Load reactions from JSON file."""
        try:
            with open(self.json_filename, 'r', encoding='utf-8') as f:
                self.reactions = json.load(f)
            print(f"Loaded {len(self.reactions)} reactions from {self.json_filename}")
            return True
        except FileNotFoundError:
            print(f"Error: File '{self.json_filename}' not found.")
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return False
    
    def extract_unique_species(self) -> Set[str]:
        """Extract all unique species from reactants and products."""
        species_set = set()
        
        for reaction in self.reactions:
            # Add reactants
            for reactant in reaction['reactants']:
                species = reactant['species']
                # Skip "0" as it's not a real species
                if species != "0":
                    species_set.add(species)
            
            # Add products
            for product in reaction['products']:
                species = product['species']
                # Skip "0" as it's not a real species
                if species != "0":
                    species_set.add(species)
        
        # Convert to sorted list
        self.unique_species = sorted(species_set)
        print(f"Found {len(self.unique_species)} unique species")
        return self.unique_species
    
    def construct_equations(self) -> Dict[str, List[Dict]]:
        """Construct differential equations for each species."""
        # Initialize equations for each species
        for species in self.unique_species:
            self.species_equations[species] = []
        
        # Go through each reaction and add terms to the appropriate equations
        for reaction in self.reactions:
            rate_expr = reaction['rate_expression']
            reaction_name = reaction['comment']
            
            # Handle reactants (negative terms)
            for reactant in reaction['reactants']:
                species = reactant['species']
                coefficient = reactant['coefficient']
                
                # Skip if species is "0" (zero-order reaction)
                if species == "0":
                    continue
                
                # Store detailed information about this term
                term_info = {
                    'sign': '-',
                    'coefficient': coefficient,
                    'rate_expression': rate_expr,
                    'reaction_name': reaction_name,
                    'term_string': f"-{coefficient}*{rate_expr}" if coefficient != 1 else f"-{rate_expr}"
                }
                
                self.species_equations[species].append(term_info)
            
            # Handle products (positive terms)
            for product in reaction['products']:
                species = product['species']
                coefficient = product['coefficient']
                
                # Skip if species is "0" (zero-order reaction)
                if species == "0":
                    continue
                
                # Store detailed information about this term
                term_info = {
                    'sign': '+',
                    'coefficient': coefficient,
                    'rate_expression': rate_expr,
                    'reaction_name': reaction_name,
                    'term_string': f"+{coefficient}*{rate_expr}" if coefficient != 1 else f"+{rate_expr}"
                }
                
                self.species_equations[species].append(term_info)
        
        return self.species_equations
    
    def format_equation(self, species: str, terms: List[Dict]) -> str:
        """Format a single differential equation."""
        if not terms:
            return f"d {species}/dt = 0"
        
        # Extract term strings and join them
        term_strings = [term['term_string'] for term in terms]
        equation = f"d {species}/dt = " + " ".join(term_strings)
        return equation
    
    def save_equations_to_file(self, output_filename: str):
        """Save all differential equations to a text file."""
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write("Differential Equations for Chemical Reaction Network\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Total species: {len(self.unique_species)}\n")
                f.write(f"Total reactions: {len(self.reactions)}\n\n")
                
                # Write equations for each species
                for species in self.unique_species:
                    terms = self.species_equations[species]
                    equation = self.format_equation(species, terms)
                    f.write(f"{equation}\n\n")
                
                # Write summary statistics
                f.write("\n" + "=" * 60 + "\n")
                f.write("Summary Statistics:\n")
                f.write(f"Species with no reactions: {sum(1 for terms in self.species_equations.values() if not terms)}\n")
                f.write(f"Species with reactions: {sum(1 for terms in self.species_equations.values() if terms)}\n")
                
                # Find species with most terms
                max_terms = max(len(terms) for terms in self.species_equations.values())
                species_with_max_terms = [s for s, terms in self.species_equations.items() if len(terms) == max_terms]
                f.write(f"Species with most terms ({max_terms}): {', '.join(species_with_max_terms)}\n")
            
            print(f"Saved {len(self.unique_species)} differential equations to '{output_filename}'")
            
        except Exception as e:
            print(f"Error saving equations: {e}")
    
    def save_reaction_details_csv(self, output_filename: str):
        """Save detailed reaction information to a CSV file."""
        try:
            with open(output_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Species', 'Sign', 'Reaction', 'Rate_Expression'])
                
                for species in sorted(self.unique_species):
                    terms = self.species_equations[species]
                    if terms:
                        for term in terms:
                            writer.writerow([
                                species,
                                term['sign'],
                                term['reaction_name'],
                                term['rate_expression']
                            ])
                    else:
                        # Species with no reactions
                        writer.writerow([species, '', '', ''])
                
            print(f"Saved reaction details to '{output_filename}'")
            
            # Save reactions per species data to separate CSV
            reactions_per_species_filename = 'reactions_per_species.csv'
            with open(reactions_per_species_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Species', 'Number_of_Terms'])
                
                for species in sorted(self.unique_species):
                    terms = self.species_equations[species]
                    num_terms = len(terms)
                    writer.writerow([species, num_terms])
                
            print(f"Saved reactions per species data to '{reactions_per_species_filename}'")
            
        except Exception as e:
            print(f"Error saving CSV: {e}")
    
    def print_sample_equations(self, num_samples: int = 5):
        """Print sample equations for verification."""
        print(f"\nSample differential equations (first {num_samples}):")
        print("-" * 50)
        
        for i, species in enumerate(self.unique_species[:num_samples]):
            terms = self.species_equations[species]
            equation = self.format_equation(species, terms)
            print(f"{i+1}. {equation}")
            
            if terms:
                print(f"   Terms: {len(terms)}")
                for j, term in enumerate(terms[:3]):  # Show first 3 terms
                    print(f"     {j+1}. {term['sign']} {term['reaction_name']}: {term['rate_expression']}")
                if len(terms) > 3:
                    print(f"     ... and {len(terms) - 3} more terms")
            print()

def main():
    """Main function to construct differential equations."""
    json_filename = 'Antimony_Geerts_all_parsed_reactions.json'
    output_filename = 'Antimony_Geerts_all_differential_equations.txt'
    
    # Create equation builder
    builder = DifferentialEquationBuilder(json_filename)
    
    # Load reactions
    if not builder.load_reactions():
        return
    
    # Extract unique species
    unique_species = builder.extract_unique_species()
    print(f"Unique species (first 10): {unique_species[:10]}")
    
    # Construct equations
    equations = builder.construct_equations()
    
    # Print sample equations
    builder.print_sample_equations(5)
    
    # Save to file
    builder.save_equations_to_file(output_filename)
    
    # Save CSV with detailed reaction information
    csv_filename = 'Antimony_Geerts_all_reaction_details.csv'
    builder.save_reaction_details_csv(csv_filename)
    
    # Print some statistics
    print("\nStatistics:")
    print(f"Total species: {len(unique_species)}")
    print(f"Species with reactions: {sum(1 for terms in equations.values() if terms)}")
    print(f"Species with no reactions: {sum(1 for terms in equations.values() if not terms)}")
    
    # Find species with most terms
    max_terms = max(len(terms) for terms in equations.values())
    species_with_max_terms = [s for s, terms in equations.items() if len(terms) == max_terms]
    print(f"Species with most terms ({max_terms}): {', '.join(species_with_max_terms[:3])}")

if __name__ == "__main__":
    main() 
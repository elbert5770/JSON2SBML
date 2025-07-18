#!/usr/bin/env python3
"""
Test script to demonstrate how to use the parsed reaction data
"""

from parse_reactions import ReactionParser

def test_parser():
    """Test the reaction parser with some specific examples."""
    
    # Create parser and parse file
    parser = ReactionParser('combined_master_model_reactions.txt')
    reactions = parser.parse_file()
    
    print(f"Successfully parsed {len(reactions)} reactions\n")
    
    # Example 1: Find reactions with specific reactants
    print("=== Reactions involving AB40_Monomer ===")
    ab40_reactions = [r for r in reactions if any(r['species'] == 'AB40_Monomer' for r in r['reactants'] + r['products'])]
    for i, reaction in enumerate(ab40_reactions[:3]):
        print(f"{i+1}. {reaction['comment']}")
        print(f"   Reactants: {[f'{r['coefficient']} {r['species']}' for r in reaction['reactants']]}")
        print(f"   Products: {[f'{p['coefficient']} {p['species']}' for p in reaction['products']]}")
        print()
    
    # Example 2: Find reactions with stoichiometric coefficients
    print("=== Reactions with stoichiometric coefficients > 1 ===")
    stoichiometric_reactions = []
    for reaction in reactions:
        for reactant in reaction['reactants']:
            if reactant['coefficient'] > 1:
                stoichiometric_reactions.append(reaction)
                break
        else:
            for product in reaction['products']:
                if product['coefficient'] > 1:
                    stoichiometric_reactions.append(reaction)
                    break
    
    for i, reaction in enumerate(stoichiometric_reactions[:3]):
        print(f"{i+1}. {reaction['comment']}")
        print(f"   Reactants: {[f'{r['coefficient']} {r['species']}' for r in reaction['reactants']]}")
        print(f"   Products: {[f'{p['coefficient']} {p['species']}' for p in reaction['products']]}")
        print()
    
    # Example 3: Find reactions with complex rate expressions
    print("=== Reactions with complex rate expressions (containing parentheses) ===")
    complex_rate_reactions = [r for r in reactions if '(' in r['rate_expression'] and ')' in r['rate_expression']]
    for i, reaction in enumerate(complex_rate_reactions[:3]):
        print(f"{i+1}. {reaction['comment']}")
        print(f"   Rate Expression: {reaction['rate_expression']}")
        print()
    
    # Example 4: Count reactions by type
    print("=== Reaction Statistics ===")
    production_reactions = [r for r in reactions if 'production' in r['comment'].lower()]
    clearance_reactions = [r for r in reactions if 'clearance' in r['comment'].lower()]
    binding_reactions = [r for r in reactions if 'binding' in r['comment'].lower()]
    
    print(f"Production reactions: {len(production_reactions)}")
    print(f"Clearance reactions: {len(clearance_reactions)}")
    print(f"Binding reactions: {len(binding_reactions)}")
    
    # Example 5: Find reactions with specific patterns
    print("\n=== Reactions with 'AB42' in the name ===")
    ab42_reactions = [r for r in reactions if 'AB42' in r['comment']]
    print(f"Found {len(ab42_reactions)} AB42-related reactions")
    
    # Show first few
    for i, reaction in enumerate(ab42_reactions[:3]):
        print(f"{i+1}. {reaction['comment']}")

if __name__ == "__main__":
    test_parser() 
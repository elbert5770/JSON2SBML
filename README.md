# JSON2SBML
A format for entering complex chemical reactions programmatically

Step 1: The reactions are encoded in 'Geerts_reactions2.json'.
Step 2: Run 'Reactions_JSON2antimony_6.py'. This generates 'New_reactions.txt' that contains the compartments, species and reactions in antimony format.  The compartments are summarized in 'unique_compartments.txt' and the species are summarized in 'unique_species.txt' for your reference.  
Step 3: The antimony model requires values for the parameters.  The list of unique parameters is 'unique_parameters.txt'.  The parameter values should be entered as 'parameter = value' in a new file.  
Step 4: This list of parameters with values is then copy and pasted at the end of the New_reactions text to create a complete Antimony model.
Step 5: Copy and paste the Antimony model into 'Antimony_Geerts_model.py' and run the program to simulate the model and/or export the SBML model.

Limitations: Antimony fails to parse units such as 1/s using the standard entry format.  The units would otherwise be added to the SBML model by Antimony.

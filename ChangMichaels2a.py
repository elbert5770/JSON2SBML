

def build_reactions():
    all_reactions = []
    counter = 0
    
    for Species in ['Antibody','AB42']:
        for Tissue in ['Lung','Heart','Kidney','Muscle','Skin','Adipose','Thymus','Bone','Other','Liver','Spleen','Pancreas','SI','LI']:
            for Comp in [ ['Vascular','Interstitial'],
                ['Vascular','Endosomal'],
                ['Interstitial','Endosomal']
                ]:      
                counter += 1
                Comp1 = f"{Tissue}{Comp[0]}"
                Comp2 = f"{Tissue}{Comp[1]}"
                Reaction_name = f"Flow within {Tissue}"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                match Comp:
                    case ['Vascular','Interstitial']: 
                        Rate_eqtn_prototype = f"(1-RC_{Tissue}_Vascular) * L_{Tissue}"
                    case ['Vascular','Endosomal']: 
                        if Species == 'Antibody':
                            Rate_eqtn_prototype = f"CLup_{Tissue}"
                    case ['Interstitial','Endosomal']: 
                        if Species == 'Antibody':
                            Rate_eqtn_prototype = f"CLup_{Tissue}"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)
        
        
            for Comp in  ['Endosomal']:
                if Species == 'Antibody':
                    counter += 2
                    Comp1 = f"{Tissue}Endosomal"
                    Reaction_name = f"{Tissue} Endosomal reactions"
                    Reactants = f"[{Species}_{Comp1},FCRn_{Comp1}]"
                    Products = f"[{Species}__FCRn_{Comp1}]"
                    Rate_type = "RMA"
                    Rate_eqtn_prototype = f"[Kon_FcRn,Koff_FcRn]"
                    Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                    all_reactions.append(Reaction_dict)

                    counter += 1
                    Reaction_name = f"{Tissue} Endosomal reactions"
                    Reactants = f"[{Species}_{Comp1}]"
                    Products = f"[0]"
                    Rate_type = "MA"
                    Rate_eqtn_prototype = f"Kdeg"
                    Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                    all_reactions.append(Reaction_dict)

            for Comp in [ ['Endosomal','Vascular'],
                ['Endosomal','Interstitial']]:
                if Species == 'Antibody':
                    counter += 1
                    Comp1 = f"{Tissue}{Comp[0]}"
                    Comp2 = f"{Tissue}{Comp[1]}"
                    Reaction_name = f"Flow out of endosomal"
                    Reactants = f"[{Species}__FCRn_{Comp1}]"
                    Products = f"[{Species}_{Comp2},FCRn_{Comp1}]"
                    Rate_type = "UDF"
                    match Comp:
                        case  ['Endosomal','Vascular']: 
                            Rate_eqtn_prototype = f"CLup_{Tissue} * FR"
                        case  ['Endosomal','Interstitial']: 
                            Rate_eqtn_prototype = f"CLup_{Tissue} * (1 - FR)"
                    Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                    all_reactions.append(Reaction_dict)

    
        for Tissue in ['Heart','Kidney','Muscle','Skin', 'Liver','Adipose','Thymus','Bone','Other','SI','LI','Spleen','Pancreas']:
            for Comp in [ ['LungVascular','Vascular']]:
                counter += 1
                Comp1 = Comp[0]
                Comp2 = f"{Tissue}{Comp[1]}"
                Reaction_name = f"Flow between lung and {Tissue}"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"Q_{Tissue}"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)
        
        for Tissue in ['Heart','Kidney','Muscle','Skin','Adipose','Thymus','Bone','Other']:
            for Comp in [ ['Vascular','Plasma']]: 
                counter += 1
                Comp1 = f"{Tissue}{Comp[0]}"
                Comp2 = Comp[1]
                Reaction_name = f"Flow between {Tissue} and plasma"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"(Q_{Tissue} - L_{Tissue})"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)

        for Tissue in ['Lung','Heart','Kidney','Muscle','Skin','Adipose','Thymus','Bone','Other','SI','LI','Spleen','Pancreas','Liver']:    
            for Comp in [ ['Interstitial','LymphNode']]: 
                counter += 1
                Comp1 = f"{Tissue}{Comp[0]}"
                Comp2 = Comp[1]
                Reaction_name = f"Flow between {Tissue} and LymphNode"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"(1 - RC_{Tissue}_Lymph) * L_{Tissue}" 
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)
                         
        for Comp in [ ['LymphNode','Plasma']]: 
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Flow between LymphNode and Plasma"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"L_{Comp1}" 
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)           

        for Comp in [ 'SI','LI','Spleen','Pancreas']: 
            counter += 1
            Comp1 = f"{Comp}Vascular"
            Reaction_name = f"Flow between Digestive system and Liver"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_LiverVascular]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"(Q_{Comp} - L_{Comp})" 
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict) 
        
        for Tissue in ['Liver']:
            for Comp in [ ['Vascular','Plasma']]: 
                counter += 1
                Comp1 = f"{Tissue}{Comp[0]}"
                Comp2 = Comp[1]
                Reaction_name = f"Flow between {Tissue} and plasma"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"((Q_{Tissue} - L_{Tissue}) + (Q_Spleen - L_Spleen) + (Q_Pancreas - L_Pancreas) + (Q_SI - L_SI) + (Q_LI - L_LI))"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)


        for Comp in [ ['LymphNode','Plasma']]:
                counter += 1
                Comp1 = Comp[0]
                Comp2 = Comp[1]
                Reaction_name = f"Flow between LymphNode and plasma"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"L_{Comp1}"  
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)

        for Comp in [ ['Plasma','LungVascular']]:
                counter += 1
                Comp1 = Comp[0]
                Comp2 = Comp[1]
                Reaction_name = f"Flow between LymphNode and plasma"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"(Q_Lung + L_Lung)"  
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)
#Module CNS
        for Tissue in ['Brain']:
            for Comp in [ ['LungVascular','Vascular']]:
                counter += 1
                Comp1 = Comp[0]
                Comp2 = f"{Tissue}{Comp[1]}"
                Reaction_name = f"Flow between lung and {Tissue}"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"Q_{Tissue}"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)
        
        for Tissue in ['Brain']:
            for Comp in [ ['Vascular','Plasma']]: 
                counter += 1
                Comp1 = f"{Tissue}{Comp[0]}"
                Comp2 = Comp[1]
                Reaction_name = f"Flow between {Tissue} and plasma"
                Reactants = f"[{Species}_{Comp1}]"
                Products = f"[{Species}_{Comp2}]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"(Q_{Tissue} - L_{Tissue})"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)
        
           
        for Comp in [ ['BrainISF','LymphNode']]: 
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Flow between {Comp[0]} and LymphNode"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"(1 - RC_{Comp[0]}_Lymph) * Q_BrainISF" 
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)
        
        for Comp in [ ['SAS','LymphNode']]: 
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Flow between {Comp[0]} and LymphNode"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"(1 - RC_{Comp[0]}_Lymph) * Q_CSF" 
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

        for Comp in [ ['BrainVascular','BrainISF'],
        ['BrainVascular','BBB'],
        ['BrainVascular','BCSFB'],
        ['BrainVascular','LV'],
        ['BrainVascular','TFV'],
        ['BrainISF','LV'],
        ['BrainISF','TFV'],
        ['SAS','BrainISF'],
        ['LV','TFV'],
        ['TFV','CM'],
        ['CM','SAS'],
         ]:      
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Flow within tissue"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            match Comp:
                case ['BrainVascular','BrainISF']: 
                    Rate_eqtn_prototype = f"(1-RC_BBB) * Q_BrainISF"
                
                case ['BrainVascular','BBB']: 
                    if Species == 'Antibody':
                        Rate_eqtn_prototype = f"CLup_BBB"
                case ['BrainVascular','BCSFB']: 
                    if Species == 'Antibody':
                        Rate_eqtn_prototype = f"CLup_BCSFB"
                case ['BrainVascular','LV']: 
                    Rate_eqtn_prototype = f"(1-RC_BCSFB) * f_LV * Q_CSF"
                case ['BrainVascular','TFV']: 
                    Rate_eqtn_prototype = f"(1-RC_BCSFB) * (1 - f_LV) * Q_CSF"
                case ['BrainISF','LV']: 
                    Rate_eqtn_prototype = f"f_LV * Q_glymph"
                case ['BrainISF','TFV']: 
                    Rate_eqtn_prototype = f"(1 - f_LV) * Q_glymph"
                case ['SAS','BrainISF']: 
                    Rate_eqtn_prototype = f"Q_glymph"
                case ['LV', 'TFV']: 
                    Rate_eqtn_prototype = f"f_LV * (Q_CSF + Q_glymph)"
                case ['TFV', 'CM']: 
                    Rate_eqtn_prototype = f"(Q_CSF + Q_glymph)"
                case ['CM', 'SAS']: 
                    Rate_eqtn_prototype = f"(Q_CSF + Q_glymph)"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    
        for Comp in  ['BBB','BCSFB']:    
            if Species == 'Antibody':  
                counter += 2
                Reaction_name = f"BrainEndosomal reactions"
                Reactants = f"[{Species}_{Comp},FCRn_{Comp}]"
                Products = f"[{Species}__FCRn_{Comp}]"
                Rate_type = "RMA"
                Rate_eqtn_prototype = f"[Kon_FcRn,Koff_FcRn]"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)

                counter += 1
                Reaction_name = f"BrainEndosomal degradation"
                Reactants = f"[{Species}_{Comp}]"
                Products = f"[0]"
                Rate_type = "MA"
                Rate_eqtn_prototype = f"Kdeg"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)

        for Comp in [ ['BBB','BrainVascular'],
            ['BBB','BrainISF'],
            ['BCSFB','BrainVascular'],
            ['BCSFB','LV'],
            ['BCSFB','TFV']]:
            if Species == 'Antibody':
                counter += 1
                Comp1 = Comp[0]
                Comp2 = Comp[1]
                Reaction_name = f"Flow out of endosomal"
                Reactants = f"[{Species}__FCRn_{Comp1}]"
                Products = f"[{Species}_{Comp2},FCRn_{Comp1}]"
                Rate_type = "UDF"
                match Comp:
                    case  ['BBB','BrainVascular']: 
                        Rate_eqtn_prototype = f"CLup_BBB * f_BBB * FR"
                    case  ['BBB','BrainISF']: 
                        Rate_eqtn_prototype = f"CLup_BBB * f_BBB * (1 - FR)"
                    case  ['BCSFB','BrainVascular']: 
                        Rate_eqtn_prototype = f"CLup_BCSFB * (1 - f_BBB) * FR"
                    case  ['BCSFB','LV']: 
                        Rate_eqtn_prototype = f"f_LV * CLup_BCSFB * (1 - f_BBB) * (1 - FR)"
                    case  ['BCSFB','TFV']: 
                        Rate_eqtn_prototype = f"(1 - f_LV) * CLup_BCSFB * (1 - f_BBB) * (1 - FR)"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)

    for Species in ['C99']:
        for Comp in ['BrainISF']:
            counter += 1
            Reaction_name = f"AB42 Synthesis"
            Reactants = f"[APP_{Comp}]"
            Products = f"[{Species}_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"k_C99"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

    for Species in ['C99']:
            for Comp in ['BrainISF']:
                counter += 1
                Reaction_name = f"AB42 Synthesis"
                Reactants = f"[{Species}_{Comp}]"
                Products = f"[0]"
                Rate_type = "MA"
                Rate_eqtn_prototype = f"v_C99"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
                all_reactions.append(Reaction_dict)
    
    for Species in ['APP']:
        for Comp in ['BrainISF']:
            counter += 1
            Reaction_name = f"APP Synthesis"
            Reactants = f"[0]"
            Products = f"[{Species}_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"k_APP"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

    for Species in ['AB42']:
        for Comp in ['BrainISF']:
            counter += 1
            Reaction_name = f"AB42 Synthesis"
            Reactants = f"[C99_{Comp}]"
            Products = f"[{Species}_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"k_Ab42"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"AB42 Degradation"
            Reactants = f"[{Species}_{Comp}]"
            Products = f"[0]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"IDE_conc"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"AB42 Primary Oligomerization"
            Reactants = f"[n_oligo1_{Species} {Species}_{Comp}]"
            Products = f"[{Species}_Oligomer_{Comp}]"
            Rate_type = "custom"
            Rate_eqtn_prototype = f"k_oligo1_{Species} * ({Species}_{Comp}/V_{Comp})^n_oligo1_{Species} * V_{Comp}"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"AB42 Secondary Oligomerization"
            Reactants = f"[n_oligo2_{Species} {Species}_{Comp},{Species}_FibrilMass_{Comp}]"
            Products = f"[{Species}_Oligomer_{Comp}]"
            Rate_type = "custom"
            Rate_eqtn_prototype = f"k_oligo2_{Species} * ({Species}_{Comp}/V_{Comp})^n_oligo2_{Species} * {Species}_FibrilMass_{Comp}/V_{Comp} * V_{Comp}"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"AB42 De-Oligomerization"
            Reactants = f"[{Species}_Oligomer_{Comp}]"
            Products = f"[{Species}_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"k_d_Oligomer_AB42"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"AB42 FibrilNumber formation"
            Reactants = f"[{Species}_Oligomer_{Comp},n_c_{Species} {Species}_{Comp}]"
            Products = f"[{Species}_FibrilNumber_{Comp}]"
            Rate_type = "custom"
            Rate_eqtn_prototype = f"k_c_AB42 * ({Species}_Oligomer_{Comp}/V_{Comp}) * ({Species}_{Comp}/V_{Comp})^n_c_{Species} * V_{Comp}"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"AB42 FibrilMass increase"
            Reactants = f"[{Species}_{Comp}]"
            Products = f"[{Species}_FibrilMass_{Comp}]"
            Rate_type = "custom"
            Rate_eqtn_prototype = f"k_plus_{Species} * ({Species}_FibrilNumber_{Comp}/V_{Comp}) * ({Species}_{Comp}/V_{Comp}) * V_{Comp}"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)
        
            counter += 1
            Reaction_name = f"AB42 FibrilMass depolymerization"
            Reactants = f"[{Species}_FibrilMass_{Comp}]"
            Products = f"[{Species}_{Comp}]"
            Rate_type = "custom"
            Rate_eqtn_prototype = f"k_off_{Species} * ({Species}_FibrilNumber_{Comp}/V_{Comp}) * V_{Comp}"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"Microglia Degradation Plaque"
            Reactants = f"[{Species}_FibrilMass_{Comp}]"
            Products = f"[0]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"Microglia*(Hi_lo_ratio*Microglia_high_frac*Microglia_Vmax_{Species}/(Microglia_EC50_{Species} + {Species}_FibrilMass_{Comp}) + (1.0 - Microglia_high_frac)*Microglia_Vmax_{Species}/(Microglia_EC50_{Species} + {Species}_FibrilMass_{Comp}))"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
            
    print(counter)
    return all_reactions



all_reactions = build_reactions()

with open("Chang2019Michaels2022_all_reactions.txt", "w", encoding="utf-8") as f:
    for reaction in all_reactions:
        f.write(str(reaction) + "\n")

# print(all_reactions)


    
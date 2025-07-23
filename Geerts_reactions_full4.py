
# Aggregation reactions
def build_reactions():
    all_reactions = []
    counter = 0
    for Species in ['AB40', 'AB42']:
        for n in range(1, 24):
            for Comp in ['ISF']:
                counter += 1
                Reaction_name = f"Monomer Addition and Dissociation"
                Reactants = f"[{Species}_O1_{Comp}, {Species}_O{n}_{Comp}]"
                Products = f"[{Species}_O{n+1}_{Comp}]"
                Rate_type = "RMA"
                Rate_eqtn_prototype = f"[k_O{n}_O{n+1}_{Species}_{Comp},k_O{n+1}_O{n}_{Species}_{Comp}]"            
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                
                all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for n in range(1, 17):
            for Comp in ['ISF']:
                counter += 1
                Reaction_name = f"Plaque Driven Monomer Addition (PDMA)"
                Reactants = f"[{Species}_O1_{Comp}, {Species}_O{n}_{Comp}]"
                Products = f"[{Species}_O{n+1}_{Comp}]"
                Rate_type = "MA"
                Rate_eqtn_prototype = f"k_O{n}_O{n+1}_{Species}_{Comp}*{Species}_PDMA_Vmax_{Comp}*({Species}_O25_{Comp} / ({Species}_O25_{Comp} + {Species}_PDMA_EC50_{Comp}))"            
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                
                all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for Comp in ['ISF','PVS','BBB','BCSFB','BrainPlasma','CM','LV','TFV','SAS' ]:
            counter += 1
            Reaction_name = f"Monomer binding antibody"
            Reactants = f"[{Species}_O1_{Comp},Antibody_{Comp}]"
            Products = f"[{Species}_O1__Antibody_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"k0_Antibody"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,
            }
            
            all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for Comp in ['central']:
            counter += 1
            Reaction_name = f"Monomer binding to antibody central"
            Reactants = f"[{Species}_O1_{Comp},Antibody_{Comp}]"
            Products = f"[{Species}_O1__Antibody_centralAntibody]"
            Rate_type = "custom"
            Rate_eqtn_prototype = f"k0_Antibody * (AB40_O1_central/V_central) * (Antibody_central/V_centralAntibody) * V_centralAntibody"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
    
    for Species in ['AB40', 'AB42']:
        for Comp in ['central']:
            counter += 1
            Reaction_name = f"Monomer binding to antibody corrected central"
            Reactants = f"[0]"
            Products = f"[{Species}_O1_{Comp}]"
            Rate_type = "custom"
            Rate_eqtn_prototype = f"k0_Antibody * (AB40_O1_central/V_central) * (Antibody_central/V_centralAntibody) * (V_centralAntibody - V_central)"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
    
    for Species in ['AB40', 'AB42']:
        for n in range(2, 18):
            for Comp in ['ISF','PVS']:
                counter += 1
                Reaction_name = f"Oligomer binding antibody"
                Reactants = f"[{Species}_O{n}_{Comp},Antibody_{Comp}]"
                Products = f"[{Species}_O{n}__Antibody_{Comp}]"
                Rate_type = "MA"
                Rate_eqtn_prototype = f"k1_Antibody"            
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                
                all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for n in range(18, 25):
            for Comp in ['ISF','PVS']:
                counter += 1
                Reaction_name = f"Proto binding antibody"
                Reactants = f"[{Species}_O{n}_{Comp},Antibody_{Comp}]"
                Products = f"[{Species}_O{n}__Antibody_{Comp}]"
                Rate_type = "MA"
                Rate_eqtn_prototype = f"k2_Antibody"            
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                
                all_reactions.append(Reaction_dict)            
    
    for Species in ['AB40', 'AB42']:
        for Comp in ['ISF','PVS']:
            counter += 1
            Reaction_name = f"Plaque binding antibody"
            Reactants = f"[{Species}_O25_{Comp},Antibody_{Comp}]"
            Products = f"[{Species}_O25__Antibody_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"k3_Antibody"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}

            all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for n in range(13, 19):
            for Comp in ['ISF']:
                counter += 1
                Reaction_name = f"Plaque Formation"
                Reactants = f"[{Species}_O1_{Comp},{Species}_O{n}_{Comp}]"
                Products = f"[{Species}_O25_{Comp}]"
                Rate_type = "MA"
                Rate_eqtn_prototype = f"Baseline_{Species}_O_P*k_O{n}_O{n+1}_{Species}_{Comp}"            
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)
    
    for Species in ['AB40', 'AB42']:
        for n in range(2, 25):
            for Comp in ['ISF']:    
                counter += 1
                Reaction_name = f"Microglia Degradation Abeta"
                Reactants = f"[{Species}_O{n}_{Comp}]"
                Products = f"[0]"
                Rate_type = "MA"
                Rate_eqtn_prototype = f"Microglia*(Hi_lo_ratio*Microglia_high_frac*Microglia_Vmax_{Species}/(Microglia_EC50_{Species} + {Species}_O{n}_{Comp}) + (1.0 - Microglia_high_frac)*Microglia_Vmax_{Species}/(Microglia_EC50_{Species} + {Species}_O{n}_{Comp}))"            
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)
    
    for Species in ['AB40', 'AB42']:
        for Comp in ['ISF']:
            counter += 1
            Reaction_name = f"Microglia Degradation Plaque"
            Reactants = f"[{Species}_O25_{Comp}]"
            Products = f"[0]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"0.5*Microglia*(Microglia_high_frac*Microglia_high_rate_{Species} + (1.0 - Microglia_high_frac)*Microglia_low_rate_{Species})"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    for Species in ['AB40', 'AB42']:
        for n in range(1, 26):
            for Comp in ['ISF']:
                counter += 1
                Reaction_name = f"Microglia Degradation Abeta-Antibody"
                Reactants = f"[{Species}_O{n}__Antibody_{Comp}]"
                Products = f"[0]"
                Rate_type = "MA"
                Rate_eqtn_prototype = f"Microglia*(Microglia_high_frac*Microglia_high_rate_mAb + (1.0 - Microglia_high_frac)*Microglia_low_rate_mAb)"            
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for Comp in ['ISF']:
            counter += 1
            Reaction_name = f"O24 split"
            Reactants = f"[{Species}_O24_{Comp}]"
            Products = f"[{Species}_O12_{Comp},{Species}_O12_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"k_O24_O12_{Species}_{Comp}*k_O24_O23_{Species}_{Comp}"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for Comp in ['ISF']:
            counter += 1
            Reaction_name = f"IDE Degradation Monomer ISF"
            Reactants = f"[{Species}_O1_{Comp}]"
            Products = f"[0]"
            Rate_type = "custom_conc_per_time"  
            Rate_eqtn_prototype = f"IDE_conc_{Comp} * {Species}_IDE_Kcat_{Comp} * (({Species}_O1_{Comp})^{Species}_IDE_Hill_{Comp} / (({Species}_O1_{Comp})^{Species}_IDE_Hill_{Comp} + {Species}_IDE_IC50_{Comp}^{Species}_IDE_Hill_{Comp}))"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    for Comp in ['ISF']:
        counter += 1
        Reaction_name = f"Production APP ISF"
        Reactants = f"[0]"
        Products = f"[APP_{Comp}]"
        Rate_type = "MA"
        Rate_eqtn_prototype = f"k_APP_production"            
        Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
        all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for Comp in ['central']:
            counter += 1
            Reaction_name = f"Systemic production Abeta"
            Reactants = f"[0]"
            Products = f"[{Species}_O1_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"{Species}_systemic_synthesis_rate/V_central" 
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    for Comp in ['ISF']:
        counter += 1
        Reaction_name = f"APP to C99 ISF"
        Reactants = f"[APP_{Comp}]"
        Products = f"[C99_{Comp}]"
        Rate_type = "MA"
        Rate_eqtn_prototype = f"k_C99"            
        Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
        all_reactions.append(Reaction_dict)

    for Comp in ['ISF']:
        counter += 1
        Reaction_name = f"Degradation C99 ISF"
        Reactants = f"[C99_{Comp}]"
        Products = f"[0]"   
        Rate_type = "MA"
        Rate_eqtn_prototype = f"v_C99"            
        Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
        all_reactions.append(Reaction_dict)

    for Species in ['AB40', 'AB42']:
        for Comp in ['ISF']:
            counter += 1
            Reaction_name = f"C99 to Abeta ISF"
            Reactants = f"[C99_{Comp}]"
            Products = f"[{Species}_O1_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"k_{Species}"            
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    for Species in ['AB40', 'AB42']:
        for Comp in [['ISF','PVS']]:
            for n in range(2, 25):
                counter += 1
                Comp1 = Comp[0]
                Comp2 = Comp[1]
                Reaction_name = f"Flow ISF to PVS oligomer/proto"
                Reactants = f"[{Species}_O{n}_{Comp1}]"
                Products = f"[{Species}_O{n}_{Comp2}]"
                Rate_type = "UDF"
                
                if n < 10:
                    Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_oligomer1) * Q_PVS"
                elif n < 17:
                    Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_oligomer2) * Q_PVS"
                else:
                    Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_proto) * Q_PVS"
            
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)
    
    for Species in ['AB40', 'AB42']:
        for Comp in [['PVS','central']]:
            for n in range(2, 25):
                counter += 1
                Comp1 = Comp[0]
                Comp2 = Comp[1]
                Reaction_name = f"Flow PVS to central oligomer/proto"
                Reactants = f"[{Species}_O{n}_{Comp1}]"
                Products = f"[0]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_Abeta) * Q_PVS"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)
    
    for Species in ['AB40', 'AB42']:
        for Comp in [['PVS','centralAntibody']]:
            for n in range(2, 25):
                counter += 1
                Comp1 = Comp[0]
                Comp2 = Comp[1]
                Reaction_name = f"Flow PVS to central oligomer/proto-Antibody"
                Reactants = f"[{Species}_O{n}__Antibody_{Comp1}]"
                Products = f"[0]"
                Rate_type = "UDF"
                Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_Antibody) * Q_PVS"
                Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
                all_reactions.append(Reaction_dict)

    for Species in ['AB40_O1', 'AB42_O1', 'AB40_O1__Antibody', 'AB42_O1__Antibody','Antibody']:
        for Comp in [['PVS','central'],['ISF','central'],['ISF','LV'],['ISF','TFV'],['BrainPlasma','ISF'],['BrainPlasma','LV'],['BrainPlasma','TFV'],['LV','TFV'],['TFV','CM'],['CM','SAS'],['SAS','ISF'],['SAS','central'],['BrainPlasma','central'],['central','BrainPlasma']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            #['PVS','central'],['ISF','central'],
            # ['ISF','LV'],['ISF','TFV'],['BrainPlasma','ISF'],['BrainPlasma','LV'],
            # ['BrainPlasma','TFV'],['LV','TFV'],['TFV','CM'],['CM','SAS'],['SAS','ISF'],
            # ['SAS','central'],['BrainPlasma','central'],['central','BrainPlasma']
            match Comp:
                case ['PVS','central']:
                    Reaction_name = f"Flow PVS to central "
                    if Species == 'AB40_O1' or Species == 'AB42_O1':
                        Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_Abeta) * Q_PVS" 
                    else:
                        Comp2 = 'centralAntibody'
                        Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_Antibody) * Q_PVS"
                        Products = f"[{Species}_{Comp2}]"        
                case ['ISF','central']: 
                    Reaction_name = f"Flow ISF to central "
                    if Species == 'AB40_O1' or Species == 'AB42_O1':
                        Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_Abeta) * (Qbrain_ISF - Q_PVS)"
                    else:
                        Comp2 = 'centralAntibody'
                        Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_Antibody) * (Qbrain_ISF - Q_PVS)"
                        Products = f"[{Species}_{Comp2}]"
                case ['ISF','LV']:
                    Reaction_name = f"Flow ISF to LV "
                    Rate_eqtn_prototype = f"f_LV*Qglymph"                  
                case ['ISF','TFV']:
                    Reaction_name = f"Flow ISF to TFV Abeta"
                    Rate_eqtn_prototype = f"(1.0 - f_LV) * Qglymph"
                case ['BrainPlasma','ISF']:
                    Reaction_name = f"Flow BrainPlasma to ISF Abeta"
                    Rate_eqtn_prototype = f"(1.0 - sigma_BBB)*Qbrain_ISF"
                case ['BrainPlasma','LV']:
                    Reaction_name = f"Flow BrainPlasma to LV Abeta"
                    Rate_eqtn_prototype = f"f_LV*(1.0 - sigma_BCSFB)*Q_CSF"
                case ['BrainPlasma','TFV']: 
                    Reaction_name = f"Flow BrainPlasma to TFV Abeta"
                    Rate_eqtn_prototype = f"(1.0 - f_LV)*(1.0 - sigma_BCSFB)*Q_CSF"
                case ['LV','TFV']: 
                    Reaction_name = f"Flow LV to TFV Abeta"
                    Rate_eqtn_prototype = f"f_LV*(Q_CSF + Qglymph)"
                case ['TFV','CM']:
                    Reaction_name = f"Flow TFV to CM Abeta"
                    Rate_eqtn_prototype = f"(Q_CSF + Qglymph)"
                case ['CM','SAS']:
                    Reaction_name = f"Flow CM to SAS Abeta"
                    Rate_eqtn_prototype = f"(Q_CSF + Qglymph)"
                case ['SAS','ISF']:
                    Reaction_name = f"Flow SAS to ISF Abeta"
                    Rate_eqtn_prototype = f"Qglymph"
                case ['SAS','central']:
                    Reaction_name = f"Flow SAS to central Abeta"
                    if Species == 'AB40_O1' or Species == 'AB42_O1':
                        Rate_eqtn_prototype = f"(1 - sigma_{Comp1}_{Comp2}_Abeta)*Q_CSF"
                    else:
                        Comp2 = 'centralAntibody'
                        Rate_eqtn_prototype = f"(1 - sigma_{Comp1}_{Comp2}_Antibody)*Q_CSF"
                        Products = f"[{Species}_{Comp2}]"
                case ['BrainPlasma','central']:
                    Reaction_name = f"Flow BrainPlasma to central Abeta"
                    if Species == 'AB40_O1' or Species == 'AB42_O1':
                        Rate_eqtn_prototype = f"(Qbrain_plasma - Q_CSF - Qbrain_ISF)"
                    else:
                        Comp2 = 'centralAntibody'
                        Rate_eqtn_prototype = f"(Qbrain_plasma - Q_CSF - Qbrain_ISF)"
                        Products = f"[{Species}_{Comp2}]"
                case ['central','BrainPlasma']:
                    Reaction_name = f"Flow central to BrainPlasma Abeta"
                    if Species == 'AB40_O1' or Species == 'AB42_O1':
                        Rate_eqtn_prototype = f"Qbrain_plasma"
                    else:
                        Comp1 = 'centralAntibody'
                        Rate_eqtn_prototype = f"Qbrain_plasma"
                        Reactants = f"[{Species}_{Comp1}]"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict) 
    
    for Species in ['AB40_O1', 'AB42_O1','Antibody']:
        for Comp in [['ISF','PVS']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF" 
            Reaction_name = f"Flow ISF to PVS "
            if Species == 'AB40_O1' or Species == 'AB42_O1' :
                Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_O1) * Q_PVS"
            elif Species == 'Antibody':
                Rate_eqtn_prototype = f"(1.0 - sigma_{Comp1}_{Comp2}_Antibody) * Q_PVS"         
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict) 

    for Species in ['AB40_O1', 'AB42_O1', 'AB40_O1__Antibody', 'AB42_O1__Antibody','Antibody']:
        for Comp in ['BBB','BCSFB']:
            counter += 1
            Reaction_name = f"{Comp} Abeta Monomer/Antibody degradation "
            Reactants = f"[{Species}_{Comp}]"
            Products = f"[0]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"kdeg"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    for Species in ['AB40_O1', 'AB42_O1', 'AB40_O1__Antibody', 'AB42_O1__Antibody','Antibody']:
        for Comp in [['ISF','BBB'],['BrainPlasma','BBB'],['BrainPlasma','BCSFB'],['TFV','BCSFB'],['LV','BCSFB']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"{Comp1} to {Comp2} Abeta Monomer/Antibody degradation "
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            match Comp:
                case ['ISF','BBB']: # Valid
                    Rate_eqtn_prototype = f"CL_up_brain*fBBB*Vol_brain_ES"
                case ['BrainPlasma','BBB']: # Valid
                    Rate_eqtn_prototype = f"CL_up_brain*fBBB*Vol_brain_ES"
                case ['BrainPlasma','BCSFB']: # Valid
                    Rate_eqtn_prototype = f"CL_up_brain*(1.0 - fBBB)*Vol_brain_ES"
                case ['TFV','BCSFB']:# Valid
                    Rate_eqtn_prototype = f"(1.0 - f_LV)*CL_up_brain*(1.0 - fBBB)*Vol_brain_ES"
                case ['LV','BCSFB']:# Valid
                    Rate_eqtn_prototype = f"f_LV*CL_up_brain*(1.0 - fBBB)*Vol_brain_ES"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    for Species in ['AB40_O1__Antibody', 'AB42_O1__Antibody','Antibody']:
        for Comp in [['BBB','ISF'],['BCSFB','LV'],['BCSFB','TFV'],['BBB','BrainPlasma'],['BCSFB','BrainPlasma']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"{Comp1} to {Comp2} FCRn-mediated return "
            Reactants = f"[{Species}__FCRn_{Comp1}]"
            Products = f"[{Species}_{Comp2},FCRn_{Comp1}]"
            Rate_type = "UDF"
            match Comp:
                case ['BBB','ISF']: # Valid
                    Rate_eqtn_prototype = f"CL_up_brain*fBBB*(1.0 - FR)*Vol_brain_ES"
                case ['BCSFB','LV']: # Valid
                    Rate_eqtn_prototype = f"f_LV*CL_up_brain*(1.0 - fBBB)*(1.0 - FR)*Vol_brain_ES"
                case ['BCSFB','TFV']: # Valid
                    Rate_eqtn_prototype = f"(1.0 - f_LV)*CL_up_brain*(1.0 - fBBB)*(1.0 - FR)*Vol_brain_ES"
                case ['BBB','BrainPlasma']: # Valid
                    Rate_eqtn_prototype = f"CL_up_brain*fBBB*FR*Vol_brain_ES"
                case ['BCSFB','BrainPlasma']: # Valid
                    Rate_eqtn_prototype = f"CL_up_brain*(1.0 - fBBB)*FR*Vol_brain_ES"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    for Species in ['AB40_O1__Antibody', 'AB42_O1__Antibody','Antibody']:
        for Comp in ['BBB','BCSFB']:
            counter += 1
            Reaction_name = f"{Comp} Binding to FCRn"
            Reactants = f"[{Species}_{Comp},FCRn_{Comp}]"
            Products = f"[{Species}__FCRn_{Comp}]"
            Rate_type = "RMA"
            Rate_eqtn_prototype = f"[kon_FCRn,koff_FCRn]"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    for Species in ['AB40_O1', 'AB42_O1']:
        for Comp in ['central']:
            counter += 1
            Reaction_name = f"central clearance 1"
            Reactants = f"[{Species}_{Comp}]"
            Products = f"[0]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"AB_O1_CL"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    for Species in ['AB40_O1__Antibody', 'AB42_O1__Antibody','Antibody']:
        for Comp in ['centralAntibody']:
            counter += 1
            Reaction_name = f"centralAntibody clearance 1"
            Reactants = f"[{Species}_{Comp}]"
            Products = f"[0]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"Antibody_CL"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    for Species in ['AB40_O1', 'AB42_O1']:
        for Comp in [['central','peripheral'],['peripheral','central']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"central clearance 2"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"AB_O1_CLd2"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    for Species in ['AB40_O1__Antibody', 'AB42_O1__Antibody','Antibody']:
        for Comp in [['centralAntibody','peripheralAntibody'],['peripheralAntibody','centralAntibody']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"central clearance 2"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"Antibody_CLd2"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    for Species in ['Antibody']:
        for Comp in [['SubCutComp','centralAntibody']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Subcutaneous compartment transport"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            Rate_eqtn_prototype = f"SubCut_ka*V_SubCutComp*SubCut_bioavailability"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    for Species in ['Antibody']:
        for Comp in ['SubCutComp']:
            counter += 1
            Reaction_name = f"Subcutaneous clearance"
            Reactants = f"[{Species}_{Comp}]"
            Products = f"[0]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f"SubCut_ka*(1.0 - SubCut_bioavailability)"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

    print(counter)
    return all_reactions



all_reactions = build_reactions()

with open("Geerts_all_reactions.txt", "w", encoding="utf-8") as f:
    for reaction in all_reactions:
        f.write(str(reaction) + "\n")

# print(all_reactions)


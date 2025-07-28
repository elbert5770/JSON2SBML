

def build_reactions():
    all_reactions = []
    counter = 0
    
    

    ['TissueVascular','Plasma'],
         ['Plasma','TissueVascular'],
         ['Plasma','BrainVascular'],
         ['BrainVascular','Plasma'],
         ['Plasma','Lymph'],
         ['Lymph','Plasma'],

         
         ['TissueInterstitial','Lymph'],
         ['BrainVascular','BrainISF'],
         ['BrainISF','CSF'],
         ['CSF','BrainISF',
         ['BrainVascular','CSF'],
         ['CSF','Lymph'],
# Module Tissue
    for Species in ['Antibody']:
        for Comp in [ ['TissueVascular','TissueInterstitial'],
        ['TissueVascular','TissueEndosomal'],
        ['TissueInterstitial','TissueEndosomal']
         ]:      
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Flow within tissue"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            match Comp:
                case ['TissueVascular','TissueInterstitial']: 
                    Rate_eqtn_prototype = f"(1-RC_{Comp1}) * L_T"
                case ['TissueVascular','TissueEndosomal']: 
                    Rate_eqtn_prototype = f"CLup_Tissue"
                case ['TissueInterstitial','TissueEndosomal']: 
                    Rate_eqtn_prototype = f"CLup_Tissue"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    
        for Comp in  ['TissueEndosomal']:
         
            counter += 2
            Reaction_name = f"TissueEndosomal reactions"
            Reactants = f"[{Species}_{Comp},{FCRn_{Comp}}]"
            Products = f"[{Species}__FCRn_{Comp}]"
            Rate_type = "RMA"
            Rate_eqtn_prototype = f["Kon_FcRn","Koff_FcRn"]
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"TissueEndosomal reactions"
            Reactants = f"[{Species}_{Comp}]"
            Products = f"[0]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f["Kdeg"]
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

        for Comp in [ ['TissueEndosomal','TissueVascular'],
            ['TissueEndosomal','TissueInterstitial']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Flow out of endosomal"
            Reactants = f"[{Species}__FCRn_{Comp1}]"
            Products = f"[{Species}_{Comp2},FCRn_{Comp1}]"
            Rate_type = "UDF"
            match Comp:
                case  ['TissueEndosomal','TissueVascular']: 
                    Rate_eqtn_prototype = f"CLup_Tissue * FR"
                case  ['TissueEndosomal','TissueInterstitial']: 
                    Rate_eqtn_prototype = f"CLup_Tissue * (1 - FR)"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)

 # Inter module flow
        for Comp in [ ['Plasma','TissueVascular'],
            ['TissueVascular','Plasma'],
            ['Plasma','BrainVascular'],
         ['BrainVascular','Plasma'],
         ['Lymph','Plasma'],
         ['TissueInterstitial','Lymph'],
         ['CSF','Lymph'],
         ['BrainISF','Lymph']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Flow between modules"
            Reactants = f"[{Species}_{Comp1}]"
            Products = f"[{Species}_{Comp2}]"
            Rate_type = "UDF"
            match Comp:
                case  ['Plasma','TissueVascular']: 
                    Rate_eqtn_prototype = f"QT"
                case  ['TissueVascular','Plasma']: 
                    Rate_eqtn_prototype = f"(QT - LT)"
                case  ['Plasma','BrainVascular']: 
                    Rate_eqtn_prototype = f"QB"
                case  ['BrainVascular','Plasma']: 
                    Rate_eqtn_prototype = f"(QB - LB)"
                case   ['Lymph','Plasma']: 
                    Rate_eqtn_prototype = f"(LT + LB)"  
                case   ['TissueInterstitial','Lymph']: 
                    Rate_eqtn_prototype = f"(1 - RC_Tv) * LT" 
                case   ['CSF','Lymph']: 
                    Rate_eqtn_prototype = f"(1-RC_CSF) * (QB_CSF)" 
                case   ['BrainISF','Lymph']: 
                    Rate_eqtn_prototype = f"(1-RC_B_ISF) * QB_ECF" 


    # Module CNS

        for Comp in [ ['BrainVascular','BrainISF'],
        ['BrainVascular','BBB'],
        ['BrainVascular','BCSFB'],
        ['BrainVascular','CSF'],
        ['BrainISF','CSF'],
        ['CSF','BrainISF'],
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
                    Rate_eqtn_prototype = f"(1-RC_BBB) * Q_BECF"
                case ['BrainVascular','BBB']: 
                    Rate_eqtn_prototype = f"CLup_BBB"
                case ['BrainVascular','BCSFB']: 
                    Rate_eqtn_prototype = f"CLup_BCSFB"
                case ['BrainVascular','CSF']: 
                    Rate_eqtn_prototype = f"(1-RC_BCSFB) * Q_BCSF"
                case ['BrainISF','CSF']: 
                    Rate_eqtn_prototype = f"QB_ECF"
                case ['CSF','BrainISF']: 
                    Rate_eqtn_prototype = f"QB_ECF"



            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)
    
    
        for Comp in  ['BBB','BCSFB']:
         
            counter += 2
            Reaction_name = f"BrainEndosomal reactions"
            Reactants = f"[{Species}_{Comp},{FCRn_{Comp}}]"
            Products = f"[{Species}__FCRn_{Comp}]"
            Rate_type = "RMA"
            Rate_eqtn_prototype = f["Kon_FcRn","Koff_FcRn"]
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

            counter += 1
            Reaction_name = f"BrainEndosomal degradation"
            Reactants = f"[{Species}_{Comp}]"
            Products = f"[0]"
            Rate_type = "MA"
            Rate_eqtn_prototype = f["Kdeg"]
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,}
            all_reactions.append(Reaction_dict)

        for Comp in [ ['BBB','BrainVascular'],
            ['BBB','BrainISF'],
            ['BCSFB','BrainVascular'],
            ['BCSFB','CSF']]:
            counter += 1
            Comp1 = Comp[0]
            Comp2 = Comp[1]
            Reaction_name = f"Flow out of endosomal"
            Reactants = f"[{Species}__FCRn_{Comp1}]"
            Products = f"[{Species}_{Comp2},FCRn_{Comp1}]"
            Rate_type = "UDF"
            match Comp:
                case  ['BBB','BrainVascular']: 
                    Rate_eqtn_prototype = f"CLup_BBB * FR"
                case  ['BBB','BrainISF']: 
                    Rate_eqtn_prototype = f"CLup_BBB * (1 - FR)"
                case  ['BCSFB','BrainVascular']: 
                    Rate_eqtn_prototype = f"CLup_BBB * FR"
                case  ['BCSFB','CSF']: 
                    Rate_eqtn_prototype = f"CLup_BBB * (1 - FR)"
            Reaction_dict = {"Reaction_name": Reaction_name,"Reactants": Reactants,"Products": Products,"Rate_type": Rate_type,"Rate_eqtn_prototype": Rate_eqtn_prototype,} 
            all_reactions.append(Reaction_dict)


   

    print(counter)
    return all_reactions



all_reactions = build_reactions()

with open("Bloomingdal_all_reactions.txt", "w", encoding="utf-8") as f:
    for reaction in all_reactions:
        f.write(str(reaction) + "\n")

# print(all_reactions)

    dAntibody_Plasmadt = ((QT - LT) * Antibody_TissueVascular + (QB - LB) * Antibody_BrainVascular + 
                          (LT + LB) * Antibody_Lymph - QT * Antibody_Plasma - QB * Antibody_Plasma) / Vp

    # 2. Tissue Vascular
    dAntibody_TissueVasculardt = (QT * Antibody_Plasma - (QT - LT) * Antibody_TissueVascular - 
                                  ((1-RC_Tv) * LT * Antibody_TissueVascular) - CLUP_T * Antibody_TissueVascular + 
                                  CLUP_T * FR * Antibody__FCRn_TissueEndosomal) / V_TissueVascular

    # 3. Tissue Endosomal (Unbound)
    dAntibody_TissueEndosomaldt = (CLUP_T * (Antibody_TissueVascular + Antibody_TissueInterstitial) / V_TissueEndosomal - 
                                   Kon_FcRn * Antibody_TissueEndosomal * FCRn_TissueEndosomal + 
                                   Koff_FcRn * Antibody__FCRn_TissueEndosomal - Kdeg * Antibody_TissueEndosomal)

    # 4. Tissue Endosomal (Bound)
    dAntibody__FCRn_TissueEndosomaldt = (Kon_FcRn * Antibody_TissueEndosomal * FCRn_TissueEndosomal - 
                                         Koff_FcRn * Antibody__FCRn_TissueEndosomal - 
                                         CLUP_T * Antibody__FCRn_TissueEndosomal / V_TissueEndosomal)

    # 5. Tissue Interstitial
    dAntibody_TissueInterstitialdt = (((1-RC_Tv) * LT * Antibody_TissueVascular) - 
                                      ((1-RC_TL) * LT * Antibody_TissueInterstitial) + 
                                      (CLUP_T * (1-FR) * Antibody__FCRn_TissueEndosomal) - 
                                      CLUP_T * Antibody_TissueInterstitial) / V_TissueInterstitial

    # 6. Brain Vascular
    dAntibody_BrainVasculardt = (QB * Antibody_Plasma - (QB-LB) * Antibody_BrainVascular - 
                                 ((1-RC_BBB) * QB_ECF * Antibody_BrainVascular) - 
                                 ((1-RC_BCSFB) * QB_CSF * Antibody_BrainVascular) -
                                 (CLUP_B * Antibody_BrainVascular) + 
                                 (CLUP_BBB * FR_B * Antibody__FCRn_EBBB) + 
                                 (CLUP_BCSFB * FR_B * Antibody__FCRn_EBCSFB)) / V_BrainVascular

    # 7. Endosomal BBB (Unbound)
    dAntibody_EBBBdt = ((CLUP_BBB * (Antibody_BrainVascular + Antibody_BrainISF)) / V_EBBB) - Kon_FcRn * Antibody_EBBB * FCRn_EBBB + Koff_FcRn * Antibody__FCRn_EBBB - Kdeg * Antibody_EBBB

    # 8. Endosomal BBB (Bound)
    dAntibody__FCRn_EBBBdt = (Kon_FcRn * Antibody_EBBB * FCRn_EBBB - Koff_FcRn * Antibody__FCRn_EBBB - (CLUP_BBB * Antibody__FCRn_EBBB) / V_EBBB)

    # 9. Brain Interstitial (ISF)
    dAntibody_BrainISFdt = (((1-RC_BBB) * QB_ECF * Antibody_BrainVascular) - ((1-RC_B_ISF) * QB_ECF * Antibody_BrainISF) + (CLUP_BBB * (1-FR_B) * Antibody__FCRn_EBBB) - (CLUP_BBB * Antibody_BrainISF) - (QB_ECF * Antibody_BrainISF) + (QB_ECF * Antibody_CSF)) / V_BrainISF

    # 10. Endosomal BCSFB (Unbound)
    dAntibody_EBCSFBdt = ((CLUP_BCSFB * Antibody_BrainVascular + CLUP_BCSFB * Antibody_CSF) / V_EBCSFB - Kon_FcRn * Antibody_EBCSFB * FCRn_EBCSFB + Koff_FcRn * Antibody__FCRn_EBCSFB - Kdeg * Antibody_EBCSFB)

    # 11. Endosomal BCSFB (Bound)
    dAntibody__FCRn_EBCSFBdt = (Kon_FcRn * Antibody_EBCSFB * FCRn_EBCSFB - (Koff_FcRn * Antibody__FCRn_EBCSFB) - ((CLUP_BCSFB * Antibody__FCRn_EBCSFB) / V_EBCSFB))

    # 12. Cerebrospinal Fluid (CSF)
    dAntibody_CSFdt = ((1-RC_BCSFB) * QB_CSF * Antibody_BrainVascular - (CLUP_BCSFB) * Antibody_CSF + (CLUP_BCSFB) * (1 - FR_B) * Antibody__FCRn_EBCSFB + QB_ECF * Antibody_BrainISF - (1-RAntibody_CSF) * QB_CSF * Antibody_CSF - QB_ECF * Antibody_CSF) / V_CSF

    # 13. Lymph Node
    dAntibody_Lymphdt = ((1-RC_TL) * LT * Antibody_TissueInterstitial + (1-RAntibody_CSF) * (QB_CSF) * Antibody_CSF + (1-RC_B_ISF) * QB_ECF * Antibody_BrainISF - (LT+LB) * Antibody_Lymph) / V_Lymph

    # 14. FcRn Tissue (Unbound)
    dFCRn_TissueEndosomaldt = (- Kon_FcRn * Antibody_TissueEndosomal * FCRn_TissueEndosomal + Koff_FcRn * Antibody__FCRn_TissueEndosomal + CLUP_T * Antibody__FCRn_TissueEndosomal / V_TissueEndosomal)

    # 15. FcRn BBB (Unbound)
    dFCRn_EBBBdt = (- Kon_FcRn * Antibody_EBBB * FCRn_EBBB + Koff_FcRn * Antibody__FCRn_EBBB + (CLUP_BBB * Antibody__FCRn_EBBB) / V_EBBB)

    # 16. FcRn BCSFB (Unbound)
    dFCRn_EBCSFBdt = (- Kon_FcRn * Antibody_EBCSFB * FCRn_EBCSFB + Koff_FcRn * Antibody__FCRn_EBCSFB + CLUP_BCSFB * Antibody__FCRn_EBCSFB / V_EBCSFB)

    
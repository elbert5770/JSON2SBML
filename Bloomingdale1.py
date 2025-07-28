

def build_reactions():
    all_reactions = []
    counter = 0
    
    Antibody_TissueVascular

    for Species in ['Antibody']
        for Comp in [['TissueVascular','Plasma'],
         ['Plasma','TissueVascular'],
         ['Plasma','BrainVascular'],
         ['BrainVascular','Plasma'],
         ['Plasma','Lymph'],
         ['Lymph','Plasma'],
         ['TissueVascular','TissueInterstitial'],
         ['TissueInterstitial','Lymph'],
         ['BrainVascular','BrainISF'],
         ['BrainISF','CSF'],
         ['CSF','BrainISF',
         ['BrainVascular','CSF'],
         ['CSF','Lymph'],
         ]
         ]:
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

    
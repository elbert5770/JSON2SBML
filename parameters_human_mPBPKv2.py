def parameters_human_mPBPKv2():
    """
    Human Parameters for mPBPK model
    
    Returns:
        dict: Dictionary containing all physiological and drug-specific parameters
    """
    
    # Initialize parameter dictionary
    p = {}
    
    # Drug-Specific (or hybrid) Parameters
    p['Kdeg_IgG'] = 26.6          # First order degradation rate constant of FcRn unbound mAb within the endosomal space (1/h)
    p['kCLUP'] = 0.55             # Clearance uptake by the vascular endothelial cells via pinocytosis (L/h/L)
    p['BR_kCLUP'] = 0.03047       # Clearance uptake in brain compartment (L/h/L)
    p['BR_BBB_RC'] = 1            # Reflection coefficient at BBB
    p['BR_BCSFB_RC'] = 0.9974     # Reflection coefficient at BCSFB
 
    # FcRn Parameters
    p['FcRn_Conc'] = 0.4982E-04   # Concentration of FcRn in endosomal space (M)
    p['FcRn_Kon'] = 5.59E08       # Association rate constant between mAb-FcRn (1/M/h)
    p['FcRn_Koff'] = 23.85        # Dissociation rate constant between mAb-FcRn and mAb- Antigen (1/h)
    p['FR'] = 0.715               # Mab-p.FcRn.Conc fraction recycled to plasma space (-)
    p['BR_FR'] = 0.715            # Mab-p.FcRn.Conc fraction recycled to plasma space in brain (-)

    # Physiological Parameters 
    # Brain parameters
    p['BR_BBB_PSA'] = 17                  # Brain surface area(m^2)
    p['BR_CP_PSA'] = 1.7                  # Choroid plexus surface area(m^2)
    p['BR_BBB_BCSFB_FR'] = p['BR_BBB_PSA'] / (p['BR_CP_PSA'] + p['BR_BBB_PSA'])  # The fraction of BBB and BCSFB
    p['BR_LV_TFV_FR'] = 0.5               # The fraction of area of lateral ventricle (1-p.BR.LV.TFV.FR for thrid-forth ventricle)
    p['BR_EPCL_RC'] = 0                   # Reflection coefficient from intersitial space to ventricle space          
    p['BR_ISF_RC'] = 0.2                  # Reflection coefficient to lymph at intersitial space
    p['BR_SAS_RC'] = 0.2                  # Reflection coefficient to lymph at SAS 
    p['BR_SAS_ISF_RC'] = 0                # Reflection coefficient from SAS to intersitial space
    
    # Volume (L) 
    p['plasma_volume'] = 3.1258535
    p['bloodcell_volume'] = 2.5575165

    p['lung_volume_vascular'] = 0.055
    p['lung_volume_endosomal'] = 0.005
    p['lung_volume_interstitial'] = 0.3
    p['lung_volume_bloodcell'] = 0.045
    p['lung_volume_cell'] = 0.595

    p['heart_volume_vascular'] = 0.013141975
    p['heart_volume_endosomal'] = 0.00170675
    p['heart_volume_interstitial'] = 0.04881305
    p['heart_volume_bloodcell'] = 0.010752525
    p['heart_volume_cell'] = 0.2669357

    p['kidney_volume_vascular'] = 0.01824735
    p['kidney_volume_endosomal'] = 0.00165885
    p['kidney_volume_interstitial'] = 0.0497655
    p['kidney_volume_bloodcell'] = 0.01492965
    p['kidney_volume_cell'] = 0.24716865

    p['muscle_volume_vascular'] = 0.66172414
    p['muscle_volume_endosomal'] = 0.15039185
    p['muscle_volume_interstitial'] = 3.9101881
    p['muscle_volume_bloodcell'] = 0.54141066
    p['muscle_volume_cell'] = 24.81465525

    p['skin_volume_vascular'] = 0.127471916
    p['skin_volume_endosomal'] = 0.0170417
    p['skin_volume_interstitial'] = 1.1247522
    p['skin_volume_bloodcell'] = 0.104295204
    p['skin_volume_cell'] = 2.03477898

    # Brain
    p['brain_volume_vascular'] = 0.03189736
    p['brain_volume_endosomal'] = 0.0072494
    p['brain_volume_interstitial'] = 0.2609784
    p['brain_volume_bloodcell'] = 0.02609784
    p['brain_volume_cell'] = 1.123657
    p['brain_volume_BBB'] = p['BR_BBB_BCSFB_FR'] * p['brain_volume_endosomal']
    p['brain_volume_BCSFB'] = (1 - p['BR_BBB_BCSFB_FR']) * p['brain_volume_endosomal']
    p['brain_volume_whole'] = (p['brain_volume_vascular'] + p['brain_volume_endosomal'] + 
                              p['brain_volume_interstitial'] + p['brain_volume_bloodcell'] + p['brain_volume_cell'])

    p['CSF_volume_Lventricle'] = 0.0225
    p['CSF_volume_TFventricle'] = 0.0225
    p['CSF_volume_cisterna'] = 0.0075
    p['CSF_volume_SAS'] = 0.09
    p['CSF_volume_total'] = (p['CSF_volume_Lventricle'] + p['CSF_volume_TFventricle'] + 
                            p['CSF_volume_cisterna'] + p['CSF_volume_SAS'])

    p['adipose_volume_vascular'] = 0.14812006
    p['adipose_volume_endosomal'] = 0.0673273
    p['adipose_volume_interstitial'] = 2.2891282
    p['adipose_volume_bloodcell'] = 0.12118914
    p['adipose_volume_cell'] = 10.8396953

    p['thymus_volume_vascular'] = 0.00035255
    p['thymus_volume_endosomal'] = 0.00003205
    p['thymus_volume_interstitial'] = 0.0010897
    p['thymus_volume_bloodcell'] = 0.00028845
    p['thymus_volume_cell'] = 0.00464725

    p['Sintestine_volume_vascular'] = 0.006146492
    p['Sintestine_volume_endosomal'] = 0.0019268
    p['Sintestine_volume_interstitial'] = 0.06705264
    p['Sintestine_volume_bloodcell'] = 0.005028948
    p['Sintestine_volume_cell'] = 0.30520512

    p['Lintestine_volume_vascular'] = 0.008736214
    p['Lintestine_volume_endosomal'] = 0.002738625
    p['Lintestine_volume_interstitial'] = 0.09530415
    p['Lintestine_volume_bloodcell'] = 0.007147811
    p['Lintestine_volume_cell'] = 0.4337982

    p['spleen_volume_vascular'] = 0.02679545
    p['spleen_volume_endosomal'] = 0.00110725
    p['spleen_volume_interstitial'] = 0.04429
    p['spleen_volume_bloodcell'] = 0.02192355
    p['spleen_volume_cell'] = 0.12733375

    p['pancreas_volume_vascular'] = 0.0056969
    p['pancreas_volume_endosomal'] = 0.0005179
    p['pancreas_volume_interstitial'] = 0.01802292
    p['pancreas_volume_bloodcell'] = 0.0046611
    p['pancreas_volume_cell'] = 0.07468118

    p['liver_volume_vascular'] = 0.182669438
    p['liver_volume_endosomal'] = 0.01071375
    p['liver_volume_interstitial'] = 0.42855
    p['liver_volume_bloodcell'] = 0.149456813
    p['liver_volume_cell'] = 1.37136

    p['bone_volume_vascular'] = 0.22361966
    p['bone_volume_endosomal'] = 0.05082265
    p['bone_volume_interstitial'] = 1.89060258
    p['bone_volume_bloodcell'] = 0.18296154
    p['bone_volume_cell'] = 7.81652357

    p['other_volume_vascular'] = 0.203688439
    p['other_volume_endosomal'] = 0.02425825
    p['other_volume_interstitial'] = 0.831249367
    p['other_volume_bloodcell'] = 0.166654178
    p['other_volume_cell'] = 3.625799767

    p['lymph_volume'] = 0.27427

    # Total Volumes (L)
    p['tissue_volume_vascular'] = (p['lung_volume_vascular'] + p['heart_volume_vascular'] + p['kidney_volume_vascular'] +
                                  p['muscle_volume_vascular'] + p['skin_volume_vascular'] + p['adipose_volume_vascular'] +
                                  p['thymus_volume_vascular'] + p['Sintestine_volume_vascular'] + p['Lintestine_volume_vascular'] +
                                  p['spleen_volume_vascular'] + p['pancreas_volume_vascular'] + p['liver_volume_vascular'] +
                                  p['bone_volume_vascular'] + p['other_volume_vascular'])

    p['tissue_volume_endosomal'] = (p['lung_volume_endosomal'] + p['heart_volume_endosomal'] + p['kidney_volume_endosomal'] +
                                   p['muscle_volume_endosomal'] + p['skin_volume_endosomal'] + p['adipose_volume_endosomal'] +
                                   p['thymus_volume_endosomal'] + p['Sintestine_volume_endosomal'] + p['Lintestine_volume_endosomal'] +
                                   p['spleen_volume_endosomal'] + p['pancreas_volume_endosomal'] + p['liver_volume_endosomal'] +
                                   p['bone_volume_endosomal'] + p['other_volume_endosomal'])

    p['tissue_volume_interstitial'] = (p['lung_volume_interstitial'] + p['heart_volume_interstitial'] + p['kidney_volume_interstitial'] +
                                      p['muscle_volume_interstitial'] + p['skin_volume_interstitial'] + p['adipose_volume_interstitial'] +
                                      p['thymus_volume_interstitial'] + p['Sintestine_volume_interstitial'] + p['Lintestine_volume_interstitial'] +
                                      p['spleen_volume_interstitial'] + p['pancreas_volume_interstitial'] + p['liver_volume_interstitial'] +
                                      p['bone_volume_interstitial'] + p['other_volume_interstitial'])

    p['tissue_volume_bloodcell'] = (p['lung_volume_bloodcell'] + p['heart_volume_bloodcell'] + p['kidney_volume_bloodcell'] +
                                   p['muscle_volume_bloodcell'] + p['skin_volume_bloodcell'] + p['adipose_volume_bloodcell'] +
                                   p['thymus_volume_bloodcell'] + p['Sintestine_volume_bloodcell'] + p['Lintestine_volume_bloodcell'] +
                                   p['spleen_volume_bloodcell'] + p['pancreas_volume_bloodcell'] + p['liver_volume_bloodcell'] +
                                   p['bone_volume_bloodcell'] + p['other_volume_bloodcell'])

    p['tissue_volume_cell'] = (p['lung_volume_cell'] + p['heart_volume_cell'] + p['kidney_volume_cell'] +
                              p['muscle_volume_cell'] + p['skin_volume_cell'] + p['adipose_volume_cell'] +
                              p['thymus_volume_cell'] + p['Sintestine_volume_cell'] + p['Lintestine_volume_cell'] +
                              p['spleen_volume_cell'] + p['pancreas_volume_cell'] + p['liver_volume_cell'] +
                              p['bone_volume_cell'] + p['other_volume_cell'])

    p['tissue_volume_total'] = (p['tissue_volume_vascular'] + p['tissue_volume_endosomal'] +
                               p['tissue_volume_interstitial'] + p['tissue_volume_bloodcell'] + p['tissue_volume_cell'])

    p['Total_Volume'] = (p['plasma_volume'] + p['tissue_volume_vascular'] + p['tissue_volume_endosomal'] +
                        p['tissue_volume_interstitial'] + p['brain_volume_vascular'] + p['brain_volume_endosomal'] +
                        p['brain_volume_interstitial'] + p['CSF_volume_total'] + p['lymph_volume'])

    p['Total_Volume_Brain'] = (p['brain_volume_vascular'] + p['brain_volume_endosomal'] + p['brain_volume_interstitial'] +
                              p['CSF_volume_total'])

    # Flows (L/h) 
    p['brain_flow_plasma'] = 21.4533
    p['CSF_flow_total'] = 0.024  
    p['ECF_flow_total'] = 0.0105 

    p['lung_flow_plasma'] = 181.9125

    p['tissue_flow_plasma'] = p['lung_flow_plasma'] - p['brain_flow_plasma']

    p['tissue_flow_lymph'] = p['tissue_flow_plasma'] * 0.002

    p['brain_flow_lymph'] = p['CSF_flow_total'] + p['ECF_flow_total']

    # Reflection coefficient 
    p['physiol_RC_tight'] = 0.95
    p['physiol_RC_medium'] = 0.9
    p['physiol_RC_loose'] = 0.85
    p['heart_RC_vascular'] = p['physiol_RC_tight']
    p['kidney_RC_vascular'] = p['physiol_RC_medium']
    p['muscle_RC_vascular'] = p['physiol_RC_tight']
    p['skin_RC_vascular'] = p['physiol_RC_tight']
    p['adipose_RC_vascular'] = p['physiol_RC_tight']
    p['thymus_RC_vascular'] = p['physiol_RC_medium']
    p['Sintestine_RC_vascular'] = p['physiol_RC_medium']
    p['Lintestine_RC_vascular'] = p['physiol_RC_tight']
    p['spleen_RC_vascular'] = p['physiol_RC_loose']
    p['pancreas_RC_vascular'] = p['physiol_RC_medium']
    p['liver_RC_vascular'] = p['physiol_RC_loose']
    p['bone_RC_vascular'] = p['physiol_RC_loose']
    p['other_RC_vascular'] = p['physiol_RC_tight']
    p['lung_RC_vascular'] = p['physiol_RC_tight']

    p['tissue_RC_vascular'] = ((p['lung_RC_vascular'] * p['lung_volume_vascular'] +
                               p['heart_RC_vascular'] * p['heart_volume_vascular'] +
                               p['kidney_RC_vascular'] * p['kidney_volume_vascular'] +
                               p['muscle_RC_vascular'] * p['muscle_volume_vascular'] +
                               p['skin_RC_vascular'] * p['skin_volume_vascular'] +
                               p['adipose_RC_vascular'] * p['adipose_volume_vascular'] +
                               p['thymus_RC_vascular'] * p['thymus_volume_vascular'] +
                               p['Sintestine_RC_vascular'] * p['Sintestine_volume_vascular'] +
                               p['Lintestine_RC_vascular'] * p['Lintestine_volume_vascular'] +
                               p['spleen_RC_vascular'] * p['spleen_volume_vascular'] +
                               p['pancreas_RC_vascular'] * p['pancreas_volume_vascular'] +
                               p['liver_RC_vascular'] * p['liver_volume_vascular'] +
                               p['bone_RC_vascular'] * p['bone_volume_vascular'] +
                               p['other_RC_vascular'] * p['other_volume_vascular']) / p['tissue_volume_vascular'])

    p['tissue_RC_lymph'] = 0.2

    return p


# Example usage:
if __name__ == "__main__":
    # Get the parameters
    params = parameters_human_mPBPKv2()
    
    # Print some key parameters as an example
    print("Key Parameters:")
    print(f"Plasma Volume: {params['plasma_volume']} L")
    print(f"Brain Flow Plasma: {params['brain_flow_plasma']} L/h")
    print(f"Total Volume: {params['Total_Volume']} L")
    print(f"Total Brain Volume: {params['Total_Volume_Brain']} L")
    print(f"FcRn Concentration: {params['FcRn_Conc']} M") 
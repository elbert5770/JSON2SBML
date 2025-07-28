import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class ModelOutput:
    """Container for model output concentrations"""
    Plasma: np.ndarray
    BrainISF: np.ndarray
    BrainCSF: np.ndarray
    BrainHomo: np.ndarray
    time: np.ndarray

def mPBPKv2(DoseIV: float, Frequency: float, NumDoses: int, Stepsize: float, p: Dict) -> ModelOutput:
    """
    Minimal Brain PBPK Model: Equations and Solver
    
    Args:
        DoseIV: Initial dose (nmol)
        Frequency: Dosing frequency (hours)
        NumDoses: Number of doses
        Stepsize: Time step size (hours)
        p: Parameter dictionary
    
    Returns:
        ModelOutput: Object containing concentration time courses
    """
    
    # Redefine Parameter Names for Equation Simplicity
    Kdeg = p['Kdeg_IgG']              # First order degradation rate of antibody in endosome (1/h)
    FR = p['FR']                      # Fraction of antibody recycled to plasma space (-)
    FR_B = p['BR_FR']                 # Fraction of antibody recycled to plasma space from brain (-)
    Kon_FcRn = p['FcRn_Kon']          # Association rate constant between antibody and FcRn (1/M/h)
    Koff_FcRn = p['FcRn_Koff']        # Dissociation rate constant of antibody_FcRn complex (1/h)
    kCLUP = p['kCLUP']                # Tissue clearance uptake rate by the vascular endothelial cells (1/h)
    BR_kCLUP = p['BR_kCLUP']          # Brain clearance uptake rate by the vascular endothelial cells (1/h)

    Vp = p['plasma_volume']                   # Plasma Volume (L)
    V_TissueVascular = p['tissue_volume_vascular']         # Tissue Vascular Volume (L)
    V_TissueEndosomal = p['tissue_volume_endosomal']        # Tissue Endosomal Volume (L)
    V_TissueInterstitial = p['tissue_volume_interstitial']     # Tissue Interstitial Volume (L)
    V_BrainVascular = p['brain_volume_vascular']          # Brain Vascular Volume (L)
    V_EBBB = p['brain_volume_BBB']           # Brain Endosomal Volume of BBB (L)
    V_BCSFB = p['brain_volume_BCSFB']       # Brain Endosomal Volume of BCSFB (L)
    V_BrainISF = p['brain_volume_interstitial']      # Brain Interstitial Volume (L)
    V_CSF = p['CSF_volume_total']             # Brain CSF Volume (L)
    V_Lymph = p['lymph_volume']                    # Lymph Volume
    V_CSF_LV = p['CSF_volume_Lventricle']      # Lateral Ventricle CSF Volume (L)    
    V_CSF_TFV = p['CSF_volume_TFventricle']    # Third + Fourth Ventricle CSF Volume (L) 
    VB_total = p['brain_volume_whole']        # Total Brain Volume (L) 

    QT = p['tissue_flow_plasma']      # Tissue Flow (L/h)
    QB = p['brain_flow_plasma']       # Brain Flow (L/h)
    LT = p['tissue_flow_lymph']       # Lymph Flow from Tissues (L/h)
    LB = p['brain_flow_lymph']        # Lymph Flow from Brain (L/h) * Note: LB = QB_ECF + QB_CSF
    QB_ECF = p['ECF_flow_total']      # Brain Interstitial Fluid (or Extracellular Fluid) Flow (L/h)
    QB_CSF = p['CSF_flow_total']      # Brain CSF Flow (L/h)

    RC_Tv = p['tissue_RC_vascular']   # Tissue Vascular Reflection Coefficient (-)
    RC_TL = p['tissue_RC_lymph']      # Tissue Lymphatic Reflection Coefficient (-)
    RC_BBB = p['BR_BBB_RC']           # BBB Reflection Coefficient (-)
    RC_BCSFB = p['BR_BCSFB_RC']       # BBB Reflection Coefficient (-)
    RC_B_ISF = p['BR_ISF_RC']         # ISF Glymphatic Reflection Coefficient (-)
    RC_CSF = p['BR_SAS_RC']         # CSF Glymphatic Reflection Coefficient (-)

    CLUP_T = p['kCLUP'] * p['tissue_volume_endosomal']                                     # Tissue clearance uptake by the vascular endothelial cells (L/h)
    CLUP_BCSFB = p['BR_kCLUP'] * p['brain_volume_endosomal'] * (1 - p['BR_BBB_BCSFB_FR'])   # BCSFB clearance uptake by epithelial cells (L/h)
    CLUP_BBB = p['BR_kCLUP'] * p['brain_volume_endosomal'] * p['BR_BBB_BCSFB_FR']           # BBB clearance uptake by the vascular endothelial cells (L/h)
    CLUP_B = p['BR_kCLUP'] * p['brain_volume_endosomal']                                 # Total brain clearance uptake by the vascular endothelial cells (L/h)

    # Introduce dose into the initial condition
    yIV = DoseIV / Vp / (1e9)  # (Convert amount initial condition(nmol) to Conc (M))

    # Set Initial Conditions
    yinitial = np.zeros(16)
    yinitial[13] = p['FcRn_Conc']  # Tissue
    yinitial[14] = p['FcRn_Conc']  # BBB
    yinitial[15] = p['FcRn_Conc']  # BCSFB

    # Differential Equation Solver
    t_all = []
    y_all = []
    
    for n in range(NumDoses):
        yinitial[0] += yIV  # Add dose to plasma compartment
        tstart = n * Frequency
        tend = (n + 1) * Frequency
        
        # Create time points for this dosing interval
        t_interval = np.arange(tstart, tend + Stepsize, Stepsize)
        
        # Solve ODE for this interval
        solution = solve_ivp(
            fun=lambda t, y: modelODE(t, y, p),
            t_span=(tstart, tend),
            y0=yinitial,
            t_eval=t_interval,
            method='BDF',  # Stiff solver similar to ode15s
            rtol=1e-6,
            atol=1e-9
        )

        if not solution.success:
            raise RuntimeError(f"ODE solver failed on dose {n+1} with message: {solution.message}")
        
        t_all.extend(solution.t)
        
        # Convert solution.y to the right format
        # solution.y should be a 2D numpy array with shape (n_variables, n_timepoints)
        y_solution = np.array(solution.y).T  # Transpose to get (n_timepoints, n_variables)
        y_all.extend(y_solution.tolist())
        yinitial = y_solution[-1]  # Last time point

    # Convert to numpy arrays
    t = np.array(t_all)
    y = np.array(y_all)

    # Model Output (nM)
    Conc = ModelOutput(
        Plasma=y[:, 0] * 1e9,
        BrainISF=y[:, 8] * 1e9,
        BrainCSF=y[:, 11] * 1e9,
        BrainHomo=(y[:, 6] * V_EBBB + y[:, 7] * V_EBBB + y[:, 8] * V_BrainISF + 
                   y[:, 9] * V_BCSFB + y[:, 10] * V_BCSFB +
                   (y[:, 11] * (V_CSF_LV + V_CSF_TFV))) / (VB_total + V_CSF_LV + V_CSF_TFV) * 1e9,
        time=t
    )
    
    return Conc


def modelODE(t: float, y: np.ndarray, p: Dict) -> np.ndarray:
    """
    Model differential equations
    
    Args:
        t: Time (hours)
        y: State vector (16 elements)
        p: Parameter dictionary
    
    Returns:
        np.ndarray: Derivatives of state variables
    """
    
    # Redefine Parameter Names for Equation Simplicity
    Kdeg = p['Kdeg_IgG']
    FR = p['FR']
    FR_B = p['BR_FR']
    Kon_FcRn = p['FcRn_Kon']
    Koff_FcRn = p['FcRn_Koff']
    kCLUP = p['kCLUP']
    BR_kCLUP = p['BR_kCLUP']

    Vp = p['plasma_volume']
    V_TissueVascular = p['tissue_volume_vascular']
    V_TissueEndosomal = p['tissue_volume_endosomal']
    V_TissueInterstitial = p['tissue_volume_interstitial']
    V_BrainVascular = p['brain_volume_vascular']
    V_EBBB = p['brain_volume_BBB']
    V_BCSFB = p['brain_volume_BCSFB']
    V_BrainISF = p['brain_volume_interstitial']
    V_CSF = p['CSF_volume_total']
    V_Lymph = p['lymph_volume']

    QT = p['tissue_flow_plasma']
    QB = p['brain_flow_plasma']
    LT = p['tissue_flow_lymph']
    LB = p['brain_flow_lymph']
    QB_ECF = p['ECF_flow_total']
    QB_CSF = p['CSF_flow_total']

    RC_Tv = p['tissue_RC_vascular']
    RC_TL = p['tissue_RC_lymph']
    RC_BBB = p['BR_BBB_RC']
    RC_BCSFB = p['BR_BCSFB_RC']
    RC_B_ISF = p['BR_ISF_RC']
    RC_CSF = p['BR_SAS_RC']

    CLUP_T = p['kCLUP'] * p['tissue_volume_endosomal']
    CLUP_BCSFB = p['BR_kCLUP'] * p['brain_volume_endosomal'] * (1 - p['BR_BBB_BCSFB_FR'])
    CLUP_BBB = p['BR_kCLUP'] * p['brain_volume_endosomal'] * p['BR_BBB_BCSFB_FR']
    CLUP_B = p['BR_kCLUP'] * p['brain_volume_endosomal']

    # Compartments
    Antibody_Plasma = y[0]
    Antibody_TissueVascular = y[1]
    Antibody_TissueEndosomal = y[2]
    Antibody__FCRn_TissueEndosomal = y[3]
    Antibody_TissueInterstitial = y[4]
    Antibody_BrainVascular = y[5]
    Antibody_EBBB = y[6]
    Antibody__FCRn_EBBB = y[7]
    Antibody_BrainISF = y[8]
    Antibody_BCSFB = y[9]
    Antibody__FCRn_BCSFB = y[10]
    Antibody_CSF = y[11]
    Antibody_Lymph = y[12]
    FCRn_TissueEndosomal = y[13]
    FCRn_EBBB = y[14]
    FCRn_BCSFB = y[15]

    # Differential Equations
    # 1. Plasma
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
                                 (CLUP_BCSFB * FR_B * Antibody__FCRn_BCSFB)) / V_BrainVascular

    # 7. Endosomal BBB (Unbound)
    dAntibody_EBBBdt = ((CLUP_BBB * (Antibody_BrainVascular + Antibody_BrainISF)) / V_EBBB) - Kon_FcRn * Antibody_EBBB * FCRn_EBBB + Koff_FcRn * Antibody__FCRn_EBBB - Kdeg * Antibody_EBBB

    # 8. Endosomal BBB (Bound)
    dAntibody__FCRn_EBBBdt = (Kon_FcRn * Antibody_EBBB * FCRn_EBBB - Koff_FcRn * Antibody__FCRn_EBBB - (CLUP_BBB * Antibody__FCRn_EBBB) / V_EBBB)

    # 9. Brain Interstitial (ISF)
    dAntibody_BrainISFdt = (((1-RC_BBB) * QB_ECF * Antibody_BrainVascular) - ((1-RC_B_ISF) * QB_ECF * Antibody_BrainISF) + (CLUP_BBB * (1-FR_B) * Antibody__FCRn_EBBB) - (CLUP_BBB * Antibody_BrainISF) - (QB_ECF * Antibody_BrainISF) + (QB_ECF * Antibody_CSF)) / V_BrainISF

    # 10. Endosomal BCSFB (Unbound)
    dAntibody_BCSFBdt = ((CLUP_BCSFB * Antibody_BrainVascular + CLUP_BCSFB * Antibody_CSF) / V_BCSFB - Kon_FcRn * Antibody_BCSFB * FCRn_BCSFB + Koff_FcRn * Antibody__FCRn_BCSFB - Kdeg * Antibody_BCSFB)

    # 11. Endosomal BCSFB (Bound)
    dAntibody__FCRn_BCSFBdt = (Kon_FcRn * Antibody_BCSFB * FCRn_BCSFB - (Koff_FcRn * Antibody__FCRn_BCSFB) - ((CLUP_BCSFB * Antibody__FCRn_BCSFB) / V_BCSFB))

    # 12. Cerebrospinal Fluid (CSF)
    dAntibody_CSFdt = ((1-RC_BCSFB) * QB_CSF * Antibody_BrainVascular - (CLUP_BCSFB) * Antibody_CSF + (CLUP_BCSFB) * (1 - FR_B) * Antibody__FCRn_BCSFB + QB_ECF * Antibody_BrainISF - (1-RC_CSF) * QB_CSF * Antibody_CSF - QB_ECF * Antibody_CSF) / V_CSF

    # 13. Lymph Node
    dAntibody_Lymphdt = ((1-RC_TL) * LT * Antibody_TissueInterstitial + (1-RC_CSF) * (QB_CSF) * Antibody_CSF + (1-RC_B_ISF) * QB_ECF * Antibody_BrainISF - (LT+LB) * Antibody_Lymph) / V_Lymph

    # 14. FcRn Tissue (Unbound)
    dFCRn_TissueEndosomaldt = (- Kon_FcRn * Antibody_TissueEndosomal * FCRn_TissueEndosomal + Koff_FcRn * Antibody__FCRn_TissueEndosomal + CLUP_T * Antibody__FCRn_TissueEndosomal / V_TissueEndosomal)

    # 15. FcRn BBB (Unbound)
    dFCRn_EBBBdt = (- Kon_FcRn * Antibody_EBBB * FCRn_EBBB + Koff_FcRn * Antibody__FCRn_EBBB + (CLUP_BBB * Antibody__FCRn_EBBB) / V_EBBB)

    # 16. FcRn BCSFB (Unbound)
    dFCRn_BCSFBdt = (- Kon_FcRn * Antibody_BCSFB * FCRn_BCSFB + Koff_FcRn * Antibody__FCRn_BCSFB + CLUP_BCSFB * Antibody__FCRn_BCSFB / V_BCSFB)

    # Return derivatives
    return np.array([
        dAntibody_Plasmadt,
        dAntibody_TissueVasculardt,
        dAntibody_TissueEndosomaldt,
        dAntibody__FCRn_TissueEndosomaldt,
        dAntibody_TissueInterstitialdt,
        dAntibody_BrainVasculardt,
        dAntibody_EBBBdt,
        dAntibody__FCRn_EBBBdt,
        dAntibody_BrainISFdt,
        dAntibody_BCSFBdt,
        dAntibody__FCRn_BCSFBdt,
        dAntibody_CSFdt,
        dAntibody_Lymphdt,
        dFCRn_TissueEndosomaldt,
        dFCRn_EBBBdt,
        dFCRn_BCSFBdt
    ])


def plot_results(conc: ModelOutput, title: str = "mPBPK Model Results"):
    """
    Plot the model results
    
    Args:
        conc: ModelOutput object containing concentration data
        title: Plot title
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plasma concentration
    axes[0, 0].plot(conc.time, conc.Plasma, 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Time (hours)')
    axes[0, 0].set_ylabel('Concentration (nM)')
    axes[0, 0].set_title('Plasma')
    axes[0, 0].grid(True)
    
    # Brain ISF concentration
    axes[0, 1].plot(conc.time, conc.BrainISF, 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time (hours)')
    axes[0, 1].set_ylabel('Concentration (nM)')
    axes[0, 1].set_title('Brain Interstitial Fluid')
    axes[0, 1].grid(True)
    
    # Brain CSF concentration
    axes[1, 0].plot(conc.time, conc.BrainCSF, 'g-', linewidth=2)
    axes[1, 0].set_xlabel('Time (hours)')
    axes[1, 0].set_ylabel('Concentration (nM)')
    axes[1, 0].set_title('Brain CSF')
    axes[1, 0].grid(True)
    
    # Brain homogenate concentration
    axes[1, 1].plot(conc.time, conc.BrainHomo, 'm-', linewidth=2)
    axes[1, 1].set_xlabel('Time (hours)')
    axes[1, 1].set_ylabel('Concentration (nM)')
    axes[1, 1].set_title('Brain Homogenate')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.suptitle(title, y=1.02, fontsize=16)
    plt.show()


# Example usage
if __name__ == "__main__":
    # Import the parameters function
    from parameters_human_mPBPKv2 import parameters_human_mPBPKv2
    
    # Get parameters
    p = parameters_human_mPBPKv2()
    
    # Run simulation
    DoseIV = 1000  # nmol
    Frequency = 168  # hours (weekly dosing)
    NumDoses = 4
    Stepsize = 1  # hours
    
    try:
        results = mPBPKv2(DoseIV, Frequency, NumDoses, Stepsize, p)
    
        # Plot results
        plot_results(results, "mPBPK Model - Weekly Dosing")
        
        print("Simulation completed successfully!")
        print(f"Final plasma concentration: {results.Plasma[-1]:.2f} nM")
        print(f"Final brain ISF concentration: {results.BrainISF[-1]:.2f} nM")
        print(f"Final brain CSF concentration: {results.BrainCSF[-1]:.2f} nM")
    except RuntimeError as e:
        print(f"An error occurred during simulation: {e}") 
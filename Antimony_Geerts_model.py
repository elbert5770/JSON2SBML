import tellurium as te
import numpy as np
import matplotlib.pyplot as plt

r = te.loada('''
  model pathway()
  compartment BBB = V_BBB
compartment BCSFB = V_BCSFB
compartment BrainPlasma = V_BrainPlasma
compartment CM = V_CM
compartment ISF = V_ISF
compartment LV = V_LV
compartment PVS = V_PVS
compartment SAS = V_SAS
compartment TFV = V_TFV
compartment central = V_central
compartment peripheral = V_peripheral

species AB40_O10_ISF in ISF
species AB40_O10_PVS in PVS
species AB40_O10_central in central
species AB40_O11_ISF in ISF
species AB40_O11_PVS in PVS
species AB40_O11_central in central
species AB40_O12_ISF in ISF
species AB40_O12_PVS in PVS
species AB40_O12_central in central
species AB40_O13_ISF in ISF
species AB40_O13_PVS in PVS
species AB40_O13_central in central
species AB40_O14_ISF in ISF
species AB40_O14_PVS in PVS
species AB40_O14_central in central
species AB40_O15_ISF in ISF
species AB40_O15_PVS in PVS
species AB40_O15_central in central
species AB40_O16_ISF in ISF
species AB40_O16_PVS in PVS
species AB40_O16_central in central
species AB40_O17_ISF in ISF
species AB40_O17_PVS in PVS
species AB40_O17_central in central
species AB40_O18_ISF in ISF
species AB40_O18_PVS in PVS
species AB40_O18_central in central
species AB40_O19_ISF in ISF
species AB40_O19_PVS in PVS
species AB40_O19_central in central
species AB40_O1_BBB in BBB
species AB40_O1_BCSFB in BCSFB
species AB40_O1_BrainPlasma in BrainPlasma
species AB40_O1_CM in CM
species AB40_O1_ISF in ISF
species AB40_O1_LV in LV
species AB40_O1_PVS in PVS
species AB40_O1_SAS in SAS
species AB40_O1_TFV in TFV
species AB40_O1_central in central
species AB40_O1_peripheral in peripheral
species AB40_O20_ISF in ISF
species AB40_O20_PVS in PVS
species AB40_O20_central in central
species AB40_O21_ISF in ISF
species AB40_O21_PVS in PVS
species AB40_O21_central in central
species AB40_O22_ISF in ISF
species AB40_O22_PVS in PVS
species AB40_O22_central in central
species AB40_O23_ISF in ISF
species AB40_O23_PVS in PVS
species AB40_O23_central in central
species AB40_O24_ISF in ISF
species AB40_O24_PVS in PVS
species AB40_O24_central in central
species AB40_O25_ISF in ISF
species AB40_O2_ISF in ISF
species AB40_O2_PVS in PVS
species AB40_O2_central in central
species AB40_O3_ISF in ISF
species AB40_O3_PVS in PVS
species AB40_O3_central in central
species AB40_O4_ISF in ISF
species AB40_O4_PVS in PVS
species AB40_O4_central in central
species AB40_O5_ISF in ISF
species AB40_O5_PVS in PVS
species AB40_O5_central in central
species AB40_O6_ISF in ISF
species AB40_O6_PVS in PVS
species AB40_O6_central in central
species AB40_O7_ISF in ISF
species AB40_O7_PVS in PVS
species AB40_O7_central in central
species AB40_O8_ISF in ISF
species AB40_O8_PVS in PVS
species AB40_O8_central in central
species AB40_O9_ISF in ISF
species AB40_O9_PVS in PVS
species AB40_O9_central in central
species AB42_O10_ISF in ISF
species AB42_O10_PVS in PVS
species AB42_O10_central in central
species AB42_O11_ISF in ISF
species AB42_O11_PVS in PVS
species AB42_O11_central in central
species AB42_O12_ISF in ISF
species AB42_O12_PVS in PVS
species AB42_O12_central in central
species AB42_O13_ISF in ISF
species AB42_O13_PVS in PVS
species AB42_O13_central in central
species AB42_O14_ISF in ISF
species AB42_O14_PVS in PVS
species AB42_O14_central in central
species AB42_O15_ISF in ISF
species AB42_O15_PVS in PVS
species AB42_O15_central in central
species AB42_O16_ISF in ISF
species AB42_O16_PVS in PVS
species AB42_O16_central in central
species AB42_O17_ISF in ISF
species AB42_O17_PVS in PVS
species AB42_O17_central in central
species AB42_O18_ISF in ISF
species AB42_O18_PVS in PVS
species AB42_O18_central in central
species AB42_O19_ISF in ISF
species AB42_O19_PVS in PVS
species AB42_O19_central in central
species AB42_O1_BBB in BBB
species AB42_O1_BCSFB in BCSFB
species AB42_O1_BrainPlasma in BrainPlasma
species AB42_O1_CM in CM
species AB42_O1_ISF in ISF
species AB42_O1_LV in LV
species AB42_O1_PVS in PVS
species AB42_O1_SAS in SAS
species AB42_O1_TFV in TFV
species AB42_O1_central in central
species AB42_O1_peripheral in peripheral
species AB42_O20_ISF in ISF
species AB42_O20_PVS in PVS
species AB42_O20_central in central
species AB42_O21_ISF in ISF
species AB42_O21_PVS in PVS
species AB42_O21_central in central
species AB42_O22_ISF in ISF
species AB42_O22_PVS in PVS
species AB42_O22_central in central
species AB42_O23_ISF in ISF
species AB42_O23_PVS in PVS
species AB42_O23_central in central
species AB42_O24_ISF in ISF
species AB42_O24_PVS in PVS
species AB42_O24_central in central
species AB42_O25_ISF in ISF
species AB42_O2_ISF in ISF
species AB42_O2_PVS in PVS
species AB42_O2_central in central
species AB42_O3_ISF in ISF
species AB42_O3_PVS in PVS
species AB42_O3_central in central
species AB42_O4_ISF in ISF
species AB42_O4_PVS in PVS
species AB42_O4_central in central
species AB42_O5_ISF in ISF
species AB42_O5_PVS in PVS
species AB42_O5_central in central
species AB42_O6_ISF in ISF
species AB42_O6_PVS in PVS
species AB42_O6_central in central
species AB42_O7_ISF in ISF
species AB42_O7_PVS in PVS
species AB42_O7_central in central
species AB42_O8_ISF in ISF
species AB42_O8_PVS in PVS
species AB42_O8_central in central
species AB42_O9_ISF in ISF
species AB42_O9_PVS in PVS
species AB42_O9_central in central
species APP_ISF in ISF
species C99_ISF in ISF

AB40_O1_ISF + AB40_O1_ISF -> AB40_O2_ISF; k_O1_O2_AB40_ISF * AB40_O1_ISF * AB40_O1_ISF * V_ISF
AB40_O2_ISF -> AB40_O1_ISF + AB40_O1_ISF; k_O2_O1_AB40_ISF * AB40_O2_ISF * V_ISF
AB40_O2_ISF + AB40_O1_ISF -> AB40_O3_ISF; k_O2_O3_AB40_ISF * AB40_O2_ISF * AB40_O1_ISF * V_ISF
AB40_O3_ISF -> AB40_O2_ISF + AB40_O1_ISF; k_O3_O2_AB40_ISF * AB40_O3_ISF * V_ISF
AB40_O3_ISF + AB40_O1_ISF -> AB40_O4_ISF; k_O3_O4_AB40_ISF * AB40_O3_ISF * AB40_O1_ISF * V_ISF
AB40_O4_ISF -> AB40_O3_ISF + AB40_O1_ISF; k_O4_O3_AB40_ISF * AB40_O4_ISF * V_ISF
AB40_O4_ISF + AB40_O1_ISF -> AB40_O5_ISF; k_O4_O5_AB40_ISF * AB40_O4_ISF * AB40_O1_ISF * V_ISF
AB40_O5_ISF -> AB40_O4_ISF + AB40_O1_ISF; k_O5_O4_AB40_ISF * AB40_O5_ISF * V_ISF
AB40_O5_ISF + AB40_O1_ISF -> AB40_O6_ISF; k_O5_O6_AB40_ISF * AB40_O5_ISF * AB40_O1_ISF * V_ISF
AB40_O6_ISF -> AB40_O5_ISF + AB40_O1_ISF; k_O6_O5_AB40_ISF * AB40_O6_ISF * V_ISF
AB40_O6_ISF + AB40_O1_ISF -> AB40_O7_ISF; k_O6_O7_AB40_ISF * AB40_O6_ISF * AB40_O1_ISF * V_ISF
AB40_O7_ISF -> AB40_O6_ISF + AB40_O1_ISF; k_O7_O6_AB40_ISF * AB40_O7_ISF * V_ISF
AB40_O7_ISF + AB40_O1_ISF -> AB40_O8_ISF; k_O7_O8_AB40_ISF * AB40_O7_ISF * AB40_O1_ISF * V_ISF
AB40_O8_ISF -> AB40_O7_ISF + AB40_O1_ISF; k_O8_O7_AB40_ISF * AB40_O8_ISF * V_ISF
AB40_O8_ISF + AB40_O1_ISF -> AB40_O9_ISF; k_O8_O9_AB40_ISF * AB40_O8_ISF * AB40_O1_ISF * V_ISF
AB40_O9_ISF -> AB40_O8_ISF + AB40_O1_ISF; k_O9_O8_AB40_ISF * AB40_O9_ISF * V_ISF
AB40_O9_ISF + AB40_O1_ISF -> AB40_O10_ISF; k_O9_O10_AB40_ISF * AB40_O9_ISF * AB40_O1_ISF * V_ISF
AB40_O10_ISF -> AB40_O9_ISF + AB40_O1_ISF; k_O10_O9_AB40_ISF * AB40_O10_ISF * V_ISF
AB40_O10_ISF + AB40_O1_ISF -> AB40_O11_ISF; k_O10_O11_AB40_ISF * AB40_O10_ISF * AB40_O1_ISF * V_ISF
AB40_O11_ISF -> AB40_O10_ISF + AB40_O1_ISF; k_O11_O10_AB40_ISF * AB40_O11_ISF * V_ISF
AB40_O11_ISF + AB40_O1_ISF -> AB40_O12_ISF; k_O11_O12_AB40_ISF * AB40_O11_ISF * AB40_O1_ISF * V_ISF
AB40_O12_ISF -> AB40_O11_ISF + AB40_O1_ISF; k_O12_O11_AB40_ISF * AB40_O12_ISF * V_ISF
AB40_O12_ISF + AB40_O1_ISF -> AB40_O13_ISF; k_O12_O13_AB40_ISF * AB40_O12_ISF * AB40_O1_ISF * V_ISF
AB40_O13_ISF -> AB40_O12_ISF + AB40_O1_ISF; k_O13_O12_AB40_ISF * AB40_O13_ISF * V_ISF
AB40_O13_ISF + AB40_O1_ISF -> AB40_O14_ISF; k_O13_O14_AB40_ISF * AB40_O13_ISF * AB40_O1_ISF * V_ISF
AB40_O14_ISF -> AB40_O13_ISF + AB40_O1_ISF; k_O14_O13_AB40_ISF * AB40_O14_ISF * V_ISF
AB40_O14_ISF + AB40_O1_ISF -> AB40_O15_ISF; k_O14_O15_AB40_ISF * AB40_O14_ISF * AB40_O1_ISF * V_ISF
AB40_O15_ISF -> AB40_O14_ISF + AB40_O1_ISF; k_O15_O14_AB40_ISF * AB40_O15_ISF * V_ISF
AB40_O15_ISF + AB40_O1_ISF -> AB40_O16_ISF; k_O15_O16_AB40_ISF * AB40_O15_ISF * AB40_O1_ISF * V_ISF
AB40_O16_ISF -> AB40_O15_ISF + AB40_O1_ISF; k_O16_O15_AB40_ISF * AB40_O16_ISF * V_ISF
AB40_O16_ISF + AB40_O1_ISF -> AB40_O17_ISF; k_O16_O17_AB40_ISF * AB40_O16_ISF * AB40_O1_ISF * V_ISF
AB40_O17_ISF -> AB40_O16_ISF + AB40_O1_ISF; k_O17_O16_AB40_ISF * AB40_O17_ISF * V_ISF
AB40_O17_ISF + AB40_O1_ISF -> AB40_O18_ISF; k_O17_O18_AB40_ISF * AB40_O17_ISF * AB40_O1_ISF * V_ISF
AB40_O18_ISF -> AB40_O17_ISF + AB40_O1_ISF; k_O18_O17_AB40_ISF * AB40_O18_ISF * V_ISF
AB40_O18_ISF + AB40_O1_ISF -> AB40_O19_ISF; k_O18_O19_AB40_ISF * AB40_O18_ISF * AB40_O1_ISF * V_ISF
AB40_O19_ISF -> AB40_O18_ISF + AB40_O1_ISF; k_O19_O18_AB40_ISF * AB40_O19_ISF * V_ISF
AB40_O19_ISF + AB40_O1_ISF -> AB40_O20_ISF; k_O19_O20_AB40_ISF * AB40_O19_ISF * AB40_O1_ISF * V_ISF
AB40_O20_ISF -> AB40_O19_ISF + AB40_O1_ISF; k_O20_O19_AB40_ISF * AB40_O20_ISF * V_ISF
AB40_O20_ISF + AB40_O1_ISF -> AB40_O21_ISF; k_O20_O21_AB40_ISF * AB40_O20_ISF * AB40_O1_ISF * V_ISF
AB40_O21_ISF -> AB40_O20_ISF + AB40_O1_ISF; k_O21_O20_AB40_ISF * AB40_O21_ISF * V_ISF
AB40_O21_ISF + AB40_O1_ISF -> AB40_O22_ISF; k_O21_O22_AB40_ISF * AB40_O21_ISF * AB40_O1_ISF * V_ISF
AB40_O22_ISF -> AB40_O21_ISF + AB40_O1_ISF; k_O22_O21_AB40_ISF * AB40_O22_ISF * V_ISF
AB40_O22_ISF + AB40_O1_ISF -> AB40_O23_ISF; k_O22_O23_AB40_ISF * AB40_O22_ISF * AB40_O1_ISF * V_ISF
AB40_O23_ISF -> AB40_O22_ISF + AB40_O1_ISF; k_O23_O22_AB40_ISF * AB40_O23_ISF * V_ISF
AB40_O23_ISF + AB40_O1_ISF -> AB40_O24_ISF; k_O23_O24_AB40_ISF * AB40_O23_ISF * AB40_O1_ISF * V_ISF
AB40_O24_ISF -> AB40_O23_ISF + AB40_O1_ISF; k_O24_O23_AB40_ISF * AB40_O24_ISF * V_ISF
AB42_O1_ISF + AB42_O1_ISF -> AB42_O2_ISF; k_O1_O2_AB42_ISF * AB42_O1_ISF * AB42_O1_ISF * V_ISF
AB42_O2_ISF -> AB42_O1_ISF + AB42_O1_ISF; k_O2_O1_AB42_ISF * AB42_O2_ISF * V_ISF
AB42_O2_ISF + AB42_O1_ISF -> AB42_O3_ISF; k_O2_O3_AB42_ISF * AB42_O2_ISF * AB42_O1_ISF * V_ISF
AB42_O3_ISF -> AB42_O2_ISF + AB42_O1_ISF; k_O3_O2_AB42_ISF * AB42_O3_ISF * V_ISF
AB42_O3_ISF + AB42_O1_ISF -> AB42_O4_ISF; k_O3_O4_AB42_ISF * AB42_O3_ISF * AB42_O1_ISF * V_ISF
AB42_O4_ISF -> AB42_O3_ISF + AB42_O1_ISF; k_O4_O3_AB42_ISF * AB42_O4_ISF * V_ISF
AB42_O4_ISF + AB42_O1_ISF -> AB42_O5_ISF; k_O4_O5_AB42_ISF * AB42_O4_ISF * AB42_O1_ISF * V_ISF
AB42_O5_ISF -> AB42_O4_ISF + AB42_O1_ISF; k_O5_O4_AB42_ISF * AB42_O5_ISF * V_ISF
AB42_O5_ISF + AB42_O1_ISF -> AB42_O6_ISF; k_O5_O6_AB42_ISF * AB42_O5_ISF * AB42_O1_ISF * V_ISF
AB42_O6_ISF -> AB42_O5_ISF + AB42_O1_ISF; k_O6_O5_AB42_ISF * AB42_O6_ISF * V_ISF
AB42_O6_ISF + AB42_O1_ISF -> AB42_O7_ISF; k_O6_O7_AB42_ISF * AB42_O6_ISF * AB42_O1_ISF * V_ISF
AB42_O7_ISF -> AB42_O6_ISF + AB42_O1_ISF; k_O7_O6_AB42_ISF * AB42_O7_ISF * V_ISF
AB42_O7_ISF + AB42_O1_ISF -> AB42_O8_ISF; k_O7_O8_AB42_ISF * AB42_O7_ISF * AB42_O1_ISF * V_ISF
AB42_O8_ISF -> AB42_O7_ISF + AB42_O1_ISF; k_O8_O7_AB42_ISF * AB42_O8_ISF * V_ISF
AB42_O8_ISF + AB42_O1_ISF -> AB42_O9_ISF; k_O8_O9_AB42_ISF * AB42_O8_ISF * AB42_O1_ISF * V_ISF
AB42_O9_ISF -> AB42_O8_ISF + AB42_O1_ISF; k_O9_O8_AB42_ISF * AB42_O9_ISF * V_ISF
AB42_O9_ISF + AB42_O1_ISF -> AB42_O10_ISF; k_O9_O10_AB42_ISF * AB42_O9_ISF * AB42_O1_ISF * V_ISF
AB42_O10_ISF -> AB42_O9_ISF + AB42_O1_ISF; k_O10_O9_AB42_ISF * AB42_O10_ISF * V_ISF
AB42_O10_ISF + AB42_O1_ISF -> AB42_O11_ISF; k_O10_O11_AB42_ISF * AB42_O10_ISF * AB42_O1_ISF * V_ISF
AB42_O11_ISF -> AB42_O10_ISF + AB42_O1_ISF; k_O11_O10_AB42_ISF * AB42_O11_ISF * V_ISF
AB42_O11_ISF + AB42_O1_ISF -> AB42_O12_ISF; k_O11_O12_AB42_ISF * AB42_O11_ISF * AB42_O1_ISF * V_ISF
AB42_O12_ISF -> AB42_O11_ISF + AB42_O1_ISF; k_O12_O11_AB42_ISF * AB42_O12_ISF * V_ISF
AB42_O12_ISF + AB42_O1_ISF -> AB42_O13_ISF; k_O12_O13_AB42_ISF * AB42_O12_ISF * AB42_O1_ISF * V_ISF
AB42_O13_ISF -> AB42_O12_ISF + AB42_O1_ISF; k_O13_O12_AB42_ISF * AB42_O13_ISF * V_ISF
AB42_O13_ISF + AB42_O1_ISF -> AB42_O14_ISF; k_O13_O14_AB42_ISF * AB42_O13_ISF * AB42_O1_ISF * V_ISF
AB42_O14_ISF -> AB42_O13_ISF + AB42_O1_ISF; k_O14_O13_AB42_ISF * AB42_O14_ISF * V_ISF
AB42_O14_ISF + AB42_O1_ISF -> AB42_O15_ISF; k_O14_O15_AB42_ISF * AB42_O14_ISF * AB42_O1_ISF * V_ISF
AB42_O15_ISF -> AB42_O14_ISF + AB42_O1_ISF; k_O15_O14_AB42_ISF * AB42_O15_ISF * V_ISF
AB42_O15_ISF + AB42_O1_ISF -> AB42_O16_ISF; k_O15_O16_AB42_ISF * AB42_O15_ISF * AB42_O1_ISF * V_ISF
AB42_O16_ISF -> AB42_O15_ISF + AB42_O1_ISF; k_O16_O15_AB42_ISF * AB42_O16_ISF * V_ISF
AB42_O16_ISF + AB42_O1_ISF -> AB42_O17_ISF; k_O16_O17_AB42_ISF * AB42_O16_ISF * AB42_O1_ISF * V_ISF
AB42_O17_ISF -> AB42_O16_ISF + AB42_O1_ISF; k_O17_O16_AB42_ISF * AB42_O17_ISF * V_ISF
AB42_O17_ISF + AB42_O1_ISF -> AB42_O18_ISF; k_O17_O18_AB42_ISF * AB42_O17_ISF * AB42_O1_ISF * V_ISF
AB42_O18_ISF -> AB42_O17_ISF + AB42_O1_ISF; k_O18_O17_AB42_ISF * AB42_O18_ISF * V_ISF
AB42_O18_ISF + AB42_O1_ISF -> AB42_O19_ISF; k_O18_O19_AB42_ISF * AB42_O18_ISF * AB42_O1_ISF * V_ISF
AB42_O19_ISF -> AB42_O18_ISF + AB42_O1_ISF; k_O19_O18_AB42_ISF * AB42_O19_ISF * V_ISF
AB42_O19_ISF + AB42_O1_ISF -> AB42_O20_ISF; k_O19_O20_AB42_ISF * AB42_O19_ISF * AB42_O1_ISF * V_ISF
AB42_O20_ISF -> AB42_O19_ISF + AB42_O1_ISF; k_O20_O19_AB42_ISF * AB42_O20_ISF * V_ISF
AB42_O20_ISF + AB42_O1_ISF -> AB42_O21_ISF; k_O20_O21_AB42_ISF * AB42_O20_ISF * AB42_O1_ISF * V_ISF
AB42_O21_ISF -> AB42_O20_ISF + AB42_O1_ISF; k_O21_O20_AB42_ISF * AB42_O21_ISF * V_ISF
AB42_O21_ISF + AB42_O1_ISF -> AB42_O22_ISF; k_O21_O22_AB42_ISF * AB42_O21_ISF * AB42_O1_ISF * V_ISF
AB42_O22_ISF -> AB42_O21_ISF + AB42_O1_ISF; k_O22_O21_AB42_ISF * AB42_O22_ISF * V_ISF
AB42_O22_ISF + AB42_O1_ISF -> AB42_O23_ISF; k_O22_O23_AB42_ISF * AB42_O22_ISF * AB42_O1_ISF * V_ISF
AB42_O23_ISF -> AB42_O22_ISF + AB42_O1_ISF; k_O23_O22_AB42_ISF * AB42_O23_ISF * V_ISF
AB42_O23_ISF + AB42_O1_ISF -> AB42_O24_ISF; k_O23_O24_AB42_ISF * AB42_O23_ISF * AB42_O1_ISF * V_ISF
AB42_O24_ISF -> AB42_O23_ISF + AB42_O1_ISF; k_O24_O23_AB42_ISF * AB42_O24_ISF * V_ISF
AB40_O1_ISF + AB40_O1_ISF -> AB40_O2_ISF; k_O1_O2_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O1_ISF * AB40_O1_ISF * V_ISF
AB40_O2_ISF + AB40_O1_ISF -> AB40_O3_ISF; k_O2_O3_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O2_ISF * AB40_O1_ISF * V_ISF
AB40_O3_ISF + AB40_O1_ISF -> AB40_O4_ISF; k_O3_O4_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O3_ISF * AB40_O1_ISF * V_ISF
AB40_O4_ISF + AB40_O1_ISF -> AB40_O5_ISF; k_O4_O5_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O4_ISF * AB40_O1_ISF * V_ISF
AB40_O5_ISF + AB40_O1_ISF -> AB40_O6_ISF; k_O5_O6_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O5_ISF * AB40_O1_ISF * V_ISF
AB40_O6_ISF + AB40_O1_ISF -> AB40_O7_ISF; k_O6_O7_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O6_ISF * AB40_O1_ISF * V_ISF
AB40_O7_ISF + AB40_O1_ISF -> AB40_O8_ISF; k_O7_O8_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O7_ISF * AB40_O1_ISF * V_ISF
AB40_O8_ISF + AB40_O1_ISF -> AB40_O9_ISF; k_O8_O9_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O8_ISF * AB40_O1_ISF * V_ISF
AB40_O9_ISF + AB40_O1_ISF -> AB40_O10_ISF; k_O9_O10_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O9_ISF * AB40_O1_ISF * V_ISF
AB40_O10_ISF + AB40_O1_ISF -> AB40_O11_ISF; k_O10_O11_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O10_ISF * AB40_O1_ISF * V_ISF
AB40_O11_ISF + AB40_O1_ISF -> AB40_O12_ISF; k_O11_O12_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O11_ISF * AB40_O1_ISF * V_ISF
AB40_O12_ISF + AB40_O1_ISF -> AB40_O13_ISF; k_O12_O13_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O12_ISF * AB40_O1_ISF * V_ISF
AB40_O13_ISF + AB40_O1_ISF -> AB40_O14_ISF; k_O13_O14_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O13_ISF * AB40_O1_ISF * V_ISF
AB40_O14_ISF + AB40_O1_ISF -> AB40_O15_ISF; k_O14_O15_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O14_ISF * AB40_O1_ISF * V_ISF
AB40_O15_ISF + AB40_O1_ISF -> AB40_O16_ISF; k_O15_O16_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O15_ISF * AB40_O1_ISF * V_ISF
AB40_O16_ISF + AB40_O1_ISF -> AB40_O17_ISF; k_O16_O17_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O16_ISF * AB40_O1_ISF * V_ISF
AB40_O17_ISF + AB40_O1_ISF -> AB40_O18_ISF; k_O17_O18_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O17_ISF * AB40_O1_ISF * V_ISF
AB40_O18_ISF + AB40_O1_ISF -> AB40_O19_ISF; k_O18_O19_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O18_ISF * AB40_O1_ISF * V_ISF
AB40_O19_ISF + AB40_O1_ISF -> AB40_O20_ISF; k_O19_O20_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O19_ISF * AB40_O1_ISF * V_ISF
AB40_O20_ISF + AB40_O1_ISF -> AB40_O21_ISF; k_O20_O21_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O20_ISF * AB40_O1_ISF * V_ISF
AB40_O21_ISF + AB40_O1_ISF -> AB40_O22_ISF; k_O21_O22_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O21_ISF * AB40_O1_ISF * V_ISF
AB40_O22_ISF + AB40_O1_ISF -> AB40_O23_ISF; k_O22_O23_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O22_ISF * AB40_O1_ISF * V_ISF
AB40_O23_ISF + AB40_O1_ISF -> AB40_O24_ISF; k_O23_O24_AB40_ISF*AB40_PDMA_Vmax_ISF*(AB40_O25_ISF / (AB40_O25_ISF + AB40_PDMA_EC50_ISF)) * AB40_O23_ISF * AB40_O1_ISF * V_ISF
AB42_O1_ISF + AB42_O1_ISF -> AB42_O2_ISF; k_O1_O2_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O1_ISF * AB42_O1_ISF * V_ISF
AB42_O2_ISF + AB42_O1_ISF -> AB42_O3_ISF; k_O2_O3_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O2_ISF * AB42_O1_ISF * V_ISF
AB42_O3_ISF + AB42_O1_ISF -> AB42_O4_ISF; k_O3_O4_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O3_ISF * AB42_O1_ISF * V_ISF
AB42_O4_ISF + AB42_O1_ISF -> AB42_O5_ISF; k_O4_O5_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O4_ISF * AB42_O1_ISF * V_ISF
AB42_O5_ISF + AB42_O1_ISF -> AB42_O6_ISF; k_O5_O6_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O5_ISF * AB42_O1_ISF * V_ISF
AB42_O6_ISF + AB42_O1_ISF -> AB42_O7_ISF; k_O6_O7_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O6_ISF * AB42_O1_ISF * V_ISF
AB42_O7_ISF + AB42_O1_ISF -> AB42_O8_ISF; k_O7_O8_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O7_ISF * AB42_O1_ISF * V_ISF
AB42_O8_ISF + AB42_O1_ISF -> AB42_O9_ISF; k_O8_O9_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O8_ISF * AB42_O1_ISF * V_ISF
AB42_O9_ISF + AB42_O1_ISF -> AB42_O10_ISF; k_O9_O10_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O9_ISF * AB42_O1_ISF * V_ISF
AB42_O10_ISF + AB42_O1_ISF -> AB42_O11_ISF; k_O10_O11_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O10_ISF * AB42_O1_ISF * V_ISF
AB42_O11_ISF + AB42_O1_ISF -> AB42_O12_ISF; k_O11_O12_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O11_ISF * AB42_O1_ISF * V_ISF
AB42_O12_ISF + AB42_O1_ISF -> AB42_O13_ISF; k_O12_O13_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O12_ISF * AB42_O1_ISF * V_ISF
AB42_O13_ISF + AB42_O1_ISF -> AB42_O14_ISF; k_O13_O14_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O13_ISF * AB42_O1_ISF * V_ISF
AB42_O14_ISF + AB42_O1_ISF -> AB42_O15_ISF; k_O14_O15_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O14_ISF * AB42_O1_ISF * V_ISF
AB42_O15_ISF + AB42_O1_ISF -> AB42_O16_ISF; k_O15_O16_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O15_ISF * AB42_O1_ISF * V_ISF
AB42_O16_ISF + AB42_O1_ISF -> AB42_O17_ISF; k_O16_O17_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O16_ISF * AB42_O1_ISF * V_ISF
AB42_O17_ISF + AB42_O1_ISF -> AB42_O18_ISF; k_O17_O18_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O17_ISF * AB42_O1_ISF * V_ISF
AB42_O18_ISF + AB42_O1_ISF -> AB42_O19_ISF; k_O18_O19_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O18_ISF * AB42_O1_ISF * V_ISF
AB42_O19_ISF + AB42_O1_ISF -> AB42_O20_ISF; k_O19_O20_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O19_ISF * AB42_O1_ISF * V_ISF
AB42_O20_ISF + AB42_O1_ISF -> AB42_O21_ISF; k_O20_O21_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O20_ISF * AB42_O1_ISF * V_ISF
AB42_O21_ISF + AB42_O1_ISF -> AB42_O22_ISF; k_O21_O22_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O21_ISF * AB42_O1_ISF * V_ISF
AB42_O22_ISF + AB42_O1_ISF -> AB42_O23_ISF; k_O22_O23_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O22_ISF * AB42_O1_ISF * V_ISF
AB42_O23_ISF + AB42_O1_ISF -> AB42_O24_ISF; k_O23_O24_AB42_ISF*AB42_PDMA_Vmax_ISF*(AB42_O25_ISF / (AB42_O25_ISF + AB42_PDMA_EC50_ISF)) * AB42_O23_ISF * AB42_O1_ISF * V_ISF
AB40_O13_ISF + AB40_O1_ISF -> AB40_O25_ISF; Baseline_AB40_O_P * AB40_O13_ISF * AB40_O1_ISF * V_ISF
AB40_O14_ISF + AB40_O1_ISF -> AB40_O25_ISF; Baseline_AB40_O_P * AB40_O14_ISF * AB40_O1_ISF * V_ISF
AB40_O15_ISF + AB40_O1_ISF -> AB40_O25_ISF; Baseline_AB40_O_P * AB40_O15_ISF * AB40_O1_ISF * V_ISF
AB40_O16_ISF + AB40_O1_ISF -> AB40_O25_ISF; Baseline_AB40_O_P * AB40_O16_ISF * AB40_O1_ISF * V_ISF
AB40_O17_ISF + AB40_O1_ISF -> AB40_O25_ISF; Baseline_AB40_O_P * AB40_O17_ISF * AB40_O1_ISF * V_ISF
AB40_O18_ISF + AB40_O1_ISF -> AB40_O25_ISF; Baseline_AB40_O_P * AB40_O18_ISF * AB40_O1_ISF * V_ISF
AB42_O13_ISF + AB42_O1_ISF -> AB42_O25_ISF; Baseline_AB42_O_P * AB42_O13_ISF * AB42_O1_ISF * V_ISF
AB42_O14_ISF + AB42_O1_ISF -> AB42_O25_ISF; Baseline_AB42_O_P * AB42_O14_ISF * AB42_O1_ISF * V_ISF
AB42_O15_ISF + AB42_O1_ISF -> AB42_O25_ISF; Baseline_AB42_O_P * AB42_O15_ISF * AB42_O1_ISF * V_ISF
AB42_O16_ISF + AB42_O1_ISF -> AB42_O25_ISF; Baseline_AB42_O_P * AB42_O16_ISF * AB42_O1_ISF * V_ISF
AB42_O17_ISF + AB42_O1_ISF -> AB42_O25_ISF; Baseline_AB42_O_P * AB42_O17_ISF * AB42_O1_ISF * V_ISF
AB42_O18_ISF + AB42_O1_ISF -> AB42_O25_ISF; Baseline_AB42_O_P * AB42_O18_ISF * AB42_O1_ISF * V_ISF
AB40_O2_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O2_ISF * V_ISF
AB40_O3_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O3_ISF * V_ISF
AB40_O4_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O4_ISF * V_ISF
AB40_O5_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O5_ISF * V_ISF
AB40_O6_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O6_ISF * V_ISF
AB40_O7_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O7_ISF * V_ISF
AB40_O8_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O8_ISF * V_ISF
AB40_O9_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O9_ISF * V_ISF
AB40_O10_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O10_ISF * V_ISF
AB40_O11_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O11_ISF * V_ISF
AB40_O12_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O12_ISF * V_ISF
AB40_O13_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O13_ISF * V_ISF
AB40_O14_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O14_ISF * V_ISF
AB40_O15_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O15_ISF * V_ISF
AB40_O16_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O16_ISF * V_ISF
AB40_O17_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O17_ISF * V_ISF
AB40_O18_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O18_ISF * V_ISF
AB40_O19_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O19_ISF * V_ISF
AB40_O20_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O20_ISF * V_ISF
AB40_O21_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O21_ISF * V_ISF
AB40_O22_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O22_ISF * V_ISF
AB40_O23_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O23_ISF * V_ISF
AB40_O24_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O24_ISF * V_ISF
AB42_O2_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O2_ISF * V_ISF
AB42_O3_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O3_ISF * V_ISF
AB42_O4_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O4_ISF * V_ISF
AB42_O5_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O5_ISF * V_ISF
AB42_O6_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O6_ISF * V_ISF
AB42_O7_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O7_ISF * V_ISF
AB42_O8_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O8_ISF * V_ISF
AB42_O9_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O9_ISF * V_ISF
AB42_O10_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O10_ISF * V_ISF
AB42_O11_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O11_ISF * V_ISF
AB42_O12_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O12_ISF * V_ISF
AB42_O13_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O13_ISF * V_ISF
AB42_O14_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O14_ISF * V_ISF
AB42_O15_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O15_ISF * V_ISF
AB42_O16_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O16_ISF * V_ISF
AB42_O17_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O17_ISF * V_ISF
AB42_O18_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O18_ISF * V_ISF
AB42_O19_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O19_ISF * V_ISF
AB42_O20_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O20_ISF * V_ISF
AB42_O21_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O21_ISF * V_ISF
AB42_O22_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O22_ISF * V_ISF
AB42_O23_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O23_ISF * V_ISF
AB42_O24_ISF -> ; Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O24_ISF * V_ISF
AB40_O25_ISF -> ; 0.5*Microglia*(Microglia_high_frac*Microglia_high_rate_AB40 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB40) * AB40_O25_ISF * V_ISF
AB42_O25_ISF -> ; 0.5*Microglia*(Microglia_high_frac*Microglia_high_rate_AB42 + (1.0 - Microglia_high_frac)*Microglia_low_rate_AB42) * AB42_O25_ISF * V_ISF
AB40_O24_ISF -> AB40_O12_ISF + AB40_O12_ISF; k_O24_O12_AB40_ISF*k_O24_O23_AB40_ISF * AB40_O24_ISF * V_ISF
AB42_O24_ISF -> AB42_O12_ISF + AB42_O12_ISF; k_O24_O12_AB42_ISF*k_O24_O23_AB42_ISF * AB42_O24_ISF * V_ISF
AB40_O1_ISF -> ; IDE_conc_ISF * AB40_IDE_Kcat_lin_ISF * ((AB40_O1_ISF)^AB40_IDE_Hill_ISF / ((AB40_O1_ISF )^AB40_IDE_Hill_ISF + AB40_IDE_IC50_ISF^AB40_IDE_Hill_ISF)) * V_ISF
AB42_O1_ISF -> ; IDE_conc_ISF * AB42_IDE_Kcat_lin_ISF * ((AB42_O1_ISF)^AB42_IDE_Hill_ISF / ((AB42_O1_ISF )^AB42_IDE_Hill_ISF + AB42_IDE_IC50_ISF^AB42_IDE_Hill_ISF)) * V_ISF
 -> APP_ISF; k_APP_production * V_ISF
 -> AB40_O1_central; AB40_systemic_synthesis_rate * V_central
 -> AB42_O1_central; AB42_systemic_synthesis_rate * V_central
APP_ISF -> C99_ISF; k_C99 * APP_ISF * V_ISF
C99_ISF -> ; v_C99 * C99_ISF * V_ISF
C99_ISF -> AB40_O1_ISF; k_in_AB40 * C99_ISF * V_ISF
C99_ISF -> AB42_O1_ISF; k_in_AB42 * C99_ISF * V_ISF
AB40_O1_ISF -> AB40_O1_PVS; (1.0 - sigma_ISF_O1) * Q_PVS * AB40_O1_ISF
AB40_O2_ISF -> AB40_O2_PVS; (1.0 - sigma_ISF_O2) * Q_PVS * AB40_O2_ISF
AB40_O3_ISF -> AB40_O3_PVS; (1.0 - sigma_ISF_O3) * Q_PVS * AB40_O3_ISF
AB40_O4_ISF -> AB40_O4_PVS; (1.0 - sigma_ISF_O4) * Q_PVS * AB40_O4_ISF
AB40_O5_ISF -> AB40_O5_PVS; (1.0 - sigma_ISF_O5) * Q_PVS * AB40_O5_ISF
AB40_O6_ISF -> AB40_O6_PVS; (1.0 - sigma_ISF_O6) * Q_PVS * AB40_O6_ISF
AB40_O7_ISF -> AB40_O7_PVS; (1.0 - sigma_ISF_O7) * Q_PVS * AB40_O7_ISF
AB40_O8_ISF -> AB40_O8_PVS; (1.0 - sigma_ISF_O8) * Q_PVS * AB40_O8_ISF
AB40_O9_ISF -> AB40_O9_PVS; (1.0 - sigma_ISF_O9) * Q_PVS * AB40_O9_ISF
AB40_O10_ISF -> AB40_O10_PVS; (1.0 - sigma_ISF_O10) * Q_PVS * AB40_O10_ISF
AB40_O11_ISF -> AB40_O11_PVS; (1.0 - sigma_ISF_O11) * Q_PVS * AB40_O11_ISF
AB40_O12_ISF -> AB40_O12_PVS; (1.0 - sigma_ISF_O12) * Q_PVS * AB40_O12_ISF
AB40_O13_ISF -> AB40_O13_PVS; (1.0 - sigma_ISF_O13) * Q_PVS * AB40_O13_ISF
AB40_O14_ISF -> AB40_O14_PVS; (1.0 - sigma_ISF_O14) * Q_PVS * AB40_O14_ISF
AB40_O15_ISF -> AB40_O15_PVS; (1.0 - sigma_ISF_O15) * Q_PVS * AB40_O15_ISF
AB40_O16_ISF -> AB40_O16_PVS; (1.0 - sigma_ISF_O16) * Q_PVS * AB40_O16_ISF
AB40_O17_ISF -> AB40_O17_PVS; (1.0 - sigma_ISF_O17) * Q_PVS * AB40_O17_ISF
AB40_O18_ISF -> AB40_O18_PVS; (1.0 - sigma_ISF_O18) * Q_PVS * AB40_O18_ISF
AB40_O19_ISF -> AB40_O19_PVS; (1.0 - sigma_ISF_O19) * Q_PVS * AB40_O19_ISF
AB40_O20_ISF -> AB40_O20_PVS; (1.0 - sigma_ISF_O20) * Q_PVS * AB40_O20_ISF
AB40_O21_ISF -> AB40_O21_PVS; (1.0 - sigma_ISF_O21) * Q_PVS * AB40_O21_ISF
AB40_O22_ISF -> AB40_O22_PVS; (1.0 - sigma_ISF_O22) * Q_PVS * AB40_O22_ISF
AB40_O23_ISF -> AB40_O23_PVS; (1.0 - sigma_ISF_O23) * Q_PVS * AB40_O23_ISF
AB40_O24_ISF -> AB40_O24_PVS; (1.0 - sigma_ISF_O24) * Q_PVS * AB40_O24_ISF
AB42_O1_ISF -> AB42_O1_PVS; (1.0 - sigma_ISF_O1) * Q_PVS * AB42_O1_ISF
AB42_O2_ISF -> AB42_O2_PVS; (1.0 - sigma_ISF_O2) * Q_PVS * AB42_O2_ISF
AB42_O3_ISF -> AB42_O3_PVS; (1.0 - sigma_ISF_O3) * Q_PVS * AB42_O3_ISF
AB42_O4_ISF -> AB42_O4_PVS; (1.0 - sigma_ISF_O4) * Q_PVS * AB42_O4_ISF
AB42_O5_ISF -> AB42_O5_PVS; (1.0 - sigma_ISF_O5) * Q_PVS * AB42_O5_ISF
AB42_O6_ISF -> AB42_O6_PVS; (1.0 - sigma_ISF_O6) * Q_PVS * AB42_O6_ISF
AB42_O7_ISF -> AB42_O7_PVS; (1.0 - sigma_ISF_O7) * Q_PVS * AB42_O7_ISF
AB42_O8_ISF -> AB42_O8_PVS; (1.0 - sigma_ISF_O8) * Q_PVS * AB42_O8_ISF
AB42_O9_ISF -> AB42_O9_PVS; (1.0 - sigma_ISF_O9) * Q_PVS * AB42_O9_ISF
AB42_O10_ISF -> AB42_O10_PVS; (1.0 - sigma_ISF_O10) * Q_PVS * AB42_O10_ISF
AB42_O11_ISF -> AB42_O11_PVS; (1.0 - sigma_ISF_O11) * Q_PVS * AB42_O11_ISF
AB42_O12_ISF -> AB42_O12_PVS; (1.0 - sigma_ISF_O12) * Q_PVS * AB42_O12_ISF
AB42_O13_ISF -> AB42_O13_PVS; (1.0 - sigma_ISF_O13) * Q_PVS * AB42_O13_ISF
AB42_O14_ISF -> AB42_O14_PVS; (1.0 - sigma_ISF_O14) * Q_PVS * AB42_O14_ISF
AB42_O15_ISF -> AB42_O15_PVS; (1.0 - sigma_ISF_O15) * Q_PVS * AB42_O15_ISF
AB42_O16_ISF -> AB42_O16_PVS; (1.0 - sigma_ISF_O16) * Q_PVS * AB42_O16_ISF
AB42_O17_ISF -> AB42_O17_PVS; (1.0 - sigma_ISF_O17) * Q_PVS * AB42_O17_ISF
AB42_O18_ISF -> AB42_O18_PVS; (1.0 - sigma_ISF_O18) * Q_PVS * AB42_O18_ISF
AB42_O19_ISF -> AB42_O19_PVS; (1.0 - sigma_ISF_O19) * Q_PVS * AB42_O19_ISF
AB42_O20_ISF -> AB42_O20_PVS; (1.0 - sigma_ISF_O20) * Q_PVS * AB42_O20_ISF
AB42_O21_ISF -> AB42_O21_PVS; (1.0 - sigma_ISF_O21) * Q_PVS * AB42_O21_ISF
AB42_O22_ISF -> AB42_O22_PVS; (1.0 - sigma_ISF_O22) * Q_PVS * AB42_O22_ISF
AB42_O23_ISF -> AB42_O23_PVS; (1.0 - sigma_ISF_O23) * Q_PVS * AB42_O23_ISF
AB42_O24_ISF -> AB42_O24_PVS; (1.0 - sigma_ISF_O24) * Q_PVS * AB42_O24_ISF
AB40_O1_PVS -> AB40_O1_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O1_PVS
AB40_O2_PVS -> AB40_O2_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O2_PVS
AB40_O3_PVS -> AB40_O3_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O3_PVS
AB40_O4_PVS -> AB40_O4_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O4_PVS
AB40_O5_PVS -> AB40_O5_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O5_PVS
AB40_O6_PVS -> AB40_O6_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O6_PVS
AB40_O7_PVS -> AB40_O7_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O7_PVS
AB40_O8_PVS -> AB40_O8_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O8_PVS
AB40_O9_PVS -> AB40_O9_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O9_PVS
AB40_O10_PVS -> AB40_O10_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O10_PVS
AB40_O11_PVS -> AB40_O11_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O11_PVS
AB40_O12_PVS -> AB40_O12_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O12_PVS
AB40_O13_PVS -> AB40_O13_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O13_PVS
AB40_O14_PVS -> AB40_O14_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O14_PVS
AB40_O15_PVS -> AB40_O15_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O15_PVS
AB40_O16_PVS -> AB40_O16_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O16_PVS
AB40_O17_PVS -> AB40_O17_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O17_PVS
AB40_O18_PVS -> AB40_O18_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O18_PVS
AB40_O19_PVS -> AB40_O19_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O19_PVS
AB40_O20_PVS -> AB40_O20_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O20_PVS
AB40_O21_PVS -> AB40_O21_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O21_PVS
AB40_O22_PVS -> AB40_O22_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O22_PVS
AB40_O23_PVS -> AB40_O23_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O23_PVS
AB40_O24_PVS -> AB40_O24_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB40_O24_PVS
AB42_O1_PVS -> AB42_O1_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O1_PVS
AB42_O2_PVS -> AB42_O2_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O2_PVS
AB42_O3_PVS -> AB42_O3_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O3_PVS
AB42_O4_PVS -> AB42_O4_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O4_PVS
AB42_O5_PVS -> AB42_O5_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O5_PVS
AB42_O6_PVS -> AB42_O6_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O6_PVS
AB42_O7_PVS -> AB42_O7_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O7_PVS
AB42_O8_PVS -> AB42_O8_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O8_PVS
AB42_O9_PVS -> AB42_O9_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O9_PVS
AB42_O10_PVS -> AB42_O10_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O10_PVS
AB42_O11_PVS -> AB42_O11_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O11_PVS
AB42_O12_PVS -> AB42_O12_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O12_PVS
AB42_O13_PVS -> AB42_O13_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O13_PVS
AB42_O14_PVS -> AB42_O14_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O14_PVS
AB42_O15_PVS -> AB42_O15_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O15_PVS
AB42_O16_PVS -> AB42_O16_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O16_PVS
AB42_O17_PVS -> AB42_O17_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O17_PVS
AB42_O18_PVS -> AB42_O18_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O18_PVS
AB42_O19_PVS -> AB42_O19_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O19_PVS
AB42_O20_PVS -> AB42_O20_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O20_PVS
AB42_O21_PVS -> AB42_O21_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O21_PVS
AB42_O22_PVS -> AB42_O22_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O22_PVS
AB42_O23_PVS -> AB42_O23_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O23_PVS
AB42_O24_PVS -> AB42_O24_central; (1.0 - sigma_PVS_Abeta)*Q_PVS * AB42_O24_PVS
AB40_O1_ISF -> AB40_O1_central; (1 - sigma_ISF_lymph_Abeta) * Qbrain_ISF * AB40_O1_ISF
AB42_O1_ISF -> AB42_O1_central; (1 - sigma_ISF_lymph_Abeta) * Qbrain_ISF * AB42_O1_ISF
AB40_O1_ISF -> AB40_O1_LV; f_LV*Qbrain_ISF * AB40_O1_ISF
AB42_O1_ISF -> AB42_O1_LV; f_LV*Qbrain_ISF * AB42_O1_ISF
AB40_O1_ISF -> AB40_O1_TFV; (1.0 - f_LV) *Qbrain_ISF * AB40_O1_ISF
AB42_O1_ISF -> AB42_O1_TFV; (1.0 - f_LV) *Qbrain_ISF * AB42_O1_ISF
AB40_O1_ISF -> AB40_O1_BBB; CL_up_brain*fBBB*Vol_brain_ES * AB40_O1_ISF
AB42_O1_ISF -> AB42_O1_BBB; CL_up_brain*fBBB*Vol_brain_ES * AB42_O1_ISF
AB40_O1_BBB -> ; kdeg_AB40_O1_BBB * AB40_O1_BBB * V_BBB
AB42_O1_BBB -> ; kdeg_AB42_O1_BBB * AB42_O1_BBB * V_BBB
AB40_O1_BCSFB -> ; kdeg_AB40_O1_BCSFB * AB40_O1_BCSFB * V_BCSFB
AB42_O1_BCSFB -> ; kdeg_AB42_O1_BCSFB * AB42_O1_BCSFB * V_BCSFB
AB40_O1_BrainPlasma -> AB40_O1_BBB; CL_up_brain*fBBB*Vol_brain_ES * AB40_O1_BrainPlasma
AB42_O1_BrainPlasma -> AB42_O1_BBB; CL_up_brain*fBBB*Vol_brain_ES * AB42_O1_BrainPlasma
AB40_O1_BrainPlasma -> AB40_O1_BCSFB; CL_up_brain*(1 - fBBB)*Vol_brain_ES * AB40_O1_BrainPlasma
AB42_O1_BrainPlasma -> AB42_O1_BCSFB; CL_up_brain*(1 - fBBB)*Vol_brain_ES * AB42_O1_BrainPlasma
AB40_O1_TFV -> AB40_O1_BCSFB; (1 - f_LV)*CL_up_brain*(1 - fBBB)*Vol_brain_ES * AB40_O1_TFV
AB42_O1_TFV -> AB42_O1_BCSFB; (1 - f_LV)*CL_up_brain*(1 - fBBB)*Vol_brain_ES * AB42_O1_TFV
AB40_O1_LV -> AB40_O1_BCSFB; f_LV*CL_up_brain*(1 - fBBB)*Vol_brain_ES * AB40_O1_LV
AB42_O1_LV -> AB42_O1_BCSFB; f_LV*CL_up_brain*(1 - fBBB)*Vol_brain_ES * AB42_O1_LV
AB40_O1_BrainPlasma -> AB40_O1_ISF; (1.0 - sigma_vascular_ISF_Abeta)*Qbrain_ISF * AB40_O1_BrainPlasma
AB42_O1_BrainPlasma -> AB42_O1_ISF; (1.0 - sigma_vascular_ISF_Abeta)*Qbrain_ISF * AB42_O1_BrainPlasma
AB40_O1_BrainPlasma -> AB40_O1_LV; f_LV*(1.0 - sigma_vascular_BCSFB_Abeta)*Qbrain_CSF * AB40_O1_BrainPlasma
AB42_O1_BrainPlasma -> AB42_O1_LV; f_LV*(1.0 - sigma_vascular_BCSFB_Abeta)*Qbrain_CSF * AB42_O1_BrainPlasma
AB40_O1_BrainPlasma -> AB40_O1_TFV; (1.0 - f_LV)*(1.0 - sigma_vascular_BCSFB_Abeta)*Qbrain_CSF * AB40_O1_BrainPlasma
AB42_O1_BrainPlasma -> AB42_O1_TFV; (1.0 - f_LV)*(1.0 - sigma_vascular_BCSFB_Abeta)*Qbrain_CSF * AB42_O1_BrainPlasma
AB40_O1_LV -> AB40_O1_TFV; (Qbrain_CSF + Qbrain_ISF) * AB40_O1_LV
AB42_O1_LV -> AB42_O1_TFV; (Qbrain_CSF + Qbrain_ISF) * AB42_O1_LV
AB40_O1_TFV -> AB40_O1_CM; (Qbrain_CSF + Qbrain_ISF) * AB40_O1_TFV
AB42_O1_TFV -> AB42_O1_CM; (Qbrain_CSF + Qbrain_ISF) * AB42_O1_TFV
AB40_O1_CM -> AB40_O1_SAS; (Qbrain_CSF + Qbrain_ISF) * AB40_O1_CM
AB42_O1_CM -> AB42_O1_SAS; (Qbrain_CSF + Qbrain_ISF) * AB42_O1_CM
AB40_O1_SAS -> AB40_O1_ISF; Qbrain_ISF * AB40_O1_SAS
AB42_O1_SAS -> AB42_O1_ISF; Qbrain_ISF * AB42_O1_SAS
AB40_O1_SAS -> AB40_O1_central; (1 - sigma_SAS_lymph)*Qbrain_CSF * AB40_O1_SAS
AB42_O1_SAS -> AB42_O1_central; (1 - sigma_SAS_lymph)*Qbrain_CSF * AB42_O1_SAS
AB40_O1_central -> ; AB_O1_CL * AB40_O1_central
AB42_O1_central -> ; AB_O1_CL * AB42_O1_central
AB40_O1_BrainPlasma -> AB40_O1_central; (Qbrain_plasma - Qlymph_Brain) * AB40_O1_BrainPlasma
AB42_O1_BrainPlasma -> AB42_O1_central; (Qbrain_plasma - Qlymph_Brain) * AB42_O1_BrainPlasma
AB40_O1_central -> AB40_O1_BrainPlasma; Qbrain_plasma * AB40_O1_central
AB42_O1_central -> AB42_O1_BrainPlasma; Qbrain_plasma * AB42_O1_central
AB40_O1_peripheral -> AB40_O1_central; AB_O1_CLd2 * AB40_O1_peripheral
AB40_O1_central -> AB40_O1_peripheral; AB_O1_CLd2 * AB40_O1_central
AB42_O1_peripheral -> AB42_O1_central; AB_O1_CLd2 * AB42_O1_peripheral
AB42_O1_central -> AB42_O1_peripheral; AB_O1_CLd2 * AB42_O1_central

AB40_IDE_Hill_ISF = 2 
AB40_IDE_IC50_ISF = 14.142136 
AB40_IDE_Kcat_lin_ISF = 1500 
AB40_PDMA_EC50_ISF = 50 
AB40_PDMA_Vmax_ISF = 0.05 
AB40_systemic_synthesis_rate = 1.16 
AB42_IDE_Hill_ISF = 2 
AB42_IDE_IC50_ISF = 28.635642 
AB42_IDE_Kcat_lin_ISF = 50 
AB42_PDMA_EC50_ISF = 50 
AB42_PDMA_Vmax_ISF = 0.07 
AB42_systemic_synthesis_rate = 1.16 
AB_O1_CL = 12.6 
AB_O1_CLd2 = 0.01 
Baseline_AB40_O_P = 1.10180959874115e-10
Baseline_AB42_O_P = 1.36788257861307e-08
CL_up_brain = 0.03 
IDE_conc_ISF = 0.005 
Microglia = 1 
Microglia_high_frac = 0 
Microglia_high_rate_AB40 = 1.60E-05 
Microglia_high_rate_AB42 = 2.22E-06 
Microglia_low_rate_AB40 = 8.00E-06 
Microglia_low_rate_AB42 = 1.11E-06 
Q_PVS = 0.0021 
Qbrain_CSF = 0.024 
Qbrain_ISF = 0.0105 
Qbrain_plasma = 21.453 
Qlymph_Brain = 0.0345 
V_BBB = 0.0065909 
V_BCSFB = 0.0006591 
V_BrainPlasma =  0.0319
V_CM = 0.0075 
V_ISF = 0.2505 
V_LV = 0.0225 
V_PVS = 0.00235 
V_SAS = 0.09875 
V_TFV = 0.0225 
V_central = 3.5 
V_peripheral = 7.5
Vol_brain_ES = 0.00725 
fBBB = 0.9090909 
f_LV = 0.5 
k_APP_production = 293 
k_C99 = 0.666 
k_O10_O11_AB40_ISF = 2.22085620197585e-05 
k_O10_O11_AB42_ISF = 0.000273561228790063 
k_O10_O9_AB40_ISF = 1e-05 
k_O10_O9_AB42_ISF = 1.9990000002185e-05
k_O11_O10_AB40_ISF = 1e-05 
k_O11_O10_AB42_ISF = 1.9992486853633e-05
k_O11_O12_AB40_ISF = 2.21116751269036e-05
k_O11_O12_AB42_ISF = 0.000273570139508399
k_O12_O11_AB40_ISF = 1e-05
k_O12_O11_AB42_ISF = 1.9994212964228e-05
k_O12_O13_AB40_ISF = 2.2036191974823e-05 
k_O12_O13_AB42_ISF = 0.000273576515722613
k_O13_O12_AB40_ISF = 1e-05 
k_O13_O12_AB42_ISF = 1.99954483396387e-05 
k_O13_O14_AB40_ISF = 2.19762470308789e-05
k_O13_O14_AB42_ISF = 0.00027358119823599
k_O14_O13_AB40_ISF = 1e-05
k_O14_O13_AB42_ISF = 1.9996355685928e-05
k_O14_O15_AB40_ISF = 2.19278533412182e-05 
k_O14_O15_AB42_ISF = 0.000273584714118453
k_O15_O14_AB40_ISF = 1e-05
k_O15_O14_AB42_ISF = 1.99970370376849e-05
k_O15_O16_AB40_ISF = 2.18882245905901e-05
k_O15_O16_AB42_ISF = 0.000273587405231008
k_O16_O15_AB40_ISF = 1e-05 
k_O16_O15_AB42_ISF = 1.99975585942839e-05 
k_O16_O17_AB40_ISF = 2.18553661906955e-05
k_O16_O17_AB42_ISF = 0.000273589499924914
k_O17_O16_AB40_ISF = 1e-05 
k_O17_O16_AB42_ISF = 1.99979645842025e-05 
k_O17_O18_AB40_ISF = 2.18278200123279e-05
k_O17_O18_AB42_ISF = 0.000273591154691691
k_O18_O17_AB40_ISF = 1e-05 
k_O18_O17_AB42_ISF = 1.99982853227344e-05
k_O18_O19_AB40_ISF = 2.18045001844338e-05
k_O18_O19_AB42_ISF = 0.00027359247922249
k_O19_O18_AB40_ISF = 1e-05 
k_O19_O18_AB42_ISF = 1.99985420618438e-05
k_O19_O20_AB40_ISF = 2.17845846512402e-05 
k_O19_O20_AB42_ISF = 0.000273593551956915 
k_O1_O2_AB40_ISF = 0.00018 
k_O1_O2_AB42_ISF = 0.0003564 
k_O20_O19_AB40_ISF = 1e-05
k_O20_O19_AB42_ISF = 1.99987500002734e-05 
k_O20_O21_AB40_ISF = 2.17674418604651e-05 
k_O20_O21_AB42_ISF = 0.000273594429997008
k_O21_O20_AB40_ISF = 1e-05 
k_O21_O20_AB42_ISF = 1.9998920203238e-05
k_O21_O22_AB40_ISF = 2.17525801568735e-05 
k_O21_O22_AB42_ISF = 0.000273595155583612
k_O22_O21_AB40_ISF = 1e-05 
k_O22_O21_AB42_ISF = 1.99990608567043e-05
k_O22_O23_AB40_ISF = 2.17396121883657e-05
k_O22_O23_AB42_ISF = 0.000273595760420077
k_O23_O22_AB40_ISF = 1e-05
k_O23_O22_AB42_ISF = 1.99991781048892e-05
k_O23_O24_AB40_ISF = 2.17282294437377e-05
k_O23_O24_AB42_ISF = 0.000273596268616006
k_O24_O12_AB40_ISF = 2
k_O24_O12_AB42_ISF = 1 
k_O24_O23_AB40_ISF = 1e-05 
k_O24_O23_AB42_ISF = 1.99992766205286e-05
k_O2_O1_AB40_ISF = 9.72 
k_O2_O1_AB42_ISF = 45.72
k_O2_O3_AB40_ISF = 7.2e-05
k_O2_O3_AB42_ISF = 0.0001368
k_O3_O2_AB40_ISF = 1e-05
k_O3_O2_AB42_ISF = 1e-05 
k_O3_O4_AB40_ISF = 2.60890688259109e-05 
k_O3_O4_AB42_ISF = 0.00027278613554061 
k_O4_O3_AB40_ISF = 1e-05
k_O4_O3_AB42_ISF = 1.98437500336414e-05
k_O4_O5_AB40_ISF = 2.45026178010471e-05
k_O4_O5_AB42_ISF = 0.000273185290628707
k_O5_O4_AB40_ISF = 1e-05 
k_O5_O4_AB42_ISF = 1.99200000173578e-05
k_O5_O6_AB40_ISF = 2.36270566727605e-05
k_O5_O6_AB42_ISF = 0.000273360511493378
k_O6_O5_AB40_ISF = 1e-05 
k_O6_O5_AB42_ISF = 1.99537037137829e-05
k_O6_O7_AB40_ISF = 2.30943396226415e-05
k_O6_O7_AB42_ISF = 0.000273449346420876
k_O7_O6_AB40_ISF = 1e-05
k_O7_O6_AB42_ISF = 1.99708454874077e-05
k_O7_O8_AB40_ISF = 2.2746639089969e-05 
k_O7_O8_AB42_ISF = 0.000273499134448932
k_O8_O7_AB40_ISF = 1e-05 
k_O8_O7_AB42_ISF = 1.99804687542636e-05 
k_O8_O9_AB40_ISF = 2.25073649754501e-05
k_O8_O9_AB42_ISF = 0.000273529184578335
k_O9_O10_AB40_ISF = 2.23357664233577e-05
k_O9_O10_AB42_ISF = 0.000273548387520094
k_O9_O8_AB40_ISF = 1e-05
k_O9_O8_AB42_ISF = 1.99862825818714e-05
k_in_AB40 = 0.238 
k_in_AB42 = 0.01495 
kdeg_AB40_O1_BBB = 26.6 
kdeg_AB40_O1_BCSFB = 26.6 
kdeg_AB42_O1_BBB = 26.6 
kdeg_AB42_O1_BCSFB = 26.6 
sigma_ISF_O1 = 0.2 
sigma_ISF_O10 = 0.99 
sigma_ISF_O11 = 0.99 
sigma_ISF_O12 = 0.99 
sigma_ISF_O13 = 0.99 
sigma_ISF_O14 = 0.99 
sigma_ISF_O15 = 0.99 
sigma_ISF_O16 = 0.99 
sigma_ISF_O17 = 0.999 
sigma_ISF_O18 = 0.999 
sigma_ISF_O19 = 0.999 
sigma_ISF_O2 = 0.9 
sigma_ISF_O20 = 0.999 
sigma_ISF_O21 = 0.999 
sigma_ISF_O22 = 0.999 
sigma_ISF_O23 = 0.999 
sigma_ISF_O24 = 0.999 
sigma_ISF_O3 = 0.9 
sigma_ISF_O4 = 0.9 
sigma_ISF_O5 = 0.9 
sigma_ISF_O6 = 0.9 
sigma_ISF_O7 = 0.9 
sigma_ISF_O8 = 0.9 
sigma_ISF_O9 = 0.9 
sigma_ISF_lymph_Abeta = 0 
sigma_PVS_Abeta = 0 
sigma_SAS_lymph = 0
sigma_vascular_BCSFB_Abeta = 0.9974 
sigma_vascular_ISF_Abeta = 1 
v_C99 = 0.333 
end
''')
print(r.getReactionIds())
print(r.getCurrentAntimony())
print(te.getODEsFromModel(r))
r.exportToSBML('Antimony_PBPK_model.xml') 

result = r.simulate(0, 100*365*24, 100,['time', '[AB42_O1_ISF]','[AB42_O25_ISF]'])
print(r['[AB42_O1_ISF]'],r['[AB42_O25_ISF]'])
r.plot()
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def run_simulation():
    r = te.loada(__file__.replace('.py', '.txt'))
    r.setIntegrator('cvode')
    r.integrator.absolute_tolerance = 1e-8
    r.integrator.relative_tolerance = 1e-8
    r.integrator.setValue('stiff', True)
    print(te.getODEsFromModel(r))
    result = r.simulate(0, 1000, 20000, ['time','[Antibody_Plasma]','[Antibody_TissueVascular]','[Antibody_BrainISF]',
    '[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_CSF]','[Antibody_TissueEndosomal]',
    '[Antibody__FcRn_TissueEndosomal]','[FcRn_TissueEndosomal]','[Antibody__FcRn_BBB]','[FcRn_BBB]'])
    plt.plot(result['time'], result['[Antibody_Plasma]'], label='Plasma')
    # plt.plot(result['time'], result['[Antibody_TissueVascular]'], label='Tissue_Vascular')
    plt.plot(result['time'], result['[Antibody_BrainISF]'], label='BrainISF')
    print(result['[Antibody_Plasma]'])
    print(result['[Antibody_BrainISF]'])
    print(result['[Antibody_CSF]'])
    print(result['[Antibody_BBB]'])
    print(result['[Antibody_TissueEndosomal]'])
    print(result['[Antibody__FcRn_TissueEndosomal]'])
    print(result['[FcRn_TissueEndosomal]'])
    print(result['[Antibody__FcRn_BBB]'])
    print(result['[FcRn_BBB]'])
    # plt.plot(result['time'], result['[Antibody_BrainVascular]'], label='BrainVascular')
    # plt.plot(result['time'], result['[Antibody_BBB]'], label='BBB')
    plt.plot(result['time'], result['[Antibody_CSF]'], label='CSF')
    # plt.plot(result['time'], result['[Antibody_TissueEndosomal]'], label='TissueEndosomal')
    # plt.plot(result['time'], result['[Antibody__FcRn_TissueEndosomal]'], label='FcRn_TissueEndosomal')
    # plt.plot(result['time'], result['[FcRn_TissueEndosomal]'], label='FcRn_TissueEndosomal')
    # plt.plot(result['time'], result['[Antibody__FcRn_BBB]'], label='FcRn_BBB')
    # plt.plot(result['time'], result['[FcRn_BBB]'], label='FcRn_BBB')
    df = pd.read_csv('Chang2019_Figure5A.csv')
    plasma_data = df[df['observation'] == 'plasma']
    plasma_sim = plasma_data[plasma_data['series'] == '36mgsim']
    # print(plasma_sim) 
    plasma_exp = plasma_data[plasma_data['series'] == '36mgdata']
    # print(plasma_exp)
    csf_data = df[df['observation'] == 'CSF']
    csf_sim = csf_data[csf_data['series'] == '36mgsim']
    # print(csf_sim)
    csf_exp = csf_data[csf_data['series'] == '36mgdata']
    # print(csf_exp)
    BDPlasma_data = df[df['observation'] == 'BDPlasma']
    BDPlasma_sim = BDPlasma_data[BDPlasma_data['series'] == '30mg']
    BDCSF_data = df[df['observation'] == 'BDCSF']
    BDCSF_sim = BDCSF_data[BDCSF_data['series'] == '30mg']
    BDBrainISF_data = df[df['observation'] == 'BDBrainISF']
    BDBrainISF_sim = BDBrainISF_data[BDBrainISF_data['series'] == '30mg']
    # print(BDPlasma_sim)
    dfMatlab = pd.read_csv("D:\Minimal_bPBPK\PK_Predictions.csv")
    dfMatlab_Plasma = dfMatlab['Plasma']
    dfMatlab_CSF = dfMatlab['CSF']
    dfMatlab_BrainISF = dfMatlab['BrainISF']
    plt.plot(dfMatlab['time'], dfMatlab_Plasma, 'b.', linewidth=2, label='Matlab Plasma')
    plt.plot(dfMatlab['time'], dfMatlab_CSF, 'g.', linewidth=2, label='Matlab CSF')
    plt.plot(dfMatlab['time'], dfMatlab_BrainISF, 'y.', linewidth=2, label='Matlab BrainISF')
    # plt.plot(plasma_sim['time'], plasma_sim['measurement'], 'b.', linewidth=2, label='Simulation (36mg)')
    # plt.scatter(plasma_exp['time'], plasma_exp['measurement'], color='red', s=50, marker='o', label='Experimental (36mg)')
    # plt.plot(csf_sim['time'], csf_sim['measurement'], 'g.', linewidth=2, label='Simulation (36mg)')
    # plt.scatter(csf_exp['time'], csf_exp['measurement'], color='orange', s=50, marker='s', label='Experimental (36mg)')
    # plt.plot(BDPlasma_sim['time'], BDPlasma_sim['measurement'], 'c.', linewidth=2, label='BD Plasma 30mg')
    # plt.plot(BDCSF_sim['time'], BDCSF_sim['measurement'], 'm.', linewidth=2, label='BD CSF 30mg')
    # plt.plot(BDBrainISF_sim['time'], BDBrainISF_sim['measurement'], 'y.', linewidth=2, label='BD BrainISF 30mg')
    plt.yscale('log')
    plt.xlim(0, 1000)
    # plt.ylim(1e-1, 1e5)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run_simulation()
    
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def run_simulation():
    # Set figure size to be wider to accommodate legend
    plt.figure(figsize=(8, 8))
    r = te.loada(__file__.replace('.py', '.txt'))
    r.setIntegrator('cvode')
    r.integrator.absolute_tolerance = 1e-8
    r.integrator.relative_tolerance = 1e-8
    r.integrator.setValue('stiff', True)
    result = r.simulate(0, 2000, 2000000, ['time','[Antibody_Plasma]','[Antibody_BrainISF]','[Antibody_LiverVascular]',
    '[Antibody_LungVascular]','[Antibody_LymphNode]','[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_SAS]',
    '[Antibody_LV]'])
    plt.plot(result['time'], result['[Antibody_Plasma]'], label='Plasma')
    # plt.plot(result['time'], result['[Antibody_BrainISF]'], label='BrainISF')
    # plt.plot(result['time'], result['[Antibody_LiverVascular]'], label='LiverVascular')
    # plt.plot(result['time'], result['[Antibody_LungVascular]'], label='LungVascular')
    # plt.plot(result['time'], result['[Antibody_LymphNode]'], label='LymphNode')
    # plt.plot(result['time'], result['[Antibody_BrainVascular]'], label='BrainVascular')
    # plt.plot(result['time'], result['[Antibody_LV]'],label='LV')
    # plt.plot(result['time'], result['[Antibody_BBB]'], label='BBB')
    plt.plot(result['time'], result['[Antibody_SAS]'], label='SAS')
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
    curtin_data = df[df['observation'] == 'AntibodySerum']
    curtin_exp = curtin_data[curtin_data['series'] == '36mg']
    plt.plot(plasma_sim['time'], plasma_sim['measurement'], 'b.', linewidth=2, label='Chang Sim Plasma (36mg)')
    plt.scatter(curtin_exp['time'], curtin_exp['measurement'], color='blue', s=50, marker='o', label='Curtin serum (36mg)')
    plt.scatter(plasma_exp['time'], plasma_exp['measurement'], color='red', s=50, marker='o', label='Chang data serum (36mg)')
    plt.plot(csf_sim['time'], csf_sim['measurement'], 'g.', linewidth=2, label='Chang Sim CSF (36mg)')
    plt.scatter(csf_exp['time'], csf_exp['measurement'], color='orange', s=50, marker='s', label='Chang data CSF (36mg)')
    plt.axhline(y=6643, color='gray', linestyle='--', linewidth=1, label='6643 nM')
    plt.xlabel('Time (hour)')
    plt.ylabel('Antibody concentration (nM)')
    plt.yscale('log')
    # plt.xlim(0.1, 1000)
    plt.ylim(1e-1, 1e5)
    plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
    plt.tight_layout()
    plt.savefig(__file__.replace('.py', '.png'), bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    run_simulation()
    
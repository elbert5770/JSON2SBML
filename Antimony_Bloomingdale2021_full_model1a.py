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
    result = r.simulate(0, 2000, 1000, ['time','[Antibody_Plasma]','[Antibody_TissueVascular]','[Antibody_BrainISF]',
    '[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_CSF]'])
    # plt.plot(result['time'], result['[Antibody_Plasma]'], label='Plasma')
    # plt.plot(result['time'], result['[Antibody_TissueVascular]'], label='Tissue_Vascular')
    # plt.plot(result['time'], result['[Antibody_BrainISF]'], label='BrainISF')
    
    # plt.plot(result['time'], result['[Antibody_BrainVascular]'], label='BrainVascular')
    # plt.plot(result['time'], result['[Antibody_BBB]'], label='BBB')
    plt.plot(result['time'], result['[Antibody_CSF]'], label='CSF')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run_simulation()
    
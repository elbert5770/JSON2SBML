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
    result = r.simulate(0, 2000, 1000, ['time','[Antibody_Plasma]','[Antibody_BrainISF]','[Antibody_LiverVascular]',
    '[Antibody_LungVascular]','[Antibody_LymphNode]','[Antibody_BrainVascular]','[Antibody_BBB]','[Antibody_SAS]',
    '[Antibody_LV]'])
    # plt.plot(result['time'], result['[Antibody_Plasma]'], label='Plasma')
    plt.plot(result['time'], result['[Antibody_BrainISF]'], label='BrainISF')
    # plt.plot(result['time'], result['[Antibody_LiverVascular]'], label='LiverVascular')
    # plt.plot(result['time'], result['[Antibody_LungVascular]'], label='LungVascular')
    # plt.plot(result['time'], result['[Antibody_LymphNode]'], label='LymphNode')
    # plt.plot(result['time'], result['[Antibody_BrainVascular]'], label='BrainVascular')
    plt.plot(result['time'], result['[Antibody_LV]'],label='LV')
    plt.plot(result['time'], result['[Antibody_BBB]'], label='BBB')
    plt.plot(result['time'], result['[Antibody_SAS]'], label='SAS')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run_simulation()
    
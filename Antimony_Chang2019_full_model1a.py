import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def run_simulation():
    r = te.loada(__file__.replace('.py', '.txt'))
    
    result = r.simulate(0, 20, 1000, ['time','[Antibody_Plasma]'])
    plt.plot(result['time'], result['[Antibody_Plasma]'])

if __name__ == "__main__":
    r, result1,result2, csv_data_3C_ApoE, csv_data_3C_nonApoE, csv_data_3A_ApoE, csv_data_3A_nonApoE, suvr = run_simulation()
    


SmaxPro	=100
Anti_ABeta_bound_sum = 0
EC50_pro=	1
gamma_MG	=0.002851928
Microglia_cells_max = 4
Microglia_baseline = 1
Microglia_cell_count = 1
rateofchange = (1 + SmaxPro * Anti_ABeta_bound_sum / (EC50_pro + Anti_ABeta_bound_sum)) * (gamma_MG * Microglia_cells_max / (Microglia_cells_max - Microglia_baseline)) * Microglia_cell_count * ((Microglia_cells_max - Microglia_cell_count) / Microglia_cells_max) -(gamma_MG * Microglia_cell_count) 








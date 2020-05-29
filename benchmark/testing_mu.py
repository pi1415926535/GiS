from benchmark.methods import test_ndocd
from plots.plots import plot_measure_results_data, create_3_plots
import pickle

folder = "data/benchmark/"
mu_list = [i*0.1 for i in range(1, 6)]
times = []
nmis = []
modularities = []
n_communities = []
labels = []
modularities_base = []
n_communities_base = []
modification_number = 20
modification_percent = 0.2
for modification, modification_type in zip([False, True, True], ["percent", "percent", "number"]):
    this_times = []
    this_nmis = []
    this_mods = []
    this_ncoms = []
    this_mods_base = []
    this_coms_base = []
    for mu in mu_list:
        time, nmi, mod_ndocd, mod_base, n_coms, n_coms_base = test_ndocd(folder, file_appending="b5_" + str(mu), MD_threshold=0.3, JS_threshold=0.3, modification=modification, modification_type=modification_type, modification_number=modification_number, modification_percent=modification_percent)
        this_times.append(time)
        this_nmis.append(nmi)
        this_mods.append(mod_ndocd)
        this_ncoms.append(n_coms)
        this_mods_base.append(mod_base)
        this_coms_base.append(n_coms_base)
        print(f'Ended: N - {mu}, time - {time} \n')
    times.append(this_times)
    nmis.append(this_nmis)
    modularities.append(this_mods)
    n_communities.append(this_ncoms)
    labels.append(f"N = {mu}")
    modularities_base.append(this_mods_base)
    n_communities_base.append(this_coms_base)
    print(f'\n\n Ended: modification, modification_type - {modification, modification_type} \n\n')


labels = ["Base NDOCD", "Modification percent", "Modification number", "BigClam"][:3]
create_3_plots(nmis, modularities, n_communities, modularities_base, n_communities_base, labels, mu_list, "mu - mixing parameter", "b5")

# pickle.dump((times, nmis, modularities, n_communities, labels, modularities_base, n_communities_base, mu_list), open("data/benchmark/b5", 'wb'))

nmis[0] = [a+0.003 for a in nmis[0]]
modularities[0] = [a+0.005 for a in modularities[0]]
n_communities[0] = [a+0.2 for a in n_communities[0]]
# import pandas as pd
# times[3] = list(pd.read_csv("time.csv", header=None).iloc[:, 1]*10)

from scipy.sparse import load_npz
from NDOCD.NDOCD import NDOCD
import numpy as np
from NDOCD.load_data import write_communities_to_file, get_email_graph, get_communities_list2
from measures.mutual_information import normalized_mutual_information
from measures.link_belong_modularity import cal_modularity, get_graph_info
import time
from measures.modularity import convert_communities_to_dict, get_modularity

graph = get_email_graph()
start = time.time()
# ndocd = NDOCD(graph)
# np.save("data/email/neighbours.npy", ndocd.neighbours_edges)
# ndocd = NDOCD(graph, np.load("data/email/neighbours.npy"), modification=True)
# ndocd = NDOCD(graph, modification=True, modification_type="percent", modification_percent=0.2)
ndocd = NDOCD(graph, modification=True, modification_type="number", modification_number=20)


ndocd.JS_threshold = 0.8
ndocd.MD_threshold = 0.25

coms = ndocd.find_all_communities(prune_every=1)
end = time.time()

bigger_than = 6
file = "data/email/coms"
write_communities_to_file([com for com in coms if len(list(com.indices)) > bigger_than], file)
nmi = normalized_mutual_information(file, "data/email/email-communities")
coms2 = [list(com.indices) for com in coms if len(list(com.indices)) > bigger_than]

length = 0
for com in coms2:
    length += len(com)

# coms_dict = convert_communities_to_dict(coms2)
# coms_dict2 = convert_communities_to_dict(coms2*2)
# coms_dict3 = convert_communities_to_dict(get_communities_list2("data/email/email-communities", " "))
# coms_dict4 = convert_communities_to_dict(get_communities_list2("data/email/email-communities", " ")*2)
# coms_dict5 = convert_communities_to_dict([coms2[2]])
# coms_dict6 = convert_communities_to_dict([[i for i in range(1005)]])
# coms_dict7 = convert_communities_to_dict([[i] for i in range(1005)])
# mod1 = get_modularity(get_graph_info("data/email/email-transformed.txt"), coms_dict)
# mod2 = get_modularity(get_graph_info("data/email/email-transformed.txt"), coms_dict2)
# mod3 = get_modularity(get_graph_info("data/email/email-transformed.txt"), coms_dict3)
# mod4 = get_modularity(get_graph_info("data/email/email-transformed.txt"), coms_dict4)
# mod5 = get_modularity(get_graph_info("data/email/email-transformed.txt"), coms_dict5)
# mod6 = get_modularity(get_graph_info("data/email/email-transformed.txt"), coms_dict6)
# mod7 = get_modularity(get_graph_info("data/email/email-transformed.txt"), coms_dict7)
#
# print(f"Mod1: {mod1}")
# print(f"Mod2: {mod2}")
# print(f"Mod3: {mod3}")
# print(f"Mod4: {mod4}")
# print(f"Mod5: {mod5}")
# print(f"Mod6: {mod6}")
# print(f"Mod6: {mod7}")

nx_graph = get_graph_info("data/email/email-transformed.txt")
mod_ndocd = get_modularity(nx_graph , convert_communities_to_dict(coms2))
mod_base = get_modularity(nx_graph , convert_communities_to_dict(get_communities_list2("data/email/email-communities", " ")))
print(f"Normalized mutual information: {nmi:0.04}")
print(f'Average size: {length/len(coms2)}')
print(f'Number of communities: {len(coms2)}')
print(f'Proper number of communities: {len(get_communities_list2("data/email/email-communities", " "))}')
print(f'Time: {end-start}')
print(f'modularity for ndocd {mod_ndocd:0.04}')
print(f'modularity for ground-truth {mod_base:0.04}')

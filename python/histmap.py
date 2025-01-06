import numpy as np
import matplotlib.pyplot as plt
from utils import create_folder

def save_histmap(hash_type:str, dataname=None):
    in_subdir_name = "{}_distribution_probing".format(hash_type) if dataname is None else \
        "{}_{}_distribution_probing".format(dataname, hash_type)
    out_subdir_name = "histmap" if dataname is None else "histmap_" + dataname
    create_folder("./tmp/{}".format(out_subdir_name), exist_ok=True)
    each_probing_cnts = []
    for i in range(100):
        cur_each_probing_cnts = np.loadtxt("./tmp/{}/{}.txt".format(in_subdir_name, i))
        each_probing_cnts.append(cur_each_probing_cnts)
    each_probing_cnts = np.array(each_probing_cnts)
    each_probing_all = np.sum(each_probing_cnts, axis=1)
    each_probing_all_max_idx = np.argmax(each_probing_all)
    each_probing_all_min_idx = np.argmin(each_probing_all)

    a_size = int(np.round(np.sqrt(each_probing_cnts.shape[1])))

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.imshow(np.resize(each_probing_cnts[each_probing_all_max_idx], (a_size, a_size)))
    plt.colorbar(shrink=0.8)
    plt.title("Probing number for each key in worst experiment")
    plt.savefig("./tmp/{}/{}_each_probing_cnts_worst.png".format(out_subdir_name,hash_type), dpi=300, bbox_inches="tight")

    # fig, ax = plt.subplots()
    # plt.imshow(np.resize(each_probing_cnts[each_probing_all_min_idx], (a_size, a_size)))
    # plt.colorbar(shrink=0.8)
    # plt.title("Probing number for each key in best experiment")
    # plt.savefig("./tmp/{}/{}_each_probing_cnts_best.png".format(out_subdir_name, hash_type), dpi=300, bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.imshow(np.resize(np.sum(np.array(each_probing_cnts), axis=0), (a_size, a_size)))
    plt.colorbar(shrink=0.8)
    plt.title("Probing number for each key in all experiments")
    plt.savefig("./tmp/{}/{}_each_probing_cnts_all.png".format(out_subdir_name, hash_type), dpi=300, bbox_inches="tight")

# dataname = "hypercube"
dataname = "denseinterval"
save_histmap("UnivMultShift", dataname)
save_histmap("Indpd2MultShift", dataname)
save_histmap("Indpd5MersennePrime", dataname)
save_histmap("SimpleTabulation", dataname)
save_histmap("Indpd5TZTable", dataname)
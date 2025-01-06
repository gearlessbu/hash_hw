import numpy as np
import matplotlib.pyplot as plt
from utils import create_folder

def save_histmap(hash_type:str):
    create_folder("./tmp/histmap", exist_ok=True)
    each_probing_cnts = []
    for i in range(100):
        cur_each_probing_cnts = np.loadtxt("./tmp/{}_distribution_probing/{}.txt".format(hash_type, i))
        each_probing_cnts.append(cur_each_probing_cnts)
    each_probing_cnts = np.array(each_probing_cnts)
    each_probing_all = np.sum(each_probing_cnts, axis=1)
    each_probing_all_max_idx = np.argmax(each_probing_all)
    each_probing_all_min_idx = np.argmin(each_probing_all)

    fig, ax = plt.subplots(figsize=(9, 9))
    plt.imshow(np.resize(each_probing_cnts[each_probing_all_max_idx], (1024, 1024)))
    plt.title("Probing number for each key in worst experiment")
    plt.savefig("./tmp/histmap/{}_each_probing_cnts_worst.png".format(hash_type), dpi=300, bbox_inches="tight")

    # fig, ax = plt.subplots()
    # plt.imshow(np.resize(each_probing_cnts[each_probing_all_min_idx], (1024, 1024)))
    # plt.title("Probing number for each key in best experiment")
    # plt.savefig("./tmp/histmap/{}_each_probing_cnts_best.png".format(hash_type), dpi=300, bbox_inches="tight")

    fig, ax = plt.subplots()
    plt.imshow(np.resize(np.sum(np.array(each_probing_cnts), axis=0), (1024, 1024)))
    plt.title("Probing number for each key in all experiments")
    plt.savefig("./tmp/histmap/{}_each_probing_cnts_all.png".format(hash_type), dpi=300, bbox_inches="tight")

save_histmap("UnivMultShift")
save_histmap("Indpd2MultShift")
save_histmap("Indpd5MersennePrime")
save_histmap("SimpleTabulation")
save_histmap("Indpd5TZTable")
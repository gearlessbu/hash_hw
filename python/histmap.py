import numpy as np
import matplotlib.pyplot as plt

# SimpleTabulation_each_probing_cnts = []
# for i in range(100):
#     cur_SimpleTabulation_each_probing_cnts = np.loadtxt("./tmp/SimpleTabulation_distribution_probing/{}.txt".format(i))
#     SimpleTabulation_each_probing_cnts.append(cur_SimpleTabulation_each_probing_cnts)

# fig, ax = plt.subplots()
# plt.imshow(np.resize(SimpleTabulation_each_probing_cnts[0], (1024, 1024)))
# plt.title("Probing number for each key in experiment 0")
# plt.savefig("./tmp/SimpleTabulation_each_probing_cnts.png", dpi=300, bbox_inches="tight")


# fig, ax = plt.subplots()
# plt.imshow(np.resize(np.sum(np.array(SimpleTabulation_each_probing_cnts), axis=0), (1024, 1024)))
# plt.title("Probing number for each key in all experiments")
# plt.savefig("./tmp/SimpleTabulation_each_probing_cnts_all.png", dpi=300, bbox_inches="tight")


UnivMultShift_each_probing_cnts = []
for i in range(100):
    cur_UnivMultShift_each_probing_cnts = np.loadtxt("./tmp/UnivMultShift_distribution_probing/{}.txt".format(i))
    UnivMultShift_each_probing_cnts.append(cur_UnivMultShift_each_probing_cnts)
UnivMultShift_each_probing_cnts = np.array(UnivMultShift_each_probing_cnts)
UnivMultShift_each_probing_all = np.sum(UnivMultShift_each_probing_cnts, axis=1)
UnivMultShift_each_probing_all_max_idx = np.argmax(UnivMultShift_each_probing_all)
UnivMultShift_each_probing_all_min_idx = np.argmin(UnivMultShift_each_probing_all)

fig, ax = plt.subplots()
plt.imshow(np.resize(UnivMultShift_each_probing_cnts[UnivMultShift_each_probing_all_max_idx], (1024, 1024)))
plt.title("Probing number for each key in worst experiment")
plt.savefig("./tmp/UnivMultShift_each_probing_cnts_worst.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots()
plt.imshow(np.resize(UnivMultShift_each_probing_cnts[UnivMultShift_each_probing_all_min_idx], (1024, 1024)))
plt.title("Probing number for each key in best experiment")
plt.savefig("./tmp/UnivMultShift_each_probing_cnts_best.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots()
plt.imshow(np.resize(np.sum(np.array(UnivMultShift_each_probing_cnts), axis=0), (1024, 1024)))
plt.title("Probing number for each key in all experiments")
plt.savefig("./tmp/UnivMultShift_each_probing_cnts_all.png", dpi=300, bbox_inches="tight")
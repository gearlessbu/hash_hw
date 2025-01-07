import numpy as np
import matplotlib.pyplot as plt
from utils import create_folder

DSH_map_L = np.loadtxt("tmp/DSH_map_L.txt")
DSH_map_alpha = np.loadtxt("tmp/DSH_map_alpha.txt")
DSH_map_p = np.loadtxt("tmp/DSH_map_p.txt")
DSH_map_r = np.loadtxt("tmp/DSH_map_r.txt")

LSH_map_L = np.loadtxt("tmp/LSH_map_L.txt")
LSH_map_alpha = np.ones(6) * LSH_map_L[3]
LSH_map_p = np.ones(6) * LSH_map_L[3]
LSH_map_r = np.ones(6) * LSH_map_L[3]

ps = [1, 2, 3, 4, 5, 6]
alphas = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
rs = [1, 3, 5, 7, 9, 11]
Ls = [16, 32, 48, 64, 80, 96]

create_folder("tmp/MAPandPR", exist_ok=True)

fig, ax = plt.subplots()
plt.plot(Ls, DSH_map_L, marker='o', label="DSH")
plt.plot(Ls, LSH_map_L, marker='o', label="LSH")
plt.xlabel("$L$")
plt.ylabel("Mean Average Precision")
plt.xticks(Ls)
plt.legend()
plt.savefig("tmp/MAPandPR/map_L.png", dpi=300, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots()
plt.plot(alphas, DSH_map_alpha, marker='o', label="DSH")
plt.plot(alphas, LSH_map_alpha, marker='o', label="LSH")
plt.xlabel(r"$\alpha$")
plt.ylabel("Mean Average Precision")
plt.xticks(alphas)
plt.legend()
plt.savefig("tmp/MAPandPR/map_alpha.png", dpi=300, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots()
plt.plot(ps, DSH_map_p, marker='o', label="DSH")
plt.plot(ps, LSH_map_p, marker='o', label="LSH")
plt.xlabel(r"$p$")
plt.ylabel("Mean Average Precision")
plt.xticks(ps)
plt.legend()
plt.savefig("tmp/MAPandPR/map_p.png", dpi=300, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots()
plt.plot(rs, DSH_map_r, marker='o', label="DSH")
plt.plot(rs, LSH_map_r, marker='o', label="LSH")
plt.xlabel(r"$r$")
plt.ylabel("Mean Average Precision")
plt.xticks(rs)
plt.legend()
plt.savefig("tmp/MAPandPR/map_r.png", dpi=300, bbox_inches="tight")
plt.close()

LSH_PR = np.loadtxt("tmp/MAPandPR/LSH_PR_64.txt")
DSH_PR = np.loadtxt("tmp/MAPandPR/DSH_PR_64.txt")
fig, ax = plt.subplots()
plt.plot(LSH_PR[1], LSH_PR[0], marker='o', label="LSH")
plt.plot(DSH_PR[1], DSH_PR[0], marker='o', label="DSH")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.legend()
plt.gca().set_aspect(1)
plt.savefig("tmp/MAPandPR/RP_64.png", dpi=300, bbox_inches="tight")
plt.close()

LSH_PR = np.loadtxt("tmp/MAPandPR/LSH_PR_96.txt")
DSH_PR = np.loadtxt("tmp/MAPandPR/DSH_PR_96.txt")
fig, ax = plt.subplots()
plt.plot(LSH_PR[1], LSH_PR[0], marker='o', label="LSH")
plt.plot(DSH_PR[1], DSH_PR[0], marker='o', label="DSH")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.legend()
plt.gca().set_aspect(1)
plt.savefig("tmp/MAPandPR/RP_96.png", dpi=300, bbox_inches="tight")
plt.close()

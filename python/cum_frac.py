import numpy as np
import matplotlib.pyplot as plt

UnivMultShift_mean_probing_cnts = np.loadtxt("./tmp/UnivMultShift_mean_probing_cnts.txt")
SimpleTabulation_mean_probing_cnts = np.loadtxt("./tmp/SimpleTabulation_mean_probing_cnts.txt")
Indpd5MersennePrime_mean_probing_cnts = np.loadtxt("./tmp/Indpd5MersennePrime_mean_probing_cnts.txt")

sorted_UnivMultShift = np.sort(UnivMultShift_mean_probing_cnts)
sorted_SimpleTabulation = np.sort(SimpleTabulation_mean_probing_cnts)
sorted_Indpd5MersennePrime = np.sort(Indpd5MersennePrime_mean_probing_cnts)

# Calculate the cumulative fraction
cumulative_fraction = np.arange(1, len(sorted_UnivMultShift) + 1) / len(sorted_UnivMultShift)


fig, ax = plt.subplots()
# Plot the cumulative fraction
# plt.plot(sorted_UnivMultShift, cumulative_fraction, marker='.', linestyle='-', color='b')
# plt.plot(sorted_SimpleTabulation, cumulative_fraction, marker='.', linestyle='-', color='r')
plt.plot(sorted_UnivMultShift, cumulative_fraction, linestyle='-', color='b', label="univ-mult-shift")
plt.plot(sorted_SimpleTabulation, cumulative_fraction, linestyle='-', color='r', label="simple-table")
plt.plot(sorted_Indpd5MersennePrime, cumulative_fraction, linestyle='-', color='g', label="5-indep-Mersenne-prime")
ax.set_xlim(0, 10)
ax.set_ylim(0, 1)
plt.xlabel("average probes per insert/delete")
plt.ylabel("cumulative fraction")
plt.title("Keys from hyper cube")
plt.legend()
plt.savefig("./tmp/hypercube_cumfrac.png", dpi=300, bbox_inches="tight")
# plt.show()
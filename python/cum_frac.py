import numpy as np
import matplotlib.pyplot as plt

UnivMultShift_mean_probing_cnts = np.loadtxt("./tmp/UnivMultShift_mean_probing_cnts.txt")
Indpd2MultShift_mean_probing_cnts = np.loadtxt("./tmp/Indpd2MultShift_mean_probing_cnts.txt")
Indpd5MersennePrime_mean_probing_cnts = np.loadtxt("./tmp/Indpd5MersennePrime_mean_probing_cnts.txt")
SimpleTabulation_mean_probing_cnts = np.loadtxt("./tmp/SimpleTabulation_mean_probing_cnts.txt")
Indpd5TZTable_mean_probing_cnts = np.loadtxt("./tmp/Indpd5TZTable_mean_probing_cnts.txt")

sorted_UnivMultShift = np.sort(UnivMultShift_mean_probing_cnts)
sorted_Indpd2MultShift = np.sort(Indpd2MultShift_mean_probing_cnts)
sorted_SimpleTabulation = np.sort(SimpleTabulation_mean_probing_cnts)
sorted_Indpd5TZTable = np.sort(Indpd5TZTable_mean_probing_cnts)
sorted_Indpd5MersennePrime = np.sort(Indpd5MersennePrime_mean_probing_cnts)

# Calculate the cumulative fraction
cumulative_fraction = np.arange(1, len(sorted_UnivMultShift) + 1) / len(sorted_UnivMultShift)

fig, ax = plt.subplots()
# Plot the cumulative fraction
plt.plot(sorted_UnivMultShift, cumulative_fraction, linestyle='-', color='b', label="univ-mult-shift")
plt.plot(sorted_Indpd2MultShift, cumulative_fraction, linestyle='-', color='purple', label="2-indep-mult-shift")
plt.plot(sorted_SimpleTabulation, cumulative_fraction, linestyle='-', color='r', label="simple-table")
plt.plot(sorted_Indpd5TZTable, cumulative_fraction, linestyle='-', color='orangered', label="5-indep-TZ-table")
plt.plot(sorted_Indpd5MersennePrime, cumulative_fraction, linestyle='-', color='g', label="5-indep-Mersenne-prime")
ax.set_xlim(0, 10)
ax.set_ylim(0, 1)
plt.xlabel("average probes per insert/delete")
plt.ylabel("cumulative fraction")
plt.title("Keys from hyper cube")
plt.legend()
plt.savefig("./tmp/hypercube_cumfrac_probes.png", dpi=300, bbox_inches="tight")
# plt.show()


UnivMultShift_mean_insert_nanosec = np.loadtxt("./tmp/UnivMultShift_mean_insert_nanosec.txt")
Indpd2MultShift_mean_insert_nanosec = np.loadtxt("./tmp/Indpd2MultShift_mean_insert_nanosec.txt")
Indpd5MersennePrime_mean_insert_nanosec = np.loadtxt("./tmp/Indpd5MersennePrime_mean_insert_nanosec.txt")
SimpleTabulation_mean_insert_nanosec = np.loadtxt("./tmp/SimpleTabulation_mean_insert_nanosec.txt")
Indpd5TZTable_mean_insert_nanosec = np.loadtxt("./tmp/Indpd5TZTable_mean_insert_nanosec.txt")

sorted_nano_UnivMultShift = np.sort(UnivMultShift_mean_insert_nanosec)
sorted_nano_Indpd2MultShift = np.sort(Indpd2MultShift_mean_insert_nanosec)
sorted_nano_SimpleTabulation = np.sort(SimpleTabulation_mean_insert_nanosec)
sorted_nano_Indpd5TZTable = np.sort(Indpd5TZTable_mean_insert_nanosec)
sorted_nano_Indpd5MersennePrime = np.sort(Indpd5MersennePrime_mean_insert_nanosec)

# Calculate the cumulative fraction
cumulative_fraction = np.arange(1, len(sorted_nano_UnivMultShift) + 1) / len(sorted_nano_UnivMultShift)

fig, ax = plt.subplots()
# Plot the cumulative fraction
plt.plot(sorted_nano_UnivMultShift, cumulative_fraction, linestyle='-', color='b', label="univ-mult-shift")
plt.plot(sorted_nano_Indpd2MultShift, cumulative_fraction, linestyle='-', color='purple', label="2-indep-mult-shift")
plt.plot(sorted_nano_SimpleTabulation, cumulative_fraction, linestyle='-', color='r', label="simple-table")
plt.plot(sorted_nano_Indpd5TZTable, cumulative_fraction, linestyle='-', color='orangered', label="5-indep-TZ-table")
plt.plot(sorted_nano_Indpd5MersennePrime, cumulative_fraction, linestyle='-', color='g', label="5-indep-Mersenne-prime")
ax.set_xlim(0, 150)
ax.set_ylim(0, 1)
plt.xlabel("average time per insert+delete cycle (nanoseconds)")
plt.ylabel("cumulative fraction")
plt.title("Keys from hyper cube")
plt.legend()
plt.savefig("./tmp/hypercube_cumfrac_nano.png", dpi=300, bbox_inches="tight")
# plt.show()


data = [
    ['univ-mult-shift'],
    ['2-indep-mult-shift'],
    ['simple-table'],
    ['5-indep-TZ-table'],
    ['5-indep-Mersenne-prime'],
]
meantimes = np.loadtxt("./tmp/mean_hash_time.txt")
for i in range(5):
    data[i].append(meantimes[i])
columns = ['hashing scheme', 'update time (nanoseconds)']
fig, ax = plt.subplots()
ax.axis('off')
table = ax.table(cellText=data, colLabels=columns, loc='center')
plt.savefig("./tmp/mean_hash_time.png", dpi=300, bbox_inches="tight")
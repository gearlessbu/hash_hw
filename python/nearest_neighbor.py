import numpy as np
import time

from KDTree import KDTree
from LSH import LSH
from utils import read_fvecs

np.random.seed(42)

def compare_KDTree_and_LSH(sample_num=1):
    file_path = "./datasets/{}/{}_base.fvecs".format("sift", "sift")
    vectors = read_fvecs(file_path)
    dim = vectors.shape[1]
    lsh = LSH(vectors, 64)
    start_time = time.time()
    tree = KDTree(vectors)
    print("KDTree building time: {} seconds".format(time.time() - start_time))
    probe = np.random.rand(dim,) * (np.linalg.norm(vectors[0]) + np.linalg.norm(vectors[10] + np.linalg.norm(vectors[20])))\
        / 3 / np.sqrt(dim) * 2.4
    
    LSH_time, KDTree_time, c = 0., 0., 0.

    for _ in range(sample_num):
        probe = np.random.rand(dim,) * (np.linalg.norm(vectors[0]) + np.linalg.norm(vectors[10] + np.linalg.norm(vectors[20])))\
            / 3 / np.sqrt(dim) * 0.4
        # probe = vectors[np.random.randint(0, vectors.shape[0])] * (1 + 0.3 * np.random.rand(dim,))

        # LSH
        start_time = time.time()
        hamming_distances = lsh.hamming_distances(probe)
        nearest_point_idx = np.argsort(hamming_distances)[0]
        distance_LSH = np.linalg.norm(probe - vectors[nearest_point_idx])
        LSH_time += time.time() - start_time
        # print("LSH time: {} seconds".format(time.time() - start_time))

        # KDTree
        start_time = time.time()
        distance, nearest_point = tree.nearest_neighbor(probe)
        KDTree_time += time.time() - start_time
        # print("KDTree time: {} seconds".format(time.time() - start_time))

        # print("c=", distance_LSH / distance)
        c += distance_LSH / distance

    print("LSH mean time: {} seconds".format(LSH_time / sample_num))
    print("KDTree mean time: {} seconds".format(KDTree_time / sample_num))
    print("LSH mean approx rate time: {} seconds".format(KDTree_time / sample_num))

compare_KDTree_and_LSH(20)
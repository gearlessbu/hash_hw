import numpy as np
import warnings
import time
from metrics import compute_map

np.random.seed(42)

class LSH:
    def __init__(self, xs:np.ndarray, L) -> None:
        self.dim = xs.shape[1]
        self.L = L
        start_time = time.time()
        # p = 2 for p-stable
        self.projs_w = np.random.randn(self.L, self.dim)
        print("Training time: {} seconds".format(time.time() - start_time))
        start_time = time.time()
        self.database = np.zeros((xs.shape[0], L), dtype=np.int32)
        for i in range(xs.shape[0]):
            self.database[i] = self.hash_method(xs[i])
        print("Database building time: {} seconds".format(time.time() - start_time))

    def hash_method(self, x):
        Hs = self.projs_w @ x
        return np.where(Hs >= 0., 1, 0)
    
    def hamming_distances(self, query):
        H = self.hash_method(query)
        distances = np.sum(H != self.database, axis=1)
        return distances

if __name__ == "__main__":
    dataset_name = "sift"
    data_query = np.load("../datasets/{}/{}_query_DSH.npy".format(dataset_name, dataset_name))
    data_base = np.load("../datasets/{}/{}_base_DSH.npy".format(dataset_name, dataset_name))
    gt = np.load("../datasets/{}/{}_gt_DSH.npy".format(dataset_name, dataset_name))
    # dsh = DSH(data_base, 64, 0.5, 5, 3)
    dsh = LSH(data_base, 96)
    map = compute_map(data_query, gt, dsh)
    print(map)

    # file_path = "../datasets/{}/{}_base.fvecs".format("sift", "sift")
    # vectors = read_fvecs(file_path)
    # dsh = DSH(vectors, 64)
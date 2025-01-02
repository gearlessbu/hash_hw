import numpy as np
import warnings
from utils import read_fvecs
from tqdm import tqdm

np.random.seed(42)

dataset_name = "sift"
dataset_name = "sift100k"
query_num = 1000

def compute_gt(query:np.ndarray, base:np.ndarray, proportion=0.02):
    k = int(proportion * base.shape[0])
    gt = []
    # for i in range(query_num):
    for i in tqdm(range(query_num)):
        distances = np.linalg.norm(base - query[i], axis=1)
        nearest_indices = np.argsort(distances)[:k]
        gt.append(nearest_indices)
    gt = np.array(gt)
    return gt

if __name__ == "__main__":
    # file_path = "../datasets/{}/{}_base.fvecs".format(dataset_name, dataset_name)
    file_path = "../datasets/{}/{}_base.fvecs".format("sift", "sift")
    vectors = read_fvecs(file_path)[:100000]
    print("Shape of vectors:", vectors.shape)
    indices = np.random.permutation(vectors.shape[0])
    data_query = vectors[indices[:query_num]]  # 选取前1000个
    data_base = vectors[indices[query_num:]]  # 选取剩下的9000个
    gt = compute_gt(data_query, data_base)
    # print(gt)
    np.save("../datasets/{}/{}_query_DSH".format(dataset_name, dataset_name), data_query)
    np.save("../datasets/{}/{}_base_DSH".format(dataset_name, dataset_name), data_base)
    np.save("../datasets/{}/{}_gt_DSH".format(dataset_name, dataset_name), gt)
import numpy as np
import warnings
from utils import read_fvecs
import time
from metrics import compute_map
from sklearn.cluster import KMeans
import scipy.io

np.random.seed(42)


def k_means_quantization_new(xs:np.ndarray, L, alpha, p=5):
    """
    k-means algorithm (sum of squared error), early stop after p iteration

    Args:
        xs: Array of points [points_num, points_dim]
        L: the code length
        alpha: parameter for k, k = L * alpha
        p: stop the k-means after p iterations

    Returns:
        center_points: final cluster representative points
        labels: cluster labels for each point
        cluster_sizes: The size of each cluster
    """
    k = int(L * alpha)
    kmeans = KMeans(k, max_iter=p).fit(xs)
    labels = kmeans.labels_
    cluster_sizes = np.array([np.sum(labels == i) for i in range(k)])
    print(np.sum(cluster_sizes))
    return kmeans.cluster_centers_, labels, cluster_sizes
    # data = scipy.io.loadmat('../mat/centers.mat')
    # labels = scipy.io.loadmat('../mat/labels.mat')
    # cluster_centers = data['U']
    # labels = labels['dump']
    # cluster_sizes = np.array([np.sum(labels == i) for i in range(1, 97)])
    # print(cluster_centers.shape, np.sum(cluster_sizes), labels.shape)
    # return cluster_centers, None, cluster_sizes

def r_nearest_neighbors_matrix(points:np.ndarray, r):
    """
    compute the r-nearest neighbors matrix W

    Args:
        points: actually the center points in DSH
        r: parameter

    Returns:
        W: r-nearest neighbors matrix
    """
    points_num, _ = points.shape
    W = np.zeros((points_num, points_num), dtype=int)
    distances = np.linalg.norm(points[:, np.newaxis, :] - points[np.newaxis, :, :], axis=2)
    Dr = []
    for i in range(points_num):
        nearest_indices = np.argsort(distances[i])[1:r+1].astype(np.int32)
        W[i, nearest_indices] = 1
        Dr = Dr + [(i, int(idx)) if i < idx else (int(idx), i) for idx in nearest_indices]
        # print(i, "::", nearest_indices)
        W[nearest_indices, i] = 1
    # print(len(set(Dr)))
    # print(set(Dr))

    return W

def dens_sensitive_proj_gen(center_points:np.ndarray, r):
    """
    generate the median plane between the centers of adjacent groups

    Args:
        center_points: center points from k-means
        r: parameter for r-nearest neighbors matrix

    Returns:
        projs: list of the projection w and intercept t
    """
    center_points_num, _ = center_points.shape
    W = r_nearest_neighbors_matrix(center_points, r)
    projs = []
    # for i in range(center_points_num - 1):
    #     for j in range(i + 1, center_points_num):
    for i in range(center_points_num):
        for j in range(center_points_num):
            if W[i, j] == 1 and i > j:
                w = center_points[i] - center_points[j]
                t = 0.5 * (center_points[i] + center_points[j]).dot(center_points[i] - center_points[j])
                projs.append([w, t])
    return projs

def dens_sensitive_proj_gen_new(center_points:np.ndarray, r, cluster_sizes:np.ndarray, L):
    center_points_num, _ = center_points.shape
    weights = cluster_sizes / np.sum(cluster_sizes)
    distances = np.square(np.linalg.norm(center_points[:, np.newaxis, :] - center_points[np.newaxis, :, :], axis=2))
    print(center_points[0])
    print(distances)
    Dr = np.zeros((center_points_num, r))
    distances += 1e9 * np.identity(center_points_num)
    for i in range(center_points_num):
        tmp = distances[i]
        tmpsort = np.sort(tmp)
        Dr[i] = tmpsort[:r]
    Dr = np.unique(Dr)
    print(np.size(Dr))
    Dr = np.sort(Dr)
    print(Dr)
    bitsize = np.zeros_like(Dr)
    for i in range(len(Dr)):
        id1, id2 = np.where(distances == Dr[i])[0]
        # print(id1, id2)
        tmp1 = (center_points[id1] + center_points[id2]) / 2.0
        tmp2 = (center_points[id1] - center_points[id2])
        tmp3 = np.matlib.repmat(tmp1, center_points_num, 1)
        DD = center_points @ tmp2
        th = tmp3 @ tmp2
        # pnum = find(DD > th);
        tmpnum = weights[DD > th]
        num1 = sum(tmpnum)
        num2 = 1 - num1
        bitsize[i] = min(num1, num2) / max(num1, num2)
    Dsorts = np.sort(bitsize)
    print(Dsorts)

def entropy_based_proj_select(projs:list, center_points:np.ndarray, cluster_sizes:np.ndarray, L):
    """
    select the candidate projections with largest entropy

    Args:
        projs: the candidate projections, around 0.5 * alpha * r * L candidate projections
        r: parameter for r-nearest neighbors matrix

    Returns:
        projs: list of the projection w and intercept t
    """
    candidate_num = len(projs)
    print("The number of candidate projections is {}.".format(candidate_num))
    if candidate_num < L:
        warnings.warn("Less the candidate projections than L")
        return projs
    weights = cluster_sizes / np.sum(cluster_sizes)
    entropies = []
    for i in range(candidate_num):
        w, t = projs[i]
        hs = center_points @ w - t
        # print(hs.shape, center_points.shape)
        Pi0 = np.sum(weights[hs < 0.])
        Pi1 = np.sum(weights[hs >= 0.])
        # if Pi0 == 0.:
        #     entropy = - Pi1 * np.log(Pi1)
        # elif Pi1 == 0.:
        #     entropy = - Pi0 * np.log(Pi0)
        # else:
        #     entropy = - Pi0 * np.log(Pi0) - Pi1 * np.log(Pi1)
        # entropies.append(entropy)
        # entropies.append(np.min([Pi0, Pi1]))
        entropies.append(np.min([Pi0, Pi1]) / np.max([Pi0, Pi1]))
    # print(np.sort(entropies))
    
    top_L_with_indices = sorted(range(candidate_num), key=lambda i: entropies[i], reverse=True)[:L]
    top_L_projs = [projs[idx] for idx in top_L_with_indices]
    # print(top_L_projs)
    return top_L_projs

class DSH:
    def __init__(self, xs:np.ndarray, L, alpha=1.5, r=3, p=3) -> None:
        # self.projs = None
        self.L = L
        start_time = time.time()
        center_points, _, cluster_sizes = k_means_quantization_new(xs, L, alpha, p)
        print("kmeans time: {} seconds".format(time.time() - start_time))
        start_time = time.time()
        projs = dens_sensitive_proj_gen(center_points, r)
        self.projs = entropy_based_proj_select(projs, center_points, cluster_sizes, L)
        # projs = dens_sensitive_proj_gen_new(center_points, r, cluster_sizes, L)
        self.projs_w = np.array([proj[0] for proj in self.projs])
        self.projs_t = np.array([proj[1] for proj in self.projs])
        print(self.projs_w.shape, self.projs_t.shape)
        print("Training time: {} seconds".format(time.time() - start_time))
        start_time = time.time()
        self.database = np.zeros((xs.shape[0], L), dtype=np.int32)
        for i in range(xs.shape[0]):
            self.database[i] = self.hash_method(xs[i])
        print("Database building time: {} seconds".format(time.time() - start_time))

    def hash_method(self, x):
        Hs = self.projs_w @ x - self.projs_t
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
    dsh = DSH(data_base, 96, p=3)
    map = compute_map(data_query, gt, dsh)
    print(map)

    # file_path = "../datasets/{}/{}_base.fvecs".format("sift", "sift")
    # vectors = read_fvecs(file_path)
    # dsh = DSH(vectors, 64)
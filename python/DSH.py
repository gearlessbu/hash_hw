import numpy as np
import warnings
from utils import read_fvecs
import time
from metrics import compute_map
from sklearn.cluster import KMeans

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
    return kmeans.cluster_centers_, labels, cluster_sizes

def k_means_quantization(xs:np.ndarray, L, alpha, p=5):
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
    points_num, _ = xs.shape
    center_points = xs[np.random.choice(points_num, k, replace=False)]

    for iteration in range(p):
        # distances = np.linalg.norm(xs[:, np.newaxis, :] - center_points[np.newaxis, :, :], axis=2)
        # labels = np.argmin(distances, axis=1)
        
        labels = np.zeros((points_num,), dtype=np.int32)
        bs = 100000
        for i in range(points_num // bs):
            print(i)
            end_p = (i + 1) * bs if i < points_num // bs - 1 else points_num
            distances = np.linalg.norm(xs[i * bs:end_p, np.newaxis, :] - center_points[np.newaxis, :, :], axis=2)
            labels[i * bs:end_p] = np.argmin(distances, axis=1)


            # distances = np.linalg.norm(xs[i * bs:(i + 1) * bs, np.newaxis, :] - center_points[np.newaxis, :, :], axis=2)
            # labels[i * 10:(i + 1) * 10] = np.argmin(distances, axis=1)
        # for i in range(points_num):
        #     distances = np.linalg.norm(xs[i] - center_points, axis=1)
        #     labels[i] = np.argmin(distances, axis=0)
        new_center_points = np.array([xs[labels == i].mean(axis=0) if np.any(labels == i) else center_points[i] for i in range(k)])

        if np.allclose(new_center_points, center_points):
            print(f"Converged after {iteration + 1} iterations.")
            break

        center_points = new_center_points

    cluster_sizes = np.array([np.sum(labels == i) for i in range(k)])

    return center_points, labels, cluster_sizes

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

    for i in range(points_num):
        nearest_indices = np.argsort(distances[i])[1:r+1]
        W[i, nearest_indices] = 1
        W[nearest_indices, i] = 1

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
    for i in range(center_points_num - 1):
        for j in range(i + 1, center_points_num):
            if W[i, j] == 1:
                w = center_points[i] - center_points[j]
                t = 0.5 * (center_points[i] + center_points[j]).dot(center_points[i] - center_points[j])
                projs.append([w, t])
    return projs

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
        hs = center_points @ w + t
        # print(hs.shape, center_points.shape)
        Pi0 = np.sum(weights[hs < 0.])
        Pi1 = np.sum(weights[hs >= 0.])
        if Pi0 == 0.:
            entropy = - Pi1 * np.log(Pi1)
        elif Pi1 == 0.:
            entropy = - Pi0 * np.log(Pi0)
        else:
            entropy = - Pi0 * np.log(Pi0) - Pi1 * np.log(Pi1)
        entropies.append(entropy)
    
    top_L_with_indices = sorted(range(candidate_num), key=lambda i: entropies[i], reverse=True)[:L]
    top_L_projs = [projs[idx] for idx in top_L_with_indices]
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
        self.projs_w = np.array([proj[0] for proj in self.projs])
        self.projs_t = np.array([proj[1] for proj in self.projs])
        print(self.projs_w.shape, self.projs_t.shape)
        print("Training time: {} seconds".format(time.time() - start_time))
        start_time = time.time()
        self.database = np.zeros((xs.shape[0], L), dtype=np.int32)
        for i in range(xs.shape[0]):
            self.database[i] = self.hash_method(xs[i])
        print("Database building time: {} seconds".format(time.time() - start_time))
        # print(self.database)

    def hash_method(self, x):
        # H = np.zeros((self.L,))
        # for i in range(self.L):
        #     H[i] = int(self.projs[i][0].dot(x) + self.projs[i][1] >= 0.)
        # return H
        Hs = self.projs_w @ x + self.projs_t
        return np.where(Hs >= 0., 1, 0)
    
    def hamming_distances(self, query):
        H = self.hash_method(query)
        distances = np.sum(H != self.database, axis=1)
        return distances

# def DSH(xs:np.ndarray, L, alpha, r, p=5):
#     center_points, _, cluster_sizes = k_means_quantization(xs, L, alpha, p)
#     projs = dens_sensitive_proj_gen(center_points, r)
#     top_L_projs = entropy_based_proj_select(projs, center_points, cluster_sizes, L)

if __name__ == "__main__":
    # file_path = "../datasets/siftsmall/siftsmall_base.fvecs"
    # # file_path = "../datasets/sift/sift_base.fvecs"
    # vectors = read_fvecs(file_path)
    

    dataset_name = "sift"
    data_query = np.load("../datasets/{}/{}_query_DSH.npy".format(dataset_name, dataset_name))
    data_base = np.load("../datasets/{}/{}_base_DSH.npy".format(dataset_name, dataset_name))
    gt = np.load("../datasets/{}/{}_gt_DSH.npy".format(dataset_name, dataset_name))
    # dsh = DSH(data_base, 64, 0.5, 5, 3)
    dsh = DSH(data_base, 64)
    map = compute_map(data_query, gt, dsh)
    print(map)
    # print(vectors[0], vectors[2])
    # print(dsh.hamming_distances(vectors[0]))
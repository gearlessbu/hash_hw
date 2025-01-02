import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

def eu_dist2(X, Y=None, squared=False):
    """
    Compute the Euclidean distance between two matrices X and Y.

    Args:
        X: Matrix of size (N, D)
        Y: Matrix of size (M, D), or None (defaults to X)
        squared: If True, return squared distances

    Returns:
        Distance matrix of size (N, M)
    """
    if Y is None:
        Y = X
    distances = cdist(X, Y, metric='sqeuclidean' if squared else 'euclidean')
    return distances

def dsh_learn(X, maxbits):
    """
    DSH_learn: Training process in Density Sensitive Hashing

    Args:
        X: Data matrix (each row is a sample vector, normalized and centralized to zero mean)
        maxbits: Code length of hash codes

    Returns:
        model: A dictionary with projection vectors U and intercepts
        B: Binary codes for data points
        elapse: Training time in seconds
    """
    import time
    tmp_T = time.time()

    alpha = 1.5
    r = 3
    iterations = 3
    cluster = round(maxbits * alpha)

    # K-Means Clustering
    kmeans = KMeans(n_clusters=cluster, max_iter=iterations, n_init=10, random_state=42)
    dump = kmeans.fit_predict(X)
    U = kmeans.cluster_centers_

    Nsamples, Nfeatures = X.shape
    model = {
        "U": np.zeros((maxbits, Nfeatures)),
        "intercept": np.zeros(maxbits)
    }

    # Cluster sizes and normalization
    clusize = np.array([np.sum(dump == i) for i in range(U.shape[0])])
    clusize = clusize / np.sum(clusize)

    # Distance matrix
    Du = eu_dist2(U, squared=False)
    np.fill_diagonal(Du, np.inf)

    Dr = []
    for i in range(Du.shape[0]):
        tmpsort = np.sort(Du[i, :])[:r]
        Dr.extend(tmpsort)
    Dr = np.unique(Dr)

    # Calculate bitsize
    bitsize = []
    for d in Dr:
        id1, id2 = np.argwhere(Du == d)[0]
        tmp1 = (U[id1] + U[id2]) / 2.0
        tmp2 = (U[id1] - U[id2])
        DD = U @ tmp2
        th = tmp1 @ tmp2
        pnum = np.where(DD > th)[0]
        tmpnum = clusize[pnum]
        num1 = np.sum(tmpnum)
        num2 = 1 - num1
        bitsize.append(min(num1, num2) / max(num1, num2))

    bitsize = np.array(bitsize)
    Dsorts = np.sort(bitsize)[::-1]

    for i in range(maxbits):
        ids = np.argmax(bitsize)
        id1, id2 = np.argwhere(Du == Dr[ids])[0]
        Du[id1, id2] = np.inf
        Du[id2, id1] = np.inf
        bitsize[ids] = -np.inf

        model["U"][i] = U[id1] - U[id2]
        model["intercept"][i] = ((U[id1] + U[id2]) / 2.0) @ model["U"][i]

    # Generate binary codes
    res = np.tile(model["intercept"], (Nsamples, 1))
    Ym = X @ model["U"].T
    B = (Ym > res).astype(int)

    elapse = time.time() - tmp_T
    return model, B, elapse

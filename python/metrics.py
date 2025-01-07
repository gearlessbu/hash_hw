import numpy as np

def compute_map(queries, ground_truth, hash_model):
    """
    Compute Mean Average Precision (MAP) for a retrieval task.

    Args:
        queries (np.ndarray): Query points, shape (num_queries, dim).
        database (np.ndarray): Database points, shape (num_database, dim).
        ground_truth (list of lists): Each query's ground truth neighbors by index.
        hash_method (callable): A hashing method that computes rankings based on Hamming distance.

    Returns:
        float: The mean average precision (MAP).
    """
    num_queries = queries.shape[0]
    k = ground_truth.shape[1]
    # k = 1000
    ap_list = []

    for i, query in enumerate(queries):
        # Use hash_method to compute Hamming distance ranking
        # hamming_distances = hash_model.nearest_k(query, k)
        hamming_distances = hash_model.hamming_distances(query)
        ranked_indices = np.argsort(hamming_distances)[:k]  # Sort database indices by distance

        # Compute Precision@k for all relevant ground truth neighbors
        relevant = set(ground_truth[i])
        retrieved = 0
        precision_sum = 0

        for k, idx in enumerate(ranked_indices, 1):  # k starts from 1
            if idx in relevant:
                retrieved += 1
                precision_sum += retrieved / k

        # Compute AP for this query
        ap = precision_sum / len(relevant) if relevant else 0
        ap_list.append(ap)

    # Compute MAP
    return np.mean(ap_list) if ap_list else 0.0

def precision_and_recall(ground_truth:set, retrieved_neighbors_k):
    # True Positives
    true_positive = 0
    # for i, idx in enumerate(retrieved_neighbors_k, 1):  # k starts from 1
    for idx in retrieved_neighbors_k:
        if idx in ground_truth:
            true_positive += 1
    
    # Precision and Recall
    precision = true_positive / len(retrieved_neighbors_k)
    recall = true_positive / len(ground_truth)
    return precision, recall

def precision_and_recall_curve(queries, ground_truth, hash_model):
    """
    Compute Mean Average Precision (MAP) for a retrieval task.

    Args:
        queries (np.ndarray): Query points, shape (num_queries, dim).
        database (np.ndarray): Database points, shape (num_database, dim).
        ground_truth (list of lists): Each query's ground truth neighbors by index.
        hash_method (callable): A hashing method that computes rankings based on Hamming distance.

    Returns:
        float: The mean average precision (MAP).
    """
    num_queries = queries.shape[0]
    # k = ground_truth.shape[1]
    # k = 1000
    ap_list = []
    ks = [3, 5, 10, 100, 300, 700, 1000, 2000, 5000, 10000, 30000, 60000, 100000, 300000]
    precisions = []
    recalls = []

    for i, query in enumerate(queries):
        # Use hash_method to compute Hamming distance ranking
        # hamming_distances = hash_model.nearest_k(query, k)
        hamming_distances = hash_model.hamming_distances(query)
        ranked_indices = np.argsort(hamming_distances)  # Sort database indices by distance
        relevant = set(ground_truth[i])

        query_precision = []
        query_recall = []

        for k in ks:
            precision, recall = precision_and_recall(relevant, ranked_indices[:k])
            query_precision.append(precision)
            query_recall.append(recall)
        query_precision.append(len(relevant) / hamming_distances.shape[0])
        query_recall.append(1.0)

        precisions.append(query_precision)
        recalls.append(query_recall)

        # if i == 100: break

    # Compute MAP
    return np.mean(precisions, axis=0), np.mean(recalls, axis=0)
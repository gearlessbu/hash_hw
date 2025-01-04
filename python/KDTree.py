import numpy as np

class KDTree:
    def __init__(self, points, depth=0):
        # print(points)
        # self.points = points
        self.depth = depth
        self.left = None
        self.right = None
        self.point = None
        
        # if len(points) > 0:
            # k = len(points[0])
        if points.size > 0:
            k = points.shape[1]
            axis = depth % k
            # points_sorted = sorted(points, key=lambda x: x[axis])
            points_sorted = points[np.argsort(points[:, axis]), :]
            
            median = len(points_sorted) // 2
            self.point = points_sorted[median]
            
            self.left = KDTree(points_sorted[:median], depth + 1)
            self.right = KDTree(points_sorted[median + 1:], depth + 1)
        
    def nearest_neighbor(self, point, best=None, exlude_self=True):
        if best is None:
            best = (float('inf'), None)

        if self.point is None:
            return best
        
        dist = np.linalg.norm(np.array(self.point) - np.array(point))
        
        if dist < best[0] and (dist > 1e-8 or not exlude_self):
            best = (dist, self.point)
        
        k = len(point)  # dim
        axis = self.depth % k  # separation axis for the current point
        diff = point[axis] - self.point[axis]
        
        if diff < 0:
            if self.left:
                best = self.left.nearest_neighbor(point, best, exlude_self)
            if self.right and abs(diff) < best[0]:
                best = self.right.nearest_neighbor(point, best, exlude_self)
        else:
            if self.right:
                best = self.right.nearest_neighbor(point, best, exlude_self)
            if self.left and abs(diff) < best[0]:
                best = self.left.nearest_neighbor(point, best, exlude_self)
        
        return best

if __name__ == "__main__":
    dim = 128
    # points = np.random.rand(1000000, dim)
    points = np.array([
        [1, 2],
        [3, 4],
        [5, 1],
        [7, 8],
        [6, 2]
    ])

    tree = KDTree(points)

    query_point = np.random.rand(dim,)
    query_point = np.array([5, 1])
    distance, nearest_point = tree.nearest_neighbor(query_point)

    print(f"Query point: {query_point}")
    print(f"Nearest neighbor: {nearest_point}")
    print(f"Distance: {distance}")

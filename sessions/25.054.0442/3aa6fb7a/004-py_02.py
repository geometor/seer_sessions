"""
1.  **Identify Clusters:** Find all distinct clusters of '8' (azure) pixels in the input grid. A cluster is a group of orthogonally connected '8' pixels.
2.  **Find Cluster Center:** For each cluster:
    *   Calculate the centroid of the cluster (average row and average column of all pixels in the cluster).
    *   Identify all pixels within the cluster that are closest to the centroid (using Euclidean distance).
    *    Among the closest pixels, select the one with the smallest row index. If there's a tie, select the one with the smallest column index (prioritize top-left).
3.  **Replace Pixel:** Change the value of the selected center pixel in each cluster from '8' (azure) to '1' (blue).
4.  **Preserve Other Pixels:** All other pixels in the grid remain unchanged.
"""

import numpy as np

def find_clusters(grid, value):
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    def dfs(row, col, current_cluster):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != value):
            return
        visited[row, col] = True
        current_cluster.append((row, col))
        dfs(row + 1, col, current_cluster)
        dfs(row - 1, col, current_cluster)
        dfs(row, col + 1, current_cluster)
        dfs(row, col - 1, current_cluster)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == value and not visited[row, col]:
                current_cluster = []
                dfs(row, col, current_cluster)
                clusters.append(current_cluster)
    return clusters

def find_center(cluster):
    # find the centermost pixel, prioritizing the pixel closer to the top left
    rows = [p[0] for p in cluster]
    cols = [p[1] for p in cluster]

    # Calculate the centroid
    centroid_row = sum(rows) / len(rows)
    centroid_col = sum(cols) / len(cols)

    # Find the point in the cluster closest to the centroid
    min_dist = float('inf')
    closest_pixels = []
    for row, col in cluster:
        dist = (row - centroid_row)**2 + (col - centroid_col)**2
        if dist < min_dist:
            min_dist = dist
            closest_pixels = [(row, col)]
        elif dist == min_dist:
            closest_pixels.append((row, col))

    # Prioritize top-left among closest pixels
    if len(closest_pixels) > 1:
        closest_pixels.sort(key=lambda x: (x[0], x[1]))
    return closest_pixels[0]


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    # find clusters of 8s
    clusters = find_clusters(output_grid, 8)
    # replace center of each cluster with 1s
    for cluster in clusters:
        center = find_center(cluster)
        output_grid[center] = 1

    return output_grid
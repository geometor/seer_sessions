# 3aa6fb7a • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Clusters:** Locate all distinct clusters of '8' (azure) pixels within the input grid. A cluster is defined as a contiguous group of '8' pixels, where contiguity includes orthogonal neighbors.
2.  **Find Center:** For each identified cluster, determine a "center" pixel. There will be one center per cluster.
3.  **Replace Pixel:** Within each cluster, change the value of *one* of the '8' pixels in the center, from '8' to '1' (blue).
4.  **Maintain Other Pixels:** All other pixels in the grid that are not part of the identified cluster of 8, or those pixels of 8 which were not selected, retain their original values.
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
    center = None
    for row, col in cluster:
        dist = (row - centroid_row)**2 + (col - centroid_col)**2
        if dist < min_dist:
            min_dist = dist
            center = (row, col)
    return center

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
```

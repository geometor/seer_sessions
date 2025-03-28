# 3aa6fb7a • 002 • example_1 • investigate_coder

---
```python
"""
Transforms the input grid by changing one pixel in each azure (8) cluster to blue (1).
The changed pixel's location varies: (1,0) in top-left, and (0,1) in bottom-right.
"""

import numpy as np

def find_clusters(grid, color):
    """
    Finds clusters of a specific color in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    def dfs(row, col, current_cluster):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_cluster.append((row, col))
        dfs(row + 1, col, current_cluster)
        dfs(row - 1, col, current_cluster)
        dfs(row, col + 1, current_cluster)
        dfs(row, col - 1, current_cluster)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_cluster = []
                dfs(row, col, current_cluster)
                clusters.append(current_cluster)
    return clusters

def get_cluster_top_left(cluster):
    """
    Returns the top-left coordinate of a cluster.
    """
    min_row = min(coord[0] for coord in cluster)
    min_col = min(coord[1] for coord in cluster)
    return (min_row, min_col)

def transform(input_grid):
    """
    Transforms the input grid based on the observed rule.
    """
    output_grid = np.copy(input_grid)
    azure_clusters = find_clusters(input_grid, 8)

    for cluster in azure_clusters:
        top_left = get_cluster_top_left(cluster)
        # Determine relative position based on top-left.
        if top_left[0] < input_grid.shape[0] / 2 and top_left[1] < input_grid.shape[1] / 2: # Top-left
          change_pixel = (top_left[0] + 1, top_left[1])
        elif top_left[0] > input_grid.shape[0] / 2 and top_left[1] > input_grid.shape[1] / 2:   # assumed Bottom-right
          change_pixel = (top_left[0] , top_left[1]+1)
        else:
          continue

        if 0 <= change_pixel[0] < output_grid.shape[0] and 0 <= change_pixel[1] < output_grid.shape[1]:
            output_grid[change_pixel] = 1

    return output_grid
```

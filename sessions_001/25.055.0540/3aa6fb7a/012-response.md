# 1-3aa6fb7a • 012 • refine_coder

---
```python
"""
Identifies clusters of azure (8) pixels in the input grid and changes
the color of all pixels in the column of the left-most azure pixel in the
vertical middle of each cluster to blue (1), but only for the rows that are
part of the cluster.
"""

import numpy as np

def get_clusters(grid, color):
    """
    Finds clusters of connected pixels with the specified color.
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

def find_target_column(cluster):
    """
    Finds the column index of the left-most pixel in the vertical middle of a cluster.
    """
    if not cluster:
        return None

    # Find min and max row
    min_row = min(p[0] for p in cluster)
    max_row = max(p[0] for p in cluster)

    # Calculate vertical middle
    vertical_mid = (min_row + max_row) // 2

    # Get all pixels in the middle row
    middle_pixels = [p for p in cluster if p[0] == vertical_mid]

    # Sort middle pixels by column to find the left-most and return its column
    if middle_pixels:
        leftmost_pixel = sorted(middle_pixels, key=lambda x: x[1])[0]
        return leftmost_pixel[1], min_row, max_row
    else:
        return None, None, None


def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)

    # Find clusters of azure pixels
    azure_clusters = get_clusters(input_grid, 8)

    # Find and change color of the target pixels in each cluster
    for cluster in azure_clusters:
        target_column, min_row, max_row = find_target_column(cluster)
        if target_column is not None:
            # Change color of all pixels in the target column within the cluster's vertical extent
            for row in range(min_row, max_row + 1):
                if (row, target_column) in cluster:
                    output_grid[row, target_column] = 1

    return output_grid
```


# a87f7484 • 012 • refine_coder

---
```python
"""
1.  **Identify Key Color:** The key color is orange (7).

2.  **Locate Orange Clusters:** Find all contiguous clusters (horizontal or vertical) of orange pixels in the input grid.

3.  **Calculate Cluster Centers:** For each orange cluster, compute its center coordinates (row, col) by averaging the row and column indices of all pixels in the cluster.

4.  **Select Cluster:**
    *   If no orange clusters, return a blank grid of the correct output size.
    *   If there is only 1, select it.
    *   If there are multiple, choose the cluster with the *lowest* row index.
    *   If multiple are at that row index, use the lowest column of these.

5.  **Extract Subgrid:** Extract a subgrid from the input grid, centered at the selected cluster center. The dimensions of the subgrid are equal to the dimensions of the output grid given in the training example.

6.  **Return Subgrid:** The extracted subgrid is the output.
"""

import numpy as np

def get_clusters(grid, key_color):
    """
    Finds clusters of the key color in the grid.
    Returns a list of (row, col) tuples representing the center of each cluster.
    """
    visited = set()
    clusters = []

    def dfs(row, col):
        """Depth-first search to find connected components."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or grid[row, col] != key_color
            or (row, col) in visited
        ):
            return []

        visited.add((row, col))
        cluster_pixels = [(row, col)]

        cluster_pixels.extend(dfs(row + 1, col))
        cluster_pixels.extend(dfs(row - 1, col))
        cluster_pixels.extend(dfs(row, col + 1))
        cluster_pixels.extend(dfs(row, col - 1))
        return cluster_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == key_color and (row, col) not in visited:
                cluster_pixels = dfs(row, col)
                if cluster_pixels:
                    # Calculate the center of the cluster
                    rows, cols = zip(*cluster_pixels)
                    center_row = int(np.mean(rows))
                    center_col = int(np.mean(cols))
                    clusters.append((center_row, center_col))
    return clusters

def select_cluster(clusters):
    """Selects the cluster based on the lowest row, then lowest col."""
    if not clusters:
        return None
    return min(clusters, key=lambda x: (x[0], x[1]))

def transform(input_grid, output_shape):
    input_grid = np.array(input_grid)
    key_color = 7

    # Locate Orange Clusters and Calculate Cluster Centers
    clusters = get_clusters(input_grid, key_color)

    # Select Cluster
    selected_center = select_cluster(clusters)

    # if no key color present, return a blank grid of the output_shape
    if selected_center is None:
        return np.zeros(output_shape, dtype=int)

    center_row, center_col = selected_center

    # Extract Subgrid
    start_row = center_row - (output_shape[0] - 1 )// 2
    start_col = center_col - (output_shape[1] - 1) // 2
    end_row = center_row + (output_shape[0] + 2)// 2
    end_col = center_col + (output_shape[1] + 2) // 2
    output_grid = np.zeros(output_shape, dtype=int)

    for i in range(output_shape[0]):
        for j in range(output_shape[1]):
            input_row = start_row + i
            input_col = start_col + j
            if 0 <= input_row < input_grid.shape[0] and 0 <= input_col < input_grid.shape[1]:
                output_grid[i, j] = input_grid[input_row, input_col]

    return output_grid
```

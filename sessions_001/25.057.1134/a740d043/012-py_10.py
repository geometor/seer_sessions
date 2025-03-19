"""
1.  **Identify Clusters:** Find all contiguous clusters of non-blue pixels (red or green) in the input grid.  Pixels are considered part of the same cluster if they are directly adjacent (up, down, left, or right), not diagonal.
2.  **Create Separate Outputs:** For each cluster found in the input
3.  **Extract Clusters:** For each cluster:
    *   Determine its bounding box (the smallest rectangle that fully encloses the cluster).
    *   Copy the cluster's pixels, maintaining their original colors and relative positions *within* the cluster.
4.  **Create Output Grid:**
    * Create a new grid of zeros (white background). The height is determined by the height of each cluster.
5.  **Place Cluster:** Place the extracted cluster into the output grid, aligning it to the top-left.
6. **Output:** Return a list of output grids, one for each cluster.
"""

import numpy as np

def find_clusters(grid):
    # Find clusters of adjacent non-blue pixels
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    def dfs(r, c, cluster_colors):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] == 1):
            return []

        visited[r, c] = True
        cluster_colors.add(grid[r,c])
        current_cluster = [(r, c, grid[r, c])]

        current_cluster.extend(dfs(r + 1, c, cluster_colors))
        current_cluster.extend(dfs(r - 1, c, cluster_colors))
        current_cluster.extend(dfs(r, c + 1, cluster_colors))
        current_cluster.extend(dfs(r, c - 1, cluster_colors))
        return current_cluster

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 1 and not visited[r, c]:
                cluster_colors = set()
                cluster = dfs(r, c, cluster_colors)
                if cluster:
                    clusters.append(cluster)
    return clusters

def get_cluster_bounds(cluster):
    # find min and max row and col
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for r, c, _ in cluster:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find clusters
    clusters = find_clusters(input_grid)
    output_grids = []

    # Iterate through clusters
    for cluster in clusters:
        # Get cluster bounds
        min_r, min_c, max_r, max_c = get_cluster_bounds(cluster)
        
        # Create output grid (white background)
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        output_grid = np.zeros((height, width), dtype=int)

        # Copy cluster pixels to output grid
        for r, c, val in cluster:
            output_grid[r - min_r, c - min_c] = val

        output_grids.append(output_grid.tolist()) # Append to list of outputs

    return output_grids
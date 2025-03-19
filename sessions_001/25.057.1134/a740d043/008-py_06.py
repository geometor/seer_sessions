"""
Identify clusters of non-blue pixels (green and red). Extract these clusters, 
maintaining their relative positions, and represent them in a new output grid. 
Change the background from blue (1) to white (0).
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

    # Initialize output grid with background color white (0)
    output_grid = np.zeros((len(clusters),3), dtype=int)

    # Iterate through clusters
    for i, cluster in enumerate(clusters):
        # Get cluster color values
        min_r, min_c, _, _ = get_cluster_bounds(cluster)
        for r, c, val in cluster:
            output_grid[i, c-min_c] = val

    return output_grid.tolist()
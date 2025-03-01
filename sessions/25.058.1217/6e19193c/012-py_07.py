"""
The transformation rule involves identifying maroon (9) pixel clusters in the input grid and reflecting them across either the horizontal or vertical centerline of the grid, depending on the cluster's position and shape. The original maroon clusters are preserved. The background pixels (non-maroon) are also copied directly from the input to the output.
"""

import numpy as np

def find_clusters(grid, color):
    visited = set()
    clusters = []

    def dfs(r, c, current_cluster):
        if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
            return
        visited.add((r, c))
        current_cluster.append((r, c))
        dfs(r + 1, c, current_cluster)
        dfs(r - 1, c, current_cluster)
        dfs(r, c + 1, current_cluster)
        dfs(r, c - 1, current_cluster)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def reflect_horizontal(cluster, grid_shape):
    new_cluster = []
    for r, c in cluster:
        new_r = grid_shape[0] - 1 - r
        new_c = c
        new_cluster.append((new_r, new_c))
    return new_cluster

def reflect_vertical(cluster, grid_shape):
  new_cluster = []
  for r,c in cluster:
    new_r = r
    new_c = grid_shape[1] - 1 - c
    new_cluster.append((new_r, new_c))
  return new_cluster


def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = input_grid.copy()

    # Find maroon clusters
    maroon_clusters = find_clusters(input_grid, 9)

    # Apply reflection for each cluster
    for cluster in maroon_clusters:
        # Determine reflection axis based on cluster properties
        rows, cols = zip(*cluster)
        is_horizontal = len(set(rows)) == 1
        is_vertical = len(set(cols)) == 1
        
        if is_horizontal:
            transformed_cluster = reflect_horizontal(cluster, input_grid.shape)
        elif is_vertical:
            transformed_cluster = reflect_vertical(cluster, input_grid.shape)
        else: # if not horizontal or vertical, pick center row and reflect over
            transformed_cluster = reflect_horizontal(cluster, input_grid.shape)

        # add to output
        for r, c in transformed_cluster:
            output_grid[r, c] = 9

    return output_grid
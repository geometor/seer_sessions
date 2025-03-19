"""
Identifies clusters of azure (8) pixels in the input grid and changes
specific azure pixels within each cluster to blue (1). The changed pixel
is the left-most pixel, vertically in the middle of a cluster.
"""

import numpy as np

def get_clusters(grid, color):
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

def find_leftmost_middle_pixel(cluster):
    # Sort by column (leftmost first) and then by row
    sorted_cluster = sorted(cluster, key=lambda x: (x[1], x[0]))

    #find min and max row
    min_row = min(p[0] for p in sorted_cluster)
    max_row = max(p[0] for p in sorted_cluster)

    if (max_row-min_row + 1) %2 == 1:
      vertical_mid = (min_row+max_row)//2
    else:
      vertical_mid = (min_row+max_row)//2

    for p in sorted_cluster:
      if p[0] == vertical_mid:
          return p

    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find clusters of azure pixels
    azure_clusters = get_clusters(input_grid, 8)

    # find and change color
    for cluster in azure_clusters:
        target_pixel = find_leftmost_middle_pixel(cluster)
        if target_pixel:
          output_grid[target_pixel[0], target_pixel[1]] = 1
    return output_grid
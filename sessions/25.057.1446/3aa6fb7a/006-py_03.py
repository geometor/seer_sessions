"""
Transforms the input grid by changing one pixel in each azure (8) cluster to blue (1).
The changed pixel is the right-most pixel of the top row if the cluster spans only one or two rows. If the cluster spans more than two rows, the right-most pixel of the bottom row is changed.
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

def get_cluster_top_rightmost(cluster):
    """
    Finds the right-most pixel in the top row of a cluster.
    """
    top_row = min(pixel[0] for pixel in cluster)
    top_row_pixels = [pixel for pixel in cluster if pixel[0] == top_row]
    rightmost_pixel = max(top_row_pixels, key=lambda x: x[1])
    return rightmost_pixel
  
def get_cluster_bottom_rightmost(cluster):
    """
    Finds the right-most pixel in the bottom row of a cluster.
    """
    bottom_row = max(pixel[0] for pixel in cluster)
    bottom_row_pixels = [pixel for pixel in cluster if pixel[0] == bottom_row]
    rightmost_pixel = max(bottom_row_pixels, key=lambda x: x[1])
    return rightmost_pixel

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find azure clusters
    azure_clusters = find_clusters(input_grid, 8)

    # change output pixels
    for cluster in azure_clusters:
        # determine row span of the cluster
        rows = set([pixel[0] for pixel in cluster])
        row_span = len(rows)
        
        # Get the right-most pixel on the top or bottom row based on row span
        if row_span <= 2:
            change_pixel = get_cluster_top_rightmost(cluster)
        else:
           # find rightmost pixel on *bottom* row
            change_pixel = get_cluster_bottom_rightmost(cluster)

        output_grid[change_pixel] = 1

    return output_grid
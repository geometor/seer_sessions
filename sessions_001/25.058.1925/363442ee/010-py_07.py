"""
The transformation replicates the top-left 3x3 colored cluster of the input grid (containing red, green, and orange pixels) and arranges these replications to fill the output grid, effectively replacing the grey area. The blue pixels in the input are ignored.
"""

import numpy as np

def get_top_left_cluster(grid):
    """Extracts the 3x3 top-left cluster from the input grid."""
    return grid[:3, :3]

def transform(input_grid):
    """Transforms the input grid by replicating the top-left cluster."""

    # Initialize output grid with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)

    # Get the 3x3 top-left cluster.
    cluster = get_top_left_cluster(input_grid)
    rows_cluster, cols_cluster = cluster.shape

    #find grey background in input
    rows, cols = input_grid.shape
    
    # Replicate and position the cluster horizontally and vertically
    for i in range(0, rows, rows_cluster):
        for j in range(0, cols, cols_cluster):
             for x in range(rows_cluster):
                 for y in range(cols_cluster):
                    if i + x < rows and j + y < cols:
                      if cluster[x,y] != 0:  #dont copy if grey
                         output_grid[i + x, j + y] = cluster[x, y]

    return output_grid
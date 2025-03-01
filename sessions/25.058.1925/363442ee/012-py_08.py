"""
The input grid's top-left 3x3 cluster (containing orange, red, and green pixels) is replicated across the entire output grid. The output grid maintains the same dimensions as the input grid. Transparent pixels (value 0) within the 3x3 cluster are not copied during replication.
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
"""
1.  **Identify the Cluster:** Find the smallest rectangular region (cluster) enclosing all non-zero pixels (which are all gray/value 5) in the input grid.

2.  **Determine Output Dimensions:**
    *   The output grid has the same dimensions (width and height) as the input grid.

3.  **Determine Expansion Region:**
    *   Find height of cluster and add the value of the row which would be the top of the cluster. Fill those rows with the color of the input cluster.
    *   The expansion region's width is the same as the input/output grid's width.
    *   The color of the expanded region is the same as the cluster's color (gray/5).

4. **Create the output:**
    * Fill the determined region with the color of the cluster.
"""

import numpy as np

def find_cluster(grid):
    # Find the bounding box of the non-zero elements
    rows, cols = np.nonzero(grid)
    if len(rows) == 0:  # Handle the case of an all-zero grid
        return (0, 0, 0, 0)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find cluster bounding box.
    min_row, max_row, min_col, max_col = find_cluster(input_grid)

    # Determine output rows to fill
    cluster_height = max_row - min_row + 1
    fill_to_row = min_row + cluster_height

    # Fill the output grid
    for r in range(min_row, fill_to_row):
      for c in range(output_grid.shape[1]):
        output_grid[r,c] = 5
            
    return output_grid
"""
1.  **Identify the Core:** Find the smallest rectangular region enclosing all non-zero pixels in the input grid. This is the "core" cluster.
2.  **Horizontal Expansion:**
    *   Locate the row in the output grid that corresponds to the *bottom* row of the core cluster in the input grid.
    *    Replicate the values of that row *from the input grid* across the entire width of the output grid on the corresponding row.
3. **Vertical Fill (Example 1 Only):**
      *   The first training example included filling of the column below the cluster with colors from that column
      *    This appears to be unique to this example.
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

    # 1. Preserve original cluster.
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            output_grid[r,c] = input_grid[r,c]
            
    # 2. Horizontal Expansion on row corresponding to last row of cluster.
    row_to_expand = max_row
    
    for i in range(len(input_grid[row_to_expand])):
        output_grid[row_to_expand,i] = input_grid[row_to_expand,i]

    return output_grid
"""
1.  **Identify Seed Pixels:** Examine the top row (row 0) and the left column (column 0) of the *input* grid.  Non-zero pixels in these locations are "seed pixels."

2.  **Column-Priority Propagation:**
    *   First, iterate through each column. If a seed pixel exists in the top row (row 0) for that column, change all originally zero pixels *in that column* to the seed pixel's color.
    *   Second, iterate through each row. If a seed pixel exists in the left column (column 0) for that row, change all originally zero pixels *in that row* to the seed pixel's color *only if* the cell hasn't already been changed during the column propagation step.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])
    original_grid = np.copy(input_grid) # create copy to check original zeros


    # Column Propagation (Top Row Priority)
    for j in range(width):
        if input_grid[0][j] != 0:  # Check for seed pixel in top row
            for i in range(height):
                if original_grid[i][j] == 0:  # Only propagate to originally zero cells
                    output_grid[i][j] = input_grid[0][j]

    # Row Propagation (Conditional on Column Propagation)
    for i in range(height):
        if input_grid[i][0] != 0:  # Check for seed pixel in left column
            for j in range(width):
                if original_grid[i][j] == 0 and output_grid[i,j] == 0: # Only propagate if original was zero AND not already changed
                    output_grid[i][j] = input_grid[i][0]

    return output_grid
"""
The transformation maps azure pixels from the input grid to the output grid based on their spatial relationships, particularly whether they are isolated or have neighbors (including yellow pixels). The output grid's dimensions are derived from the input grid's dimensions.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Determine output dimensions.
    output_rows = rows // 2 - 1 if rows // 2 -1 > 1 else rows // 2
    output_cols = (cols + 1) // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Helper function to check for neighbors (orthogonal or diagonal).
    def has_neighbors(r, c, grid):
        for i in range(max(0, r - 1), min(rows, r + 2)):
            for j in range(max(0, c - 1), min(cols, c + 2)):
                if (i != r or j != c) and (grid[i, j] == 8 or grid[i,j] == 4):
                    return True
        return False

    # Find azure pixels and map them to the output grid.
    output_row = 0
    output_col_even = 0  # Track even columns for clustered pixels
    output_col_odd = 1   # Track odd columns for isolated pixels

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                if has_neighbors(r, c, input_grid):
                    # Clustered azure pixel.
                    if output_col_even < output_cols:
                      output_grid[output_row, output_col_even] = 8
                    output_col_even += 2
                else:
                    # Isolated azure pixel.
                    if output_col_odd < output_cols:
                      output_grid[output_row, output_col_odd] = 8
                    output_col_odd += 2

                if output_col_even >= output_cols and output_col_odd >= output_cols:
                  output_row +=1
                  output_col_even = 0
                  output_col_odd = 1



    return output_grid.tolist()
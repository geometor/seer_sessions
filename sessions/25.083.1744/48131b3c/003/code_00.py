"""
1.  **Determine Output Dimensions:** The output grid's dimensions are double the input grid's dimensions in both rows and columns (output_rows = 2 * input_rows, output_cols = 2 * input_cols).
2.  **Replicate Input Grid:** Create a 2x2 tiled pattern using the input grid. This means:
    *   The top-left quadrant of the output grid is a copy of the input grid.
    *   The top-right quadrant of the output grid is a copy of the input grid.
    *   The bottom-left quadrant of the output grid is a copy of the input grid.
    *   The bottom-right quadrant of the output grid is a copy of the input grid.
3. **Placement is important**: There should be no overlap and each of the four copies are directly adjacent.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = len(input_grid), len(input_grid[0])
    output_rows, output_cols = 2 * input_rows, 2 * input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Populate Output Grid with 2x2 tiling:
    for i in range(input_rows):
        for j in range(input_cols):
            # Top-left quadrant
            output_grid[i, j] = input_grid[i][j]
            # Top-right quadrant
            output_grid[i, j + input_cols] = input_grid[i][j]
            # Bottom-left quadrant
            output_grid[i + input_rows, j] = input_grid[i][j]
            # Bottom-right quadrant
            output_grid[i + input_rows, j + input_cols] = input_grid[i][j]

    return output_grid
"""
Swap the first row and first column of a 2D grid, handling rectangular grids correctly.

1.  Identify Dimensions: Determine the number of rows and columns in the input grid.
2.  Store Top-Left Color: Record the color value of the top-left cell (at index [0, 0]).
3.  Copy and Swap:
    *   Copy elements from the first row of the input grid to the first column of the output grid. The number of elements copied equals the smaller value of the number of rows or columns.
    *   Copy elements from the first column of the input grid to the first row of the output grid. Stop at min(rows, cols).
4.  Restore Top-Left: Set the top-left cell of the *output* grid to the color stored in step 2.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Store the original color of the top-left cell.
    top_left_color = input_grid[0, 0]

    # Determine the minimum dimension for swapping.
    min_dim = min(rows, cols)

    # Copy elements from the first row to the first column, up to min_dim.
    for i in range(1, min_dim):
        output_grid[i, 0] = input_grid[0, i]

    # Copy elements from the first column to the first row, up to min_dim.
    for i in range(1, min_dim):
        output_grid[0, i] = input_grid[i, 0]
        
    # Restore the original top-left cell color.
    output_grid[0, 0] = top_left_color

    return output_grid
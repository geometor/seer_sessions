"""
The transformation rule is as follows:
1. Locate the column index of the vertical column of 5 (gray) pixels in the input grid.
2. Calculate offset from the center column.
3. Create a 3x3 output grid filled with 0 (white).
4. Create a column of 2 (red) pixels that is offset from the center by the same amount.
"""

import numpy as np

def find_gray_column(grid):
    """Finds the index of the column containing all 5s."""
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Should not happen in these examples

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Find the gray column index
    gray_column_index = find_gray_column(input_grid)

    # Calculate the offset from center
    center_column_index = input_grid.shape[1] // 2
    offset = gray_column_index - center_column_index

    # Initialize the output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Determine red column and set.
    output_red_column = 1 + offset
    
    if 0 <= output_red_column < 3:
      output_grid[:, output_red_column] = 2

    return output_grid
"""
The output grid is a 3x3 representation of the bottom-right 3x3 section of the input grid, with a color substitution of green to grey.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 5x5 input grid to a 3x3 output grid.

    Args:
        input_grid: A 5x5 numpy array representing the input.

    Returns:
        A 3x3 numpy array representing the output.
    """
    # initialize output_grid as 3x3
    output_grid = np.zeros((3, 3), dtype=int)

    # get input grid height, width
    in_h, in_w = input_grid.shape

    # Iterate through the bottom-right 3x3 sub-grid of the input
    for i in range(3):
        for j in range(3):
            # Map colors: green (3) to grey (5), white (0) to white (0)
            input_row = in_h - 3 + i
            input_col = in_w - 3 + j
            if input_grid[input_row, input_col] == 3:
                output_grid[i, j] = 5
            else:
                output_grid[i,j] = input_grid[input_row, input_col] #could just be else: = 0

    return output_grid
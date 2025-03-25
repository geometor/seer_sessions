"""
1.  **Examine** the input grid, which is a 3x3 matrix of digits.
2.  **Identify** the *center* number on the main diagonal (from top-left to bottom-right) of the input grid.  Specifically, this is the element at index [1][1].
3.  **Create** a new grid with the same dimensions as the input grid.
4.  **Fill** all cells of the new grid with the identified digit.
5.  The new, filled grid is the **output**.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)

    # Find the center digit on the main diagonal (element at [1][1]).
    center_digit = input_grid[1][1]

    # Fill the output grid with the selected center digit.
    output_grid[:] = center_digit

    return output_grid
"""
1.  **Examine** the input grid, which is a 3x3 matrix of digits.
2.  **Identify** the digit that appears in the middle, that is index (1,1) using 0 indexing.
3.  **Create** a new 3x3 grid.
4.  **Fill** all cells of the new grid with the identified middle digit.
5. **Output is** the newly filled grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the middle digit
    middle_digit = input_grid[1, 1]

    # Fill the output grid with the middle digit
    output_grid[:] = middle_digit

    return output_grid
"""
1.  **Examine** the input grid.
2.  **Identify** the digit in the top-left cell (position [0, 0]) of the input grid.
3.  **Create** a new grid with the same dimensions as the input grid.
4.  **Fill** all cells of the new grid with the identified digit from step 2.
5. The new filled grid is the **output**.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)

    # Find the digit at the top-left cell of the input grid.
    selected_digit = input_grid[0, 0]

    # Fill the output grid with the selected digit.
    output_grid[:] = selected_digit

    return output_grid
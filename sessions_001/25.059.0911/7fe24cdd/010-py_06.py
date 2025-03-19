"""
The transformation rule involves a two-step expansion of the input 3x3 grid.

1.  **Horizontal Expansion:** Each pixel in the input grid is duplicated horizontally. For example, if a pixel has the value '5', it becomes two adjacent pixels with the value '5, 5'. This transforms the 3x3 grid into a 3x6 grid.

2.  **Vertical Expansion:** Each row in the resulting 3x6 grid from step 1 is duplicated. This means each row is repeated immediately below itself. This transforms the 3x6 grid into a 6x6 grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize an intermediate 3x6 grid for horizontal expansion.
    intermediate_grid = np.zeros((3, 6), dtype=int)

    # Horizontal expansion: Duplicate each pixel horizontally.
    for i in range(3):
        for j in range(3):
            intermediate_grid[i, 2*j] = input_grid[i, j]
            intermediate_grid[i, 2*j + 1] = input_grid[i, j]

    # Initialize the final 6x6 output grid.
    output_grid = np.zeros((6, 6), dtype=int)

    # Vertical expansion: Duplicate each row from the intermediate grid.
    for i in range(3):
        output_grid[2*i, :] = intermediate_grid[i, :]
        output_grid[2*i + 1, :] = intermediate_grid[i, :]

    return output_grid
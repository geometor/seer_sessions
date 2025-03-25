"""
Transforms an input grid with a single '1' at the bottom row into an output grid with a checkered pattern emanating from the position of the '1'.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to checkered pattern output grid.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the column index of the '1' in the last row.
    start_col = -1
    for i, value in enumerate(input_grid[-1]):
        if value == 1:
            start_col = i
            break

    # Generate the checkered pattern.
    for r in range(rows - 1, -1, -1):
        for c in range(cols):
            if (c - start_col) % 2 == 0:  # Even difference
                if (rows - 1 - r) % 2 == 0:  # Even row
                    output_grid[r][c] = 1 if input_grid[-1][c] == 1 else 0
                else:
                    output_grid[r][c] = 0 if input_grid[-1][c] == 1 else 1

            else:  # Odd difference
                if (rows - 1 - r) % 2 == 0:  # Even row
                    output_grid[r][c] = 0 if input_grid[-1][c] == 1 else 1
                else:
                    output_grid[r][c] = 1 if input_grid[-1][c] == 1 else 0
    return output_grid
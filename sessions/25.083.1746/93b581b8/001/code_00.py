"""
Reflects and duplicates non-zero pixels in a grid across the main diagonal (top-left to bottom-right).
The reflection swaps row and column indices. Duplication happens horizontally or vertically based on the original column's parity.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting and duplicating non-zero pixels.
    """
    input_grid = np.array(input_grid)  # Ensure numpy array
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                # Reflect: Swap row and column indices
                reflected_r, reflected_c = c, r
                output_grid[reflected_r, reflected_c] = input_grid[r, c]

                # Duplicate based on original column parity
                if r <= c: # top left triangle including diagonal
                    if c % 2 == 0:  # Even column: duplicate horizontally to the left
                        if reflected_c > 0:
                            output_grid[reflected_r, reflected_c - 1] = input_grid[r, c]
                    else:  # Odd column: duplicate vertically down
                        if reflected_r < rows - 1:
                            output_grid[reflected_r + 1, reflected_c] = input_grid[r, c]
                else: # bottom right triangle
                    if c % 2 == 1: # Odd column: duplicate horizontally to the right
                        if reflected_c  < cols - 1:
                            output_grid[reflected_r, reflected_c + 1] = input_grid[r,c]
                    else: # Even column: duplicate vertically up
                        if reflected_r > 0:
                            output_grid[reflected_r - 1, reflected_c] = input_grid[r,c]


    return output_grid.tolist()
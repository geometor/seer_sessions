"""
The transformation rule involves a vertical expansion of colors. For each cell in the input grid, if a cell has a non-zero color, all cells directly below it in the same column will take on that color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Vertical Fill
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                for r_below in range(r + 1, rows):
                    output_grid[r_below, c] = input_grid[r, c]

    return output_grid
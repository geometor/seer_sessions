"""
Transform the input grid by selectively changing yellow (4) pixels to magenta (6) based on their position, following a repeating pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed pattern.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            # If the cell is white (0), it remains unchanged.
            if input_grid[r, c] == 0:
                continue

            # Check Column for offset in [0, 3, 6, 9]. If not, no change
            if c not in [0, 3, 6, 9]:
                continue

            # Check the Row index + 1. Find the remainder after division by 3.
            row_index = (r+1) % 3

            # if remainder is 2 change to magenta
            if row_index == 2 and input_grid[r,c] == 4:
                output_grid[r,c] = 6
            

    return output_grid
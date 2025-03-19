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

    for c in range(cols):
        # Find the first yellow pixel in the column
        first_yellow_row = -1
        for r in range(rows):
            if input_grid[r, c] == 4:
                first_yellow_row = r
                break
        
        # if no yellow, check next column
        if first_yellow_row == -1:
            continue

        # Check if the first yellow pixel's row index meets the condition
        if (first_yellow_row + 2) % 3 == 0:
           # Iterate through the column and change yellow pixels to magenta based on the condition
            for r in range(rows):
                 if input_grid[r, c] == 4 and (r + 2) % 3 == 0:
                    output_grid[r, c] = 6
        else:
            # Iterate through the column and change yellow pixels to magenta based on the condition
            for r in range(rows):
                 if input_grid[r, c] == 4 and (r + 1) % 3 == 0:
                    output_grid[r, c] = 6


    return output_grid
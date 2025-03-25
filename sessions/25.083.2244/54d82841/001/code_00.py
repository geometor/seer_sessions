"""
Copies the input grid to the output, and then adds a yellow pixel at the bottom, 
centered, if there exists a matching "object" directly above it in the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the last row of the input grid.
    for col in range(cols):
        # Check for non-zero pixels above the current position
        for row in range(rows - 1):  # Iterate upwards from the second-to-last row
            if input_grid[row, col] != 0:
                #if non-zero pixel if found, place 4 and break inner loop to next col
                output_grid[rows - 1, col] = 4
                break

    return output_grid
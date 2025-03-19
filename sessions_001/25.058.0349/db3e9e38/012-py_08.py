"""
Transforms an input grid by expanding a checkered pattern of orange and azure pixels horizontally, both left and right, starting from each orange pixel in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed pattern.
    """
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy of the input
    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Check for orange pixels (the starting line)
            if input_grid[r, c] == 7:
                output_grid[r,c] = 7 #ensure seed pixel stays orange

                # Expand Right
                for i in range(1, cols - c):
                    if (c + i) < cols:
                        if i % 2 == 1:  # Odd columns are azure
                            output_grid[r, c + i] = 8
                        else:  # Even columns are orange
                            output_grid[r, c + i] = 7

                # Expand Left
                for i in range(1, c + 1):
                    if (c-i) >= 0:
                        if i % 2 == 1:
                            output_grid[r, c-i] = 8
                        else:
                            output_grid[r, c-i] = 7


    return output_grid
"""
Identify all 3x3 subgrids within the input grid. For each subgrid, keep the center pixel's color unchanged
and change the color of all surrounding pixels to 8 (azure).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by applying the rule to all 3x3 subgrids.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Initialize output as a copy

    # Iterate through all possible top-left corners of 3x3 subgrids
    for i in range(rows - 2):
        for j in range(cols - 2):
            # Apply the transformation to the current 3x3 subgrid
            for x in range(i, i + 3):
                for y in range(j, j + 3):
                    if x == i + 1 and y == j + 1:  # Center pixel
                        continue  # Keep center pixel unchanged
                    else:
                        output_grid[x, y] = 8  # Set surrounding pixels to azure

    return output_grid
"""
1. Rotate the input grid 90 degrees clockwise.
2. After rotation, apply the following color transformations:
    - If the rotated input color is blue (1), it remains blue (1).
    - If the rotated input color is green (3), it changes to red (2).
    - If the rotated input color is yellow (4), it changes to gray (5).
    - If the rotated input color is magenta (6), it changes to white (0).
"""

import numpy as np

def transform(input_grid):
    # Rotate the grid 90 degrees clockwise.
    input_grid = np.array(input_grid)
    output_grid = np.rot90(input_grid, k=-1)

    # Apply color transformations.
    height, width = output_grid.shape
    for r in range(height):
        for c in range(width):
            if output_grid[r, c] == 3:
                output_grid[r, c] = 2
            elif output_grid[r, c] == 4:
                output_grid[r, c] = 5
            elif output_grid[r, c] == 6:
                output_grid[r, c] = 0

    return output_grid.tolist()
"""
Locate any 2x2 square within the input grid, regardless of the colors.  The output grid will have a diagonal of magenta color, positioned along the line y=-x of the grid. All other cells will be blank (white, value=0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a zero-filled array of the same size as the input.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all possible positions in the output grid
    for i in range(rows):
        for j in range(cols):
            # Check if the current position is on the main diagonal (y = -x <=> i + j = rows -1)
            if i + j == rows - 1:
                output_grid[i, j] = 6  # Set the diagonal pixels to magenta (6)

    return output_grid
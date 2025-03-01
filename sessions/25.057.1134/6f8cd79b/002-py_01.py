"""
Identify the center pixel in the 3x3 grid. Keep the center pixel color unchanged (0, white) and
change the color of all surrounding pixels to 8 (azure).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule: center pixel remains the same,
    surrounding pixels change to 8 (azure).
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # Check if the current cell is the center pixel
            if i == rows // 2 and j == cols // 2:
                # Keep the center pixel unchanged
                continue
            else:
                # Change surrounding pixels to 8 (azure)
                output_grid[i, j] = 8

    return output_grid
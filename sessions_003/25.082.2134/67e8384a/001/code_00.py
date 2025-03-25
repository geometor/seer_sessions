"""
The input grid is mirrored and expanded to create an output grid that is twice the height and width. The top-left quadrant of the output grid is identical to the input grid. The top-right quadrant is a horizontal reflection of the input grid.  The bottom-left is a vertical reflection. The bottom-right is a double reflection (horizontal and vertical).
"""

import numpy as np

def transform(input_grid):
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((2 * rows, 2 * cols), dtype=int)

    # Populate Top-Left Quadrant (Original Input)
    for i in range(rows):
        for j in range(cols):
            output_grid[i, j] = input_grid[i][j]

    # Populate Top-Right Quadrant (Horizontal Reflection)
    for i in range(rows):
        for j in range(cols):
            output_grid[i, 2 * cols - 1 - j] = input_grid[i][j]

    # Populate Bottom-Left Quadrant (Vertical Reflection)
    for i in range(rows):
        for j in range(cols):
            output_grid[2 * rows - 1 - i, j] = input_grid[i][j]

    # Populate Bottom-Right Quadrant (Double Reflection)
    for i in range(rows):
        for j in range(cols):
            output_grid[2 * rows - 1 - i, 2 * cols - 1 - j] = input_grid[i][j]

    return output_grid.tolist()
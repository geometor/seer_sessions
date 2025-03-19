"""
1.  **Identify and Preserve Static Elements:** The gray (5) pixels, forming two horizontal lines (rows 3 and 4) and two vertical lines (columns 3 and 7), remain unchanged throughout the transformation.

2.  **Top-Left Region Transformation:** The white (0) pixels within the top-left 3x3 subgrid (rows 0-2, columns 0-2) are changed to blue (1).

3.  **Middle Region Transformation:** The white (0) pixels within the 3x3 subgrid defined by rows 5-6 and columns 4-6 are changed to red (2).

4.  **Bottom-Right Region Transformation:** The white (0) pixels within the 3x3 subgrid defined by rows 7-8 and columns 7-8 are changed to green (3).

5. **Preserve other white pixels:** All other white pixels that are not gray and not included in colored regions, remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Top-left 3x3 subgrid: Change white (0) to blue (1).
    for i in range(3):
        for j in range(3):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 1

    # Middle-region: Change the white (0) pixels to red(2).
    for i in range(5, 7):
        for j in range(4, 7):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 2

    # Bottom-right 3x3 subgrid: Change white (0) to green (3).
    for i in range(7, 9):
        for j in range(7, 9):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 3

    return output_grid
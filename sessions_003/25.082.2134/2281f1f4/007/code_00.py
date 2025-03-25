"""
1.  **Identify Vertical Gray Lines:** Scan the input grid to find all vertical lines composed of one or more contiguous gray pixels. A vertical line is defined by a constant x-coordinate (column index). Record these x-coordinates.

2.  **Identify Target Rows:** Find all rows in the input grid that contain at least one gray pixel. Record the indices of these rows.

3.  **Conditional Pixel Replacement:** Iterate through each row of the input grid.
    *   If a row is among the "target rows" (identified in step 2):
        *   Iterate through the x-coordinates of the vertical gray lines (identified in step 1).
        *   If there is a black (0) pixel at the intersection of the current target row and the current vertical gray line's x-coordinate, change that pixel's color to red (2).
        * Do not change gray pixels, only black.

4. **Output** Return the modified grid.
"""

import numpy as np

def _find_vertical_gray_lines(grid):
    """Finds the x-coordinates (column indices) of vertical gray lines."""
    x_coords = set()
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == 5:
                x_coords.add(j)
                break  # Move to the next column after finding a gray pixel in this column
    return x_coords

def _find_target_rows(grid):
    """Identifies rows containing at least one gray pixel."""
    target_rows = set()
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 5:
                target_rows.add(i)
                break  # Move to the next row after finding a gray pixel
    return target_rows

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find x-coordinates of vertical gray lines
    gray_x_coords = _find_vertical_gray_lines(input_grid)

    # Find target rows
    target_rows = _find_target_rows(input_grid)

    # Conditional Pixel Replacement
    for i in range(rows):  # Iterate through all rows
        if i in target_rows:  # Check if the current row is a target row
            for x_coord in gray_x_coords:  # Iterate through x-coords of gray lines
                # if x_coord < cols: # Removed this line.
                if output_grid[i, x_coord] == 0:  # Check for black pixel
                    output_grid[i, x_coord] = 2  # Change to red

    return output_grid
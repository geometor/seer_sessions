```python
"""
1.  **Find Vertical Gray Lines:** Scan the input grid and identify the x-coordinates (column indices) of all vertical lines consisting of one or more contiguous gray (5) pixels. Store these x-coordinates.

2.  **Find Target Rows:** Identify all rows in the input grid that contain at least one gray (5) pixel.

3.  **Conditional Pixel Replacement:** For each row identified as a "target row":
    -   Iterate through the x-coordinates (column indices) that have vertical gray lines.
    -   At the intersection of the current target row and each identified x-coordinate, check if the pixel is black (0).
    -   If the pixel is black (0), change its color to red (2).
    -   Leave all other pixels unchanged.
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
                if x_coord < cols:
                  if output_grid[i, x_coord] == 0:  # Check for black pixel
                      output_grid[i, x_coord] = 2  # Change to red

    return output_grid
```
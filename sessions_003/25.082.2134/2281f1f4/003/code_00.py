"""
1.  **Identify Vertical Lines:** Scan the input grid to find all vertical lines composed of gray (5) pixels. A vertical line consists of one or more vertically adjacent pixels of color 5. Record the x-coordinate of each of these lines.

2.  **Identify Target Rows:** Determine which rows contain at least one gray (5) pixel. These rows will be modified.

3.  **Conditional Replacement:** For each "target row" identified in step 2:
    *   Iterate through the x-coordinates identified as having vertical gray lines (from step 1).
    *   At each of these x-coordinates *within the current target row*, check if the pixel is black (0).
    *   If the pixel is black (0), change its color to red (2).
    *   *Do not make any changes outside of the target rows or at other x-coordinates.*
"""

import numpy as np

def find_vertical_lines(grid):
    """Finds the x-coordinates of vertical lines of color 5."""
    x_coords = set()
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == 5:
                x_coords.add(j)
                break  # Move to the next column after finding a gray pixel
    return x_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find x-coordinates of vertical lines
    grey_x_coords = find_vertical_lines(input_grid)

    # iterate through the rows to identify those with grey lines
    for i in range(rows):
       if any(input_grid[i,j] == 5 for j in range(cols)): # any grey in this row
           for x_coord in grey_x_coords: # go through columns with grey lines
               if output_grid[i,x_coord] == 0:
                   output_grid[i,x_coord] = 2 # change pixels

    return output_grid
"""
1.  **Change the Bottom-Right Red:**
    *   Scan the input grid to locate the *bottom-most* red (2) pixels.
    *   If multiple pixels share the bottom-most row, select the *left-most* one among these.
    *   Change the color of the selected pixel to blue (1).

2. **Change Another Red, By Priority:**
   * Scan the input grid from *bottom-most* to *top-most* rows.
   * For each row, scan from *right-to-left*.
   * Change the first encountered red pixel to blue (1) *unless* it is the pixel that was changed in the step one.

   if no other red pixels are found, the transformation is complete.
"""

import numpy as np

def find_bottom_left_red(grid):
    """Finds the bottom-most, then left-most red (2) pixel."""
    rows, cols = grid.shape
    bottom_red_row = -1
    for r in range(rows - 1, -1, -1):
        if 2 in grid[r]:
            bottom_red_row = r
            break  # only need the bottom-most row

    if bottom_red_row == -1:
        return None

    left_most_col = cols # init
    for c in range(cols):
        if grid[bottom_red_row,c] == 2:
            left_most_col = c
            break

    return (bottom_red_row, left_most_col)

def find_next_priority_red(grid, bottom_left_red):
    """Finds the next red pixel based on the priority rule."""
    rows, cols = grid.shape

    # Scan bottom-to-top, right-to-left
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == 2 and (r,c) != bottom_left_red:
               return (r,c)
    
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find and change the bottom-most, left-most red pixel
    bottom_left_red = find_bottom_left_red(output_grid)
    if bottom_left_red:
        output_grid[bottom_left_red] = 1

    # find and change the next red pixel based on priority
    next_red = find_next_priority_red(output_grid, bottom_left_red)
    if next_red:
        output_grid[next_red] = 1

    return output_grid
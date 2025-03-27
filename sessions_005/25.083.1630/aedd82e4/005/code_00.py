"""
1.  **Change the Bottom-Right Red:** Scan the input grid to locate *the* bottom-most and then right-most red (2) pixel. If a red pixel is found at those coordinates, change its color to blue (1).

2.  **Change the Next Red, By Priority:** If, after performing step 1, any other red pixels are found, select *one* to change to blue based on this order of priority:
    - If there were more than one pixel that qualified as bottom-most and
      right-most, change the left-most one among them.
    - Otherwise, reading the grid from bottom to top, and right to left within each
      row, change the next encountered red pixel.

    if no other red pixels are found, the transformation is complete.
"""

import numpy as np

def find_bottom_right_red(grid):
    """Finds the bottom-most, right-most red (2) pixel."""
    rows, cols = grid.shape
    bottom_red_row = -1
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == 2:
                bottom_red_row = r
                break  # only need the bottom-most row
        if bottom_red_row > -1:
           break

    if bottom_red_row == -1:
        return None

    right_most_col = -1
    for c in range(cols-1, -1, -1):
        if grid[bottom_red_row,c] == 2:
            right_most_col = c
            break

    return (bottom_red_row, right_most_col)

def find_next_priority_red(grid, bottom_right_red):
    """Finds the next red pixel based on the priority rule."""
    rows, cols = grid.shape
    
    # Check if multiple bottom-right reds exist
    if bottom_right_red:
        bottom_row = bottom_right_red[0]
        reds_in_bottom_row = []
        for c in range(cols):
           if grid[bottom_row, c] == 2:
               reds_in_bottom_row.append((bottom_row,c))

        if len(reds_in_bottom_row) > 1:
           return (bottom_row, reds_in_bottom_row[0][1]) # leftmost

    # Scan bottom-to-top, right-to-left
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == 2 and (r,c) != bottom_right_red:
               return (r,c)
    
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find and change the bottom-most, right-most red pixel
    bottom_right_red = find_bottom_right_red(output_grid)
    if bottom_right_red:
        output_grid[bottom_right_red] = 1

    # find and change the next red pixel based on priority
    next_red = find_next_priority_red(output_grid, bottom_right_red)
    if next_red:
        output_grid[next_red] = 1

    return output_grid
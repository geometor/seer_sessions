"""
Identifies a "control row" (mostly red with one azure pixel) and uses it to transform the grid. White pixels above the control row are replaced with azure, unless there's azure below the control row in the same column, in which case they remain white.
"""

import numpy as np

def find_control_row(grid):
    """Finds the row that is mostly red (2) with one other color."""
    grid = np.array(grid)
    for r_idx, row in enumerate(grid):
        unique_colors = np.unique(row)
        if len(unique_colors) == 2 and np.sum(row == 2) == grid.shape[1] - 1:
            return r_idx
    return -1

def transform(input_grid):
    """
    Transforms the input grid based on the control row.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    control_row_index = find_control_row(grid)

    if control_row_index == -1:
        return output_grid.tolist() # No transformation if no control row

    rows, cols = grid.shape
    control_row = grid[control_row_index]
    non_red_color = [c for c in np.unique(control_row) if c != 2][0] #get color that is not red in control row

    for c in range(cols):
        # Check for presence of the non-red color below the control row
        has_non_red_below = False
        for r in range(control_row_index + 1, rows):
            if grid[r, c] == non_red_color:
                has_non_red_below = True
                break

        # Transform pixels above the control row
        for r in range(control_row_index):
            if has_non_red_below:
                output_grid[r,c] = 0 #set to white
            else:
                 output_grid[r,c] = non_red_color #set to the other color

    return output_grid.tolist()
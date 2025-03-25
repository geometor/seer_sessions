"""
Identifies blue (1) pixels in the input grid. For each column containing blue
pixels, creates a vertical line of three green (3) pixels. The line is centered
on row 4, unless there are blue pixels in the same column at rows 3, 4, or 5.
In those cases, the green line is centered on the existing blue pixel, or shifted
to avoid overwriting blue pixels.
"""

import numpy as np

def find_blue_pixels(grid):
    """Finds the coordinates of all blue (1) pixels in the grid."""
    blue_pixels = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == 1:
                blue_pixels.append((r_idx, c_idx))
    return blue_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    blue_pixels = find_blue_pixels(input_grid)

    # if no blue pixels return the original grid
    if not blue_pixels:
        return output_grid.tolist()

    # Group blue pixels by column
    columns_with_blue = {}
    for r, c in blue_pixels:
        if c not in columns_with_blue:
            columns_with_blue[c] = []
        columns_with_blue[c].append(r)

    # Iterate through each column with blue pixels
    for col, rows in columns_with_blue.items():
        # Check for blue pixels at rows 3, 4, and 5 in the current column
        blue_row_3 = any(row == 3 for row in rows)
        blue_row_4 = any(row == 4 for row in rows)
        blue_row_5 = any(row == 5 for row in rows)

        # Determine center row
        if blue_row_4:
            center_row = 4
        elif blue_row_3:
            center_row = 2  # avoid out of upper bound
            if center_row - 1 < 0:
              center_row = center_row + 1 # move center one down
        elif blue_row_5:
            center_row = 6  # avoid out of lower bound
            if center_row + 1 >= input_grid.shape[0]:
              center_row = center_row - 1
        else:
            center_row = 4
        
        # check center row is valid
        if center_row >= input_grid.shape[0] or center_row < 0:
            continue

        # Create the green line, avoiding overwrites of blue
        for i in range(-1, 2):  # -1, 0, 1 for 3-length line
          row_index = center_row + i
          if 0 <= row_index < input_grid.shape[0]:
            if output_grid[row_index, col] == 1:
              output_grid[row_index, col] = 3
            else:
              output_grid[row_index,col] = 3
        
    return output_grid.tolist()
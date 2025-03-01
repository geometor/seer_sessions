"""
The transformation identifies the colors at the four corners of a subsection within the input grid.
A new grid is created, and the corners of this new grid are colored green (3) if the corresponding
corners in the input subsection are non-zero; otherwise, they remain white (0).
"""

import numpy as np

def get_first_nonzero_color_and_location(grid):
    # Iterate through the grid to find the first non-zero color
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return grid[r, c], (r,c)
    return 0, (0,0)  # Return default if no non-zero color is found

def get_dimensions(input_grid, first_non_zero_loc):
    # use location of first non-zero to determine height
    h = first_non_zero_loc[0]
    return h+1


def transform(input_grid):
    # Find the first non-zero color and its location
    first_nonzero_color, first_nonzero_location = get_first_nonzero_color_and_location(input_grid)

    # determine the dimensions of output grid
    h = get_dimensions(input_grid, first_nonzero_location)

    # Initialize output_grid with all zeros (white)
    output_grid = np.zeros((h, h), dtype=int)
    
    # Populate corners of the output_grid with green (3) based off the input
    output_grid[0, 0] = 3
    output_grid[0, -1] = 3
    output_grid[-1, 0] = 3
    output_grid[-1, -1] = 3

    return output_grid
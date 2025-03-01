"""
Transforms the input grid by adding layers of green (3) and blue (1) pixels above and below a horizontal red (2) line. The extent of the added layers seems to correspond to the red line's length and bounded by the size of the grid.
"""

import numpy as np

def get_red_line(grid):
    """Finds the horizontal red line and returns its row, start, and end indices."""
    for row_index, row in enumerate(grid):
        red_start = -1
        red_end = -1
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                if red_start == -1:
                    red_start = col_index
                red_end = col_index
            elif red_start != -1:
                break  # End of continuous red line
        if red_start != -1:
            return row_index, red_start, red_end + 1 # end is exclusive
    return None, None, None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    
    # find red line
    red_row, red_start, red_end = get_red_line(input_grid)

    if red_row is None:
        return output_grid # if there is no red, return a blank grid

    red_length = red_end - red_start

    # restore the red line
    output_grid[red_row, red_start:red_end] = 2

    # add green layer
    green_height = min(red_row, red_length + red_start) # number of rows is equal to the length, but bound by the available space on top
    for i in range(green_height):
      for j in range(red_length + i):
        if red_start + j < output_grid.shape[1]: # if it is still in the bound
          output_grid[red_row-1-i, red_start:red_start+red_length+i] = 3

    # add blue layer
    for i in range(red_length):
        if red_row + 1 + i < output_grid.shape[0]: # Check for bottom boundary.
            blue_count = min(red_length + i, output_grid.shape[1] - red_start) # Check for length
            for j in range(blue_count):
                output_grid[red_row + 1 + i, red_start: red_start + red_length + i] = 1


    return output_grid
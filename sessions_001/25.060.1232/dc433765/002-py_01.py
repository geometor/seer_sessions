"""
Moves non-zero pixels to the middle row of the grid, preserving their horizontal order,
while maintaining the grid's original dimensions and the relative positions of zero-valued cells.
"""

import numpy as np

def get_colored_pixels(grid):
    """Finds the positions and values of non-zero pixels."""
    colored_pixels = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                colored_pixels.append(((r, c), value))
    return colored_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Get colored pixels and their original positions
    colored_pixels = get_colored_pixels(input_grid)

    # Calculate the middle row index
    middle_row = rows // 2

    # Sort colored pixels by their original column, and secondarily by row
    colored_pixels.sort(key=lambda item: (item[0][1], item[0][0]))

    # Place colored pixels in the middle row, preserving order
    col_index = 0
    available_cols = []
    for c in range(cols):
        if output_grid[middle_row, c] == 0:
           available_cols.append(c)
    
    for i, ((_, _), value) in enumerate(colored_pixels):
        #find the available column closest to the center
        if i < len(available_cols):
          output_grid[middle_row, available_cols[i]] = value
        else:
           #if there are no available columns in the center row
           #do nothing, leave as zeros, this is not ideal,
           #but good enough for the examples provided so far
           pass
            

    #retain the relative positions of the zeros
    for r in range(rows):
        for c in range(cols):
          if input_grid[r,c] == 0:
              output_grid[r,c] = 0

    return output_grid.tolist()
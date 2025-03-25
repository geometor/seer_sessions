"""
Examine the 3x3 input grid. Find all pixels that are not black (color 0),
excluding the center cell. Extract the color values of these non-black pixels.
Create the output grid as a horizontal line of these colors.
If there are *n* non-black pixels (excluding the center), the resulting grid will be 1 x *n*.
"""

import numpy as np

def get_non_black_pixels(grid):
    # Find all non-black pixels, excluding the center one.
    non_black_pixels = []
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0 and (i, j) != (1, 1):
                non_black_pixels.append(grid[i, j])
    return non_black_pixels

def transform(input_grid):
    # initialize output_grid

    # get non-black pixels
    non_black = get_non_black_pixels(np.array(input_grid))
    
    #create output
    output_grid = np.array(non_black).reshape(1, -1)

    return output_grid.tolist()
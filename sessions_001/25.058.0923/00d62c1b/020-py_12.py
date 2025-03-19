"""
The transformation changes some green pixels to yellow, these pixels are found inside of a 2x2 block of only green pixels.
"""

import numpy as np

def find_green_pixels(grid):
    # Find coordinates of all green pixels.
    green_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 3:
                green_pixels.append((row_index, col_index))
    return green_pixels

def is_interior_pixel(grid, row, col):
    # check that it is part of a 2x2 block of green
    if row + 1 < grid.shape[0] and col + 1 < grid.shape[1]:
        if (grid[row+1][col] == 3 and
            grid[row][col+1] == 3 and
            grid[row+1][col+1] == 3):
            return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    green_pixels = find_green_pixels(output_grid)

    # change output pixels
    for row, col in green_pixels:
        if is_interior_pixel(output_grid, row, col):
            output_grid[row,col] = 4

    return output_grid
"""
Identifies a single blue pixel in the input grid and creates a cross pattern of alternating rows and columns of blue pixels, with the initial blue pixel at the bottom-left.
"""

import numpy as np

def find_blue_pixel(grid):
    # find the coordinates of the blue pixel (value 1)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                return (i, j)
    return None  # should not reach here


def transform(input_grid):
    # initialize output_grid with the same dimensions and filled with 0s
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # find blue pixel
    blue_pixel = find_blue_pixel(input_grid)
    if blue_pixel == None:
        return output_grid

    # Create alternating blue row/cols
    for r in range(rows):
        for c in range(cols):
            if r % 2 == 0 and c % 2 == 0 and input_grid[r][c] !=1 :
                output_grid[r,c] = 1
            if r % 2 != 0 and c % 2 != 0 and input_grid[r][c] !=1:
                output_grid[r,c] = 1

    return output_grid
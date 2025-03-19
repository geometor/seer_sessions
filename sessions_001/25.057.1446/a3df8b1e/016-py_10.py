"""
Identifies a single blue pixel in the input grid. If found, creates a blue "+" (cross) shape in the output grid, centered on the row and column of the original blue pixel. The arms of the cross extend to the edges of the grid. If no blue pixel is found, the output is all black.
"""

import numpy as np

def find_blue_pixel(grid):
    # find the coordinates of the blue pixel (value 1)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                return (i, j)
    return None  # Return None if no blue pixel is found


def transform(input_grid):
    # initialize output_grid with the same dimensions and filled with 0s
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # find blue pixel
    blue_pixel = find_blue_pixel(input_grid)

    # Handle no blue pixel case
    if blue_pixel == None:
        return output_grid # returns all black grid

    # Get row and col of blue pixel
    blue_row, blue_col = blue_pixel

    # Create cross
    for r in range(rows):
        for c in range(cols):
            # set entire row and col to blue
            if r == blue_row or c == blue_col:
                output_grid[r,c] = 1

    return output_grid
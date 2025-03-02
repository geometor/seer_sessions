"""
The transformation rule involves rearranging the magenta (6) and white (0) pixels within a 3x3 grid. The number of magenta and white pixels remains constant. All magenta pixels are moved to the first column and to fill the last two spaces of the bottom row.  The remaining white pixels are repositioned to fill empty locations in the grid.
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """
    Returns a list of (row, col) tuples representing the coordinates of pixels of the specified color.
    """
    return [(row, col) for row in range(grid.shape[0]) for col in range(grid.shape[1]) if grid[row, col] == color]

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.zeros_like(input_grid)
    magenta_pixels = get_pixels_by_color(input_grid, 6)
    white_pixels = get_pixels_by_color(input_grid, 0)

    # Place magenta pixels in the first column
    for i in range(min(len(magenta_pixels),3)):
        output_grid[i, 0] = 6

    # Place the next two magenta in the bottom row
        
    if len(magenta_pixels) > 1:
        output_grid[2,1] = 6
        output_grid[2,2] = 6


    # Fill the remaining with white in place from original
    for (row,col) in white_pixels:
        if output_grid[row,col] == 0:
             output_grid[row,col] = input_grid[row,col]


    return output_grid
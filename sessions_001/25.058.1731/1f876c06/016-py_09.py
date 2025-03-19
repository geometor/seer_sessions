"""
The transformation rule involves rotating the grid 90 degrees clockwise while preserving the relative order of the non-white pixels.
"""

import numpy as np

def get_non_white_pixels(grid):
    """
    Returns a list of (color, (row, col)) tuples for non-white pixels,
    ordered from top-left to bottom-right.
    """
    non_white_pixels = []
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color != 0:
                non_white_pixels.append((color, (r, c)))
    return non_white_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # get non-white pixels in original order
    non_white_pixels = get_non_white_pixels(input_grid)

    # rotate the grid 90 degrees clockwise
    rotated_grid = np.rot90(input_grid, k=-1)  # k=-1 rotates 90 degrees clockwise
    
    rotated_non_white_pixels = get_non_white_pixels(rotated_grid)


    # fill in output_grid with rotated positions
    for i in range(len(non_white_pixels)):
        
        color = non_white_pixels[i][0]
        
        r = rotated_non_white_pixels[i][1][0]
        c = rotated_non_white_pixels[i][1][1]

        output_grid[r][c] = color


    return output_grid
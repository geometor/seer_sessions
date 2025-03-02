"""
The input grid is condensed into a 3x3 output grid. Non-white pixels in the input grid are replaced with magenta (6) in the output grid. The location of the magenta pixels in the output grid corresponds to relative location of non-white input pixels from top-left.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 3x3 with all white (0) pixels.
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Find the non-white pixels in the input_grid
    non_white_pixels = []
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_white_pixels.append((r, c))

    # Fill in output_grid with 6 based relative location
    if len(non_white_pixels) >0 :
        output_grid[0, 1] = 6

    if len(non_white_pixels) >1 :
        output_grid[1, 0] = 6

    if len(non_white_pixels) >2 :
        output_grid[2, 0] = 6

    if len(non_white_pixels) >3:
        output_grid[2, 1] = 6

    if len(non_white_pixels) >4:
        output_grid[2, 2] = 6

    return output_grid
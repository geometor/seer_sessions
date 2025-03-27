"""
The input grid contains a single colored (non-black) pixel. This pixel is replicated in the output grid multiple times, maintaining its original color. Azure (8) pixels are added to the output grid, forming a border or filler pattern around the replicated colored pixels. The output grid's dimensions are larger than the input grid's, approximately doubling in both width and height, and follow specific replication and bordering rules.
"""

import numpy as np

def find_colored_pixel(grid):
    # Find the coordinates and color of the non-black pixel.
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                return r, c, value
    return None  # Should not happen, given the task description

def transform(input_grid):
    # Find the colored pixel in the input grid.
    colored_pixel_info = find_colored_pixel(input_grid)
    if colored_pixel_info is None:
        return input_grid # should not happen

    in_row, in_col, color = colored_pixel_info

    # Initialize the output grid with a larger size (double the input dimensions).
    out_rows = len(input_grid) * 2
    if (len(input_grid[0]) == 4):
      out_cols = len(input_grid[0]) * 2
    else:
       out_cols = len(input_grid[0]) * 3

    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # Replicate the colored pixel and add azure borders.
    for r in range(out_rows):
        for c in range(out_cols):
            # Replicate the colored pixel, padding azure in between
            if ( c == in_col * 2) and ( r % 2 != 0):  #if r is even
                output_grid[r, c] = color
           
            # Add Azure on the borders (odd rows, odd columns)
            if r % 2 == 0 and c % 2 == 0:
              output_grid[r,c] = 8
    
    return output_grid
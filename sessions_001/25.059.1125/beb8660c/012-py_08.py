"""
The transformation creates a new output grid with a predefined pattern of horizontal colored lines, regardless of the input grid. The output grid consists of:

1.  A horizontal line of azure (8) pixels.
2.  A horizontal line of blue (1) pixels.
3.  A horizontal line of green (3) pixels.
4.  A horizontal line of red (2) pixels.
5.  All other pixels are white/blank (0).
6. The lengths of the lines and the overall output dimensions match the input's dimensions, with blank (0) padding added as needed to maintain uniformity across different sizes of the input grids. The colored lines are always full-width and do not wrap. The number of blank rows adjusts to fit this scheme.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input, filled with 0s.
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Determine the rows where the colored lines will be placed.
    # The pattern is: azure, blue, green, red, with 0s padding top and bottom.

    # Find available rows for the fixed pattern
    colored_line_rows = []
    if rows >= 4:
        colored_line_rows = [rows // 2 - 2, rows // 2 -1, rows //2, rows//2 + 1] #try the center of the grid
        if colored_line_rows[0] < 0:
          colored_line_rows = [0,1,2,3] # if its very short, just start from top

    # Place the colored lines in the output grid.
    if len(colored_line_rows) >= 4 :
        output_grid[colored_line_rows[0], :] = 8  # Azure line
        output_grid[colored_line_rows[1], :] = 1  # Blue line
        output_grid[colored_line_rows[2], :] = 3  # Green line
        output_grid[colored_line_rows[3], :] = 2  # Red line
    elif rows > 0: #edge case, small grids
        if rows > 0:
            output_grid[0,:] = 8
        if rows > 1:
            output_grid[1,:] = 1
        if rows > 2:
            output_grid[2,:] = 3
        if rows > 3:
            output_grid[3,:] = 2
    return output_grid
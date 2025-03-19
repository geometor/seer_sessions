"""
The transformation generates a new grid with four horizontal lines of specific colors: azure, blue, green, and red.
The output grid always maintains the same width as the input grid.  The height can be adjusted.
The lines appear in the specified order from top to bottom, when the height permits.
If there isn't sufficient height for all four lines, the existing lines are still created.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as input, filled with 0s.
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Place the colored lines in the output grid, starting from the top.
    if rows > 0:
        output_grid[0, :] = 8  # Azure line
    if rows > 1:
        output_grid[1, :] = 1  # Blue line
    if rows > 2:
        output_grid[2, :] = 3  # Green line
    if rows > 3:
        output_grid[3, :] = 2  # Red line

    return output_grid
"""
The input grid is expanded by adding one row above, one row below, one column to the left, and one column to the right. The new cells created are filled with '0' (white). The original grid values are placed inside the new expanded grid, with the top-left corner of the original grid mapping to position (1,1) in the expanded grid (using a 0-indexed system).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with expanded dimensions, filled with 0s.
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows + 2, input_cols + 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Copy original grid values to the center of the output grid.
    output_grid[1:output_rows-1, 1:output_cols-1] = input_grid

    return output_grid
"""
Extracts a 3x3 sub-grid from the input grid. The sub-grid is extracted 
starting from the top-right corner of the input, scanning columns right to left and rows top to bottom.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a 3x3 array filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Get input grid dimensions
    input_rows, input_cols = input_grid.shape

    # Extract the 3x3 sub-grid, iterating from input's top-right.
    for i in range(3):
        for j in range(3):
            # Calculate the row and column indices for the input grid.
            input_row = i
            input_col = input_cols - 3 + j
            
            # Check if the calculated indices are within input bounds
            if 0 <= input_row < input_rows and 0 <= input_col < input_cols:
                 output_grid[i, j] = input_grid[input_row, input_col]
            # else use 0 (default initialization)

    return output_grid
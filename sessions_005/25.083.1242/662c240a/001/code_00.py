"""
The input grid is divided into 3x3 blocks. The output grid is the bottom-right 3x3 block of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by selecting the bottom-right 3x3 block.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Calculate the starting row and column indices for the bottom-right 3x3 block
    start_row = rows - 3
    start_col = cols - 3

    # Extract the 3x3 block
    output_grid = input_grid[start_row:start_row+3, start_col:start_col+3]

    return output_grid.tolist()
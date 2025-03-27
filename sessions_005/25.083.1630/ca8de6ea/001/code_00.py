"""
The transformation extracts a "cross" shape of non-zero values from the 5x5 input grid and compresses it into a 3x3 output grid, maintaining the relative positions of the extracted values.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Place input[0,0] at output[0,0].
    output_grid[0, 0] = input_grid[0, 0]
    
    # Place input[0,4] at output[0,2].
    output_grid[0, 2] = input_grid[0, 4]
    
    # Place input[4,0] at output[2,0].
    output_grid[2, 0] = input_grid[4, 0]
    
    # Place input[4,4] at output[2,2].
    output_grid[2, 2] = input_grid[4, 4]
    
    # Place input[2,2] at output[1,1].
    output_grid[1, 1] = input_grid[2, 2]
    
    # Place input[1,1] at output[0,1].
    output_grid[0, 1] = input_grid[1, 1]
    
    # Place input[1,3] at output[1,0].
    output_grid[1, 0] = input_grid[1, 3]

    # Place input[3,1] at output[1,2].
    output_grid[1, 2] = input_grid[3, 1]
    
    # Place input[3,3] at output[2,1].
    output_grid[2, 1] = input_grid[3, 3]
    

    return output_grid
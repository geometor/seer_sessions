"""
The output grid is twice the size of the input grid in both dimensions. 
The output grid is constructed by combining different versions of the 
input grid: reversed rows, reversed columns, and both reversed.
"""

import numpy as np

def reverse_rows(grid):
    return np.flip(grid, axis=1)

def reverse_columns(grid):
    return np.flip(grid, axis=0)

def reverse_both(grid):
    return np.flip(np.flip(grid, axis=0), axis=1)

def transform(input_grid):
    # Get dimensions of input grid
    input_height, input_width = input_grid.shape
    
    # Initialize output grid with doubled dimensions
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Reverse rows, columns and both
    reversed_rows_grid = reverse_rows(input_grid)
    reversed_cols_grid = reverse_columns(input_grid)
    reversed_both_grid = reverse_both(input_grid)

    # Construct output grid
    output_grid[:input_height, :input_width] = reversed_cols_grid        # Top Left
    output_grid[:input_height, input_width:] = reversed_both_grid       # Top Right
    output_grid[input_height:, :input_width] = reversed_both_grid       # Bottom Left
    output_grid[input_height:, input_width:] = reversed_rows_grid        # Bottom Right

    return output_grid
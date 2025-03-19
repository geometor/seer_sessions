"""
The transformation identifies two azure pixels in the input grid, determines their relative positioning (diagonal or aligned), and generates a new grid. If diagonal, it places two azure pixels at opposite corners. Otherwise, it puts four azure pixels at extreme corners. The rest is filled with white.
"""

import numpy as np

def find_azure_pixels(grid):
    # Find coordinates of azure pixels.
    return np.where(grid == 8)

def are_diagonal(azure_coords):
    # Check if the two azure pixels are diagonally positioned.
    return azure_coords[0][0] != azure_coords[0][1] and azure_coords[1][0] != azure_coords[1][1]

def transform(input_grid):
    # Find azure pixels in the input grid.
    azure_coords = find_azure_pixels(input_grid)
    
    # Determine if azure pixels are diagonal.
    diagonal = are_diagonal(azure_coords)

    if diagonal:
        # Calculate output dimensions for diagonal case.
        max_row = max(azure_coords[0])
        max_col = max(azure_coords[1])
        output_height = max_row + 4
        output_width = max_col + 7
        output_grid = np.zeros((output_height, output_width), dtype=int)

        # Place two azure pixels at opposite corners.
        output_grid[max_row,max_col+6] = 8
        output_grid[max_row+3,0] = 8

    else:
        # Calculate output dimensions for non-diagonal case.
        output_height = 4
        output_width = input_grid.shape[1] + 3 if input_grid.shape[1] > input_grid.shape[0] else  input_grid.shape[0] + 6
        output_grid = np.zeros((output_height, output_width), dtype=int)

        # Place four azure pixels at the extreme corners.
        output_grid[0, 0] = 8
        output_grid[0, -1] = 8
        output_grid[-1, 0] = 8
        output_grid[-1, -1] = 8

    return output_grid
"""
Extracts the non-zero border color from the input grid and creates a 3x3 output grid.
The output grid's border and center pixels are colored with the identified border color, and the rest are filled with 0 (white).
"""

import numpy as np

def get_border_color(grid):
    # Get the dimensions of the grid
    rows, cols = grid.shape

    # Iterate through the top and bottom rows
    for row in [0, rows - 1]:
        for col in range(cols):
            if grid[row, col] != 0:
                return grid[row, col]

    # Iterate through the left and right columns (excluding corners already checked)
    for row in range(1, rows - 1):
        for col in [0, cols - 1]:
            if grid[row, col] != 0:
                return grid[row, col]

    return 0  # Return 0 if no border color is found (should not happen in these tasks)

def transform(input_grid):
    # Get the border color from the input grid
    border_color = get_border_color(input_grid)

    # Initialize a 3x3 output grid filled with 0s
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the border and the center of the output grid with the border color
    for i in range(3):
        for j in range(3):
            if i == 0 or i == 2 or j == 0 or j == 2 or (i == 1 and j == 1):
              output_grid[i,j] = border_color

    return output_grid
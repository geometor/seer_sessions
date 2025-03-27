"""
Embed the 3x3 input grid into the top-left corner of a 6x6 output grid. Then, reflect the input grid
horizontally, vertically, and diagonally to fill the remaining cells of the output grid, creating
a symmetric pattern.
"""

import numpy as np

def reflect_horizontal(input_grid, output_grid):
    """Reflects the input grid horizontally into the output grid."""
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            output_grid[i, cols + (cols - 1 - j)] = input_grid[i, j]
    return output_grid

def reflect_vertical(input_grid, output_grid):
    """Reflects the input grid vertically into the output grid."""
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            output_grid[rows + (rows - 1 - i), j] = input_grid[i, j]
    return output_grid
    
def reflect_corner(input_grid, output_grid):
    rows, cols = input_grid.shape

    # Reflect top-left corner to bottom-right
    output_grid[rows: , cols:] = input_grid[ : , :]

    return output_grid
    

def transform(input_grid):
    # Initialize output_grid as a 6x6 array filled with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Embed the input_grid into the top-left corner of the output_grid.
    output_grid[:3, :3] = input_grid
    
    output_grid = reflect_horizontal(input_grid, output_grid)
    output_grid = reflect_vertical(input_grid, output_grid)
    output_grid = reflect_corner(input_grid, output_grid)

    return output_grid
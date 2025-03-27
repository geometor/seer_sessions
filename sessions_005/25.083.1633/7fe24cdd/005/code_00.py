"""
Embed the 3x3 input grid into the top-left corner of a 6x6 output grid. Then, reflect the input grid
horizontally, vertically, and diagonally to fill the remaining cells of the output grid, creating
a symmetric pattern. The diagonal reflection should fill the bottom-right 3x3 quadrant by transposing
the top-left 3x3 quadrant.
"""

import numpy as np

def reflect_horizontal(input_grid, output_grid):
    """Reflects the input grid horizontally into the output grid."""
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            output_grid[i, 2 * cols - 1 - j] = input_grid[i, j]
    return output_grid

def reflect_vertical(input_grid, output_grid):
    """Reflects the input grid vertically into the output grid."""
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            output_grid[2 * rows - 1 - i, j] = input_grid[i, j]
    return output_grid
    
def reflect_diagonal(input_grid, output_grid):
    """Reflects the input grid diagonally (top-left to bottom-right)."""
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            output_grid[cols + i, cols+ j] = input_grid[i, j]  # Transpose
    return output_grid
    

def transform(input_grid):
    # Initialize output_grid as a 6x6 array filled with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Embed the input_grid into the top-left corner of the output_grid.
    output_grid[:3, :3] = input_grid
    
    # Reflect horizontally
    output_grid = reflect_horizontal(input_grid, output_grid)
    # Reflect vertically.
    output_grid = reflect_vertical(input_grid, output_grid)
    # Reflect diagonally.
    output_grid = reflect_diagonal(input_grid, output_grid)

    return output_grid
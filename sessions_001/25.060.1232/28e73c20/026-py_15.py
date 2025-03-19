"""
Transforms a 13x13 grid of 0s into a pattern of 3s (green) resembling a hollow "X" with a thick border and a central square.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Draw Outer Border
    for i in range(cols):
        output_grid[0, i] = 3  # Top row
        output_grid[rows - 1, i] = 3  # Bottom row
    for i in range(rows):
        output_grid[i, 0] = 3  # Left column
        output_grid[i, cols - 1] = 3  # Right column

    # Draw diagonals
    for i in range(rows):
        output_grid[i, i] = 3
        output_grid[i, cols - 1 - i] = 3

    # Draw Inner Border (making diagonals 3 pixels thick)
    for i in range(1, rows - 1):
        output_grid[i, i - 1] = 3
        output_grid[i, i + 1] = 3
        output_grid[i, cols - i] = 3
        output_grid[i, cols - i - 2] = 3
        
    # Draw square (3x3 in the center)
    center = rows // 2
    for i in range(center - 1, center + 2):
        for j in range(center - 1, center + 2):
            output_grid[i,j] = 3

    return output_grid
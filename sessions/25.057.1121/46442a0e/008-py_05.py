"""
The input grid's dimensions are doubled to create an output grid.
The expanded input grid is superimposed to create an outline.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    rows, cols = input_grid.shape
    
    # Create output grid with doubled dimensions, initialized with zeros (or any default value)
    output_grid = np.zeros((2 * rows, 2 * cols), dtype=int)

    # Superimpose the expanded input grid.
    for i in range(rows):
        for j in range(cols):
            output_grid[i, j] = input_grid[i,j]
            output_grid[i+rows, j] = input_grid[i,j]
            output_grid[i, j+cols] = input_grid[i,j]
            output_grid[i+rows, j+cols] = input_grid[i,j]
    
    return output_grid
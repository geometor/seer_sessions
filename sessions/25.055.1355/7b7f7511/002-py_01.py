"""
The transformation extracts the top-left quadrant (or quarter-sized sub-grid) of the input grid. This is achieved by taking the width and dividing by 2, taking the height and dividing by two, and creating a new grid with the new dimensions. The content of the new grid consists of elements copied from the input grid.
"""

import numpy as np

def transform(input_grid):
    # Calculate output dimensions.
    output_width = input_grid.shape[1] // 2
    output_height = input_grid.shape[0] // 2

    # Initialize output_grid.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Extract sub-grid and populate output_grid.
    for i in range(output_height):
        for j in range(output_width):
            output_grid[i, j] = input_grid[i, j]
            
    return output_grid
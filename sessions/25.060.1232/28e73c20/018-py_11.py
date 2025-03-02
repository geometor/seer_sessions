"""
1. Copy the input grid to the output grid.
2. If the input grid is 3x3 and contains only the color blue, create a green border around the grid, leaving the center pixel blue.
3. Otherwise, fill the entire output grid with green.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input.
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Check if the grid is 3x3 and contains only blue.
    if height == 3 and width == 3 and np.all(output_grid == 1):
        # Create a green border.
        for i in range(height):
            for j in range(width):
                if i == 0 or i == height - 1 or j == 0 or j == width - 1:
                    output_grid[i, j] = 3
    else:
        # Fill the entire grid with green.
        output_grid[:] = 3

    return output_grid
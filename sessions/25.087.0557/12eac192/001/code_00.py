"""
Iterate through each pixel of the input grid. If a pixel has the color blue (1) or azure (8), change its color to green (3) in the output grid. Otherwise, keep the original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing blue (1) and azure (8) pixels to green (3).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    height, width = output_grid.shape

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel's color is blue (1) or azure (8)
            if input_grid[r, c] == 1 or input_grid[r, c] == 8:
                # Change the color to green (3) in the output grid
                output_grid[r, c] = 3
            # No else needed, as the output_grid already has the original color

    return output_grid
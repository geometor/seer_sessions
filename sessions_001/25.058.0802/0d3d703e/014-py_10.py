"""
The transformation rule is a color substitution cipher. Each color in the input grid is consistently replaced with a corresponding color in the output grid, while the grid structure itself remains unchanged. The mapping is: 5 -> 1, 8 -> 9, 6 -> 2.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by applying a color substitution cipher.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each pixel of the input grid.
    for i in range(height):
        for j in range(width):
            # Apply the color mapping.
            if input_grid[i, j] == 5:
                output_grid[i, j] = 1
            elif input_grid[i, j] == 8:
                output_grid[i, j] = 9
            elif input_grid[i, j] == 6:
                output_grid[i, j] = 2

    return output_grid
"""
The transformation rule performs a direct color substitution on each pixel of the input grid. Red pixels are changed to magenta, green pixels to yellow, and azure pixels to maroon. The dimensions of the grid remain unchanged. All other colors remain the same.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by applying a specific color mapping.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        list of lists: A 2D array representing the transformed output grid.
    """
    # initialize output_grid as a copy to avoid modifying the original input
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell of the output grid
    for i in range(rows):
        for j in range(cols):
            # Apply color mapping based on input pixel value
            if input_grid[i][j] == 2:
                output_grid[i][j] = 6
            elif input_grid[i][j] == 3:
                output_grid[i][j] = 4
            elif input_grid[i][j] == 8:
                output_grid[i][j] = 9

    return output_grid
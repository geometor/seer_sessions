"""
Each pixel in the input grid is expanded into a 2x2 block of the same color in the output grid. A single-pixel black border (color 0) is added to the top and bottom of the expanded grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating pixels and adding a black border.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    input_height, input_width = input_grid.shape

    # Initialize output_grid with correct dimensions:
    #  - Height: input_height * 2 (for duplication) + 2 (for top/bottom border)
    #  - Width:  input_width * 2 (for duplication)
    output_height = input_height * 2 + 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Duplicate pixels from input_grid to output_grid, offset by 1 row
    # to account for the top border.
    for row in range(input_height):
        for col in range(input_width):
            # Map input pixel to a 2x2 block in the output grid
            output_grid[2 * row + 1, 2 * col    ] = input_grid[row, col]
            output_grid[2 * row + 1, 2 * col + 1] = input_grid[row, col]
            output_grid[2 * row + 2, 2 * col    ] = input_grid[row, col]
            output_grid[2 * row + 2, 2 * col + 1] = input_grid[row, col]

    return output_grid
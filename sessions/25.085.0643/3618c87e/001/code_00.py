"""
Identify blue pixels (1) in the input grid. For each blue pixel found at position (row, col), change that position in the output grid to white (0). Then, change the pixel at the bottom row (last row) in the same column (position: height-1, col) to blue (1). All other pixels remain unchanged from the input.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the 'falling blue pixel' rule.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    grid = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to modify and return as the output
    output_grid = grid.copy()

    # Get the dimensions of the grid
    height, width = grid.shape
    bottom_row_index = height - 1

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the original input grid is blue (1)
            if grid[r, c] == 1:
                # If it's blue, change its original position in the output grid to white (0)
                output_grid[r, c] = 0
                # Change the pixel at the bottom row of the same column in the output grid to blue (1)
                output_grid[bottom_row_index, c] = 1

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()
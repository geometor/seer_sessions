"""
The transformation rule involves transposing the input grid, effectively swapping rows and columns. If the original dimensions are (height, width), the new dimensions will be (width, height). The values at input_grid[y][x] will be at output_grid[x][y].
"""

import numpy as np

def transform(input_grid):
    """
    Transposes the input grid.

    Args:
        input_grid: A 2D list or numpy array representing the input grid.

    Returns:
        A 2D list or numpy array representing the transposed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Transpose the array
    output_array = np.transpose(input_array)

    # Convert back to list
    output_grid = output_array.tolist()

    return output_grid
"""
Locates a 4x4 square of non-zero pixels within the input grid, extracts it, and transforms it into a 4x4 grid where all pixels are green (3).
"""

import numpy as np

def find_nonzero_square(grid):
    """
    Finds the 4x4 square of non-zero pixels.

    Args:
        grid: The input grid.

    Returns:
        A tuple (row, col) of the top-left corner of the square, or None if no such square exists.
    """
    grid_np = np.array(grid)
    rows, cols = grid_np.shape
    for i in range(rows - 3):
        for j in range(cols - 3):
            subgrid = grid_np[i:i+4, j:j+4]
            if np.all(subgrid != 0):  # Check if all pixels in the subgrid are non-zero
                return (i, j)
    return None

def transform(input_grid):
    """
    Transforms an input grid to an output grid based on the observed rule.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        list of lists: The transformed 2D array (output grid).
    """
    # Find the top-left corner of the 4x4 non-zero square
    start_row, start_col = find_nonzero_square(input_grid)

    # Initialize output_grid as all zeros
    output_grid = np.zeros((4, 4), dtype=int)

    # If the square wasn't found return black 4x4
    if start_row is None:
        return output_grid.tolist()

    # Fill the output grid with green (3)
    output_grid[:] = 3

    return output_grid.tolist()
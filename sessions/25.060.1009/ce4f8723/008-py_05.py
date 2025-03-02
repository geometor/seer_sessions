"""
Searches for a 4x4 square of non-zero pixels within the input grid. If found, returns a 4x4 green square; otherwise, returns a black grid of the same dimensions as the input.
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

    # Get input grid dimensions
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])


    # If the square wasn't found return black grid of same dimensions as input
    if start_row is None:
        output_grid = np.zeros((input_rows, input_cols), dtype=int)
        return output_grid.tolist()

    # Initialize output_grid as 4x4 of zeros
    output_grid = np.zeros((4, 4), dtype=int)

    # Fill the output grid with green (3)
    output_grid[:] = 3

    return output_grid.tolist()
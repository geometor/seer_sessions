"""
Identifies gray (5) pixels connected to magenta (6) pixels and changes them to white (0).
Magenta pixels remain unchanged.
"""

import numpy as np

def is_connected_to_magenta(grid, row, col):
    """
    Checks if a pixel at (row, col) is adjacent (directly or diagonally) to a magenta pixel.

    Args:
        grid: The input grid (NumPy array).
        row: The row index of the pixel.
        col: The column index of the pixel.

    Returns:
        True if connected to a magenta pixel, False otherwise.
    """
    rows, cols = grid.shape
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i != row or j != col) and grid[i, j] == 6:
                return True
    return False

def transform(input_grid):
    """
    Transforms the input grid by replacing gray pixels connected to magenta pixels with white pixels.
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is gray (5)
            if output_grid[i, j] == 5:
                # Check connectivity to magenta
                if is_connected_to_magenta(output_grid, i, j):
                    # Replace gray pixels with white (0) if connected
                    output_grid[i, j] = 0

    return output_grid
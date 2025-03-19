"""
Finds a 3x3 square of uniform color within the input grid and extracts it to form the output grid.
"""

import numpy as np

def find_3x3_square(input_grid):
    """
    Searches for a 3x3 square of a single color within the input grid.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        tuple: (row, col) of the top-left corner of the 3x3 square if found, otherwise None.
    """
    rows, cols = input_grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            color = input_grid[r, c]
            # Check if all pixels in the 3x3 block have the same color.
            if (input_grid[r:r+3, c:c+3] == color).all():
                return (r, c)
    return None

def transform(input_grid):
    """
    Finds a 3x3 square of uniform color within the input grid and extracts it to form the output grid.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The 3x3 output grid.
    """
    # Find the top-left corner of the 3x3 square.
    square_location = find_3x3_square(input_grid)

    if square_location:
        row, col = square_location
        # Extract the 3x3 square.
        output_grid = input_grid[row:row+3, col:col+3]
        return output_grid
    else:
        # Handle the case where no 3x3 square is found (shouldn't happen based on the problem description).
      return None

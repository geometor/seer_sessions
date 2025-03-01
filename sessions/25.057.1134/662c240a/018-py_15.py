"""
Examine the input grid and look for n x n squares of uniform color, where n is between 2 and 4 inclusive.
If a uniform square is found that matches the output, extract it to form the output.
"""

import numpy as np

def find_nxn_square(input_grid, n):
    """
    Searches for an nxn square of a single color within the input grid.

    Args:
        input_grid (numpy.ndarray): The input grid.
        n (int): size of square

    Returns:
        tuple: (row, col) of the top-left corner of the nxn square if found, otherwise None.
    """
    rows, cols = input_grid.shape
    for r in range(rows - (n - 1)):
        for c in range(cols - (n - 1)):
            color = input_grid[r, c]
            # Check if all pixels in the nxn block have the same color.
            if (input_grid[r:r+n, c:c+n] == color).all():
                return (r, c)
    return None

def transform(input_grid):
    """
    Finds an nxn square of uniform color within the input grid and extracts it to form the output grid, where n is between 2 and 4 inclusive.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The nxn output grid.
    """
    # Iterate through possible square sizes from 2x2 to 4x4.
    for n in range(2, 5):
        # Find the top-left corner of the nxn square.
        square_location = find_nxn_square(input_grid, n)

        if square_location:
            row, col = square_location
            # Extract the nxn square.
            output_grid = input_grid[row:row+n, col:col+n]
            return output_grid

    # Handle the case where no suitable square is found.
    return None
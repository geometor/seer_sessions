"""
Extracts non-zero digits (1, 3, 4, 5, and 7) from the input grid and arranges them into a 3x3 output grid
according to a specific order: 1, 3, 4, 5, 7. The order is fixed, and only these digits are placed in the output.
"""

import numpy as np

def get_digit_positions(grid):
    """
    Returns a dictionary of specified digit positions (row, col) in the grid.
    Only considers digits 1, 3, 4, 5, and 7.
    """
    positions = {}
    grid = np.array(grid)
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] in [1, 3, 4, 5, 7]:
                positions[grid[i, j]] = (i, j)
    return positions

def transform(input_grid):
    """
    Transforms the input grid by extracting specific non-zero digits (1, 3, 4, 5, 7)
    and arranging them in a 3x3 output grid in the fixed order: 1, 3, 4, 5, 7.
    """
    # Determine the order of digits
    order = [1, 3, 4, 5, 7]

    # Get the positions of the relevant non-zero digits in the input grid
    input_positions = get_digit_positions(input_grid)

    # Create a 3x3 output grid filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Populate the output grid based on the pre-determined order
    k = 0
    for digit in order:
        if digit in input_positions:
            row = k // 3
            col = k % 3
            output_grid[row+1, col] = digit  # offset to start on second row
            k += 1

    return output_grid
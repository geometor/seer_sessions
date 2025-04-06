"""
Transforms a 3x3 input grid by rotating its elements 180 degrees.
The element at input_grid[row][col] is moved to output_grid[2-row][2-col].
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rotates a 3x3 grid 180 degrees.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the grid rotated 180 degrees.
    """
    # Assuming the input is always 3x3 based on the examples
    rows = 3
    cols = 3

    # Initialize an output grid of the same size, filled with zeros or any placeholder
    # Using list comprehension for initialization
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the corresponding position in the output grid after 180-degree rotation
            # The new row index is (rows - 1 - r) = 2 - r
            # The new column index is (cols - 1 - c) = 2 - c
            new_r = rows - 1 - r
            new_c = cols - 1 - c

            # Assign the value from the input grid to the calculated position in the output grid
            output_grid[new_r][new_c] = input_grid[r][c]

    # Return the completed output grid
    return output_grid

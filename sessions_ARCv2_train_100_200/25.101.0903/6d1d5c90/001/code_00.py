"""
This transformation removes the first column from the input grid.
The height of the grid remains unchanged, while the width decreases by one.
The relative order and values of the pixels in the remaining columns are preserved.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Removes the first column from the input grid.

    Args:
        input_grid: The input 2D list representing the grid.

    Returns:
        A new 2D list representing the grid with the first column removed.
    """

    # Initialize an empty list to store the rows of the output grid.
    output_grid = []

    # Iterate through each row in the input grid.
    for row in input_grid:
        # Create a new row by slicing the original row, starting from the second element (index 1).
        # This effectively skips the first element (index 0).
        new_row = row[1:]
        # Append the new row (without the first column's element) to the output grid.
        output_grid.append(new_row)

    # Return the resulting grid.
    return output_grid

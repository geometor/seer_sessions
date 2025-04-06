"""
Takes an input grid and produces an output grid with the same height 
but double the width. Each row in the output grid is formed by 
concatenating the corresponding input row with itself.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Duplicates the input grid horizontally.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the output 2D grid, which is the
        input grid concatenated horizontally with itself.
    """
    # Initialize an empty list to store the rows of the output grid
    output_grid = []

    # Iterate through each row in the input grid
    for row in input_grid:
        # Create the new row by concatenating the current row with itself
        new_row = row + row
        # Append the newly created double-width row to the output grid
        output_grid.append(new_row)

    # Return the completed output grid
    return output_grid

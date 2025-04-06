"""
For each row in the input grid, create a new row by concatenating the current input row with itself. The output grid consists of these new, concatenated rows.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by concatenating each row with itself.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the output grid where each row is the
        concatenation of the corresponding input row with itself.
    """
    # Initialize an empty list to store the rows of the output grid
    output_grid = []

    # Iterate through each row in the input grid
    for row in input_grid:
        # Create a new row by concatenating the current row with itself
        # Example: if row is [1, 2, 3], new_row becomes [1, 2, 3, 1, 2, 3]
        new_row = row + row

        # Append the newly created concatenated row to the output grid
        output_grid.append(new_row)

    # Return the final output grid
    return output_grid

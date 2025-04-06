"""
Extracts the top-left 2x2 subgrid from the input grid.
The input grid is assumed to have at least 2 rows and 2 columns.
The output grid will always be a 2x2 grid containing the elements
from the first two rows and first two columns of the input grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects the top-left 2x2 portion of the input grid.

    Args:
        input_grid: A list of lists representing the input grid of integers.
                    It's assumed to have at least 2 rows and 2 columns.

    Returns:
        A 2x2 list of lists representing the top-left corner of the input grid.
    """
    # Initialize an empty list to store the output grid
    output_grid = []

    # Select the first row (index 0) from the input grid
    # and take the first two elements (index 0 and 1)
    row0 = input_grid[0][:2]
    output_grid.append(row0)

    # Select the second row (index 1) from the input grid
    # and take the first two elements (index 0 and 1)
    row1 = input_grid[1][:2]
    output_grid.append(row1)

    # Return the constructed 2x2 output grid
    return output_grid

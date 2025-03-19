"""
The output grid is a copy of the first column of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the first column of the input grid to create the output grid.
    """
    # Initialize the output grid as an empty list.
    output_grid = []

    # Iterate through each row of the input grid.
    for row in input_grid:
        # Append the first element (column 0) of the current row to the output grid.
        output_grid.append([row[0]])

    return output_grid
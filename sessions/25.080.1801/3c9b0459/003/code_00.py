"""
The transformation rule is to reverse each row of the input grid independently.  For each row in the input grid, create a new row where the elements are in the reversed order. The output grid is composed of these reversed rows.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as an empty list.
    output_grid = []

    # Iterate through each row in the input grid.
    for row in input_grid:
        # Reverse the current row and append it to the output grid.
        output_grid.append(row[::-1])

    return output_grid
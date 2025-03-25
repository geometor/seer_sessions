"""
Transforms a 3x3 input grid into a 3x3 output grid. Each column
in the output grid is filled with the value found at the second row
(index 1) of the corresponding column in the input grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 3x3 input grid into a 3x3 output grid.  Each column
    in the output grid is filled with the value found at the second row
    (index 1) of the corresponding column in the input grid."""

    # Initialize the output grid as a 3x3 array filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through each column of the input grid.
    for j in range(3):
        # Extract the value from the second row (index 1) of the current column.
        selected_value = input_grid[1, j]

        # Fill the corresponding column in the output grid with the selected value.
        output_grid[:, j] = selected_value

    return output_grid
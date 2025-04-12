import math
import numpy as np

"""
Transforms a 4x8 input grid into a 4x4 output grid.
The value of an output cell at (r, c) is 4 if and only if the input cells 
at (r, c) and (r, c+4) are both 0. Otherwise, the output cell value is 0.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on comparing cells from the left and right halves.

    Args:
        input_grid: A 4x8 list of lists containing integers (0, 5, 6).

    Returns:
        A 4x4 list of lists containing integers (0, 4).
    """
    # Get dimensions (assuming 4x8 input, generating 4x4 output)
    rows = 4
    output_cols = 4
    input_cols_offset = 4 # The offset to reach the right half of the input

    # Initialize the 4x4 output grid with zeros
    output_grid = [[0 for _ in range(output_cols)] for _ in range(rows)]

    # Iterate through each cell position (r, c) of the output grid
    for r in range(rows):
        for c in range(output_cols):
            # Get the corresponding values from the left and right halves of the input grid
            left_value = input_grid[r][c]
            right_value = input_grid[r][c + input_cols_offset]

            # Check the condition: both left and right values must be 0
            if left_value == 0 and right_value == 0:
                # If the condition is met, set the output cell to 4
                output_grid[r][c] = 4
            # Else: the output cell remains 0 (as initialized)

    # Return the completed 4x4 output grid
    return output_grid
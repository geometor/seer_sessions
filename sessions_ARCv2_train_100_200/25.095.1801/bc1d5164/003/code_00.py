import math
import numpy as np # Using numpy for potential future grid operations, though lists suffice here

"""
Constructs a 3x3 output grid by selecting elements from a 5x7 input grid.
Most selections use fixed index mappings:
- Output rows [0, 1, 2] map to Input rows [0, 1, 4].
- Output columns [0, 1, 2] map to Input columns [0, 5, 6].
The central output element (1, 1) has a conditional mapping:
- If Input[1, 5] is non-zero, Output[1, 1] takes the value of Input[1, 5].
- Otherwise, Output[1, 1] takes the value of Input[3, 5].
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 5x7 input grid into a 3x3 output grid using fixed and
    conditional element selection.

    Args:
        input_grid: A 5x7 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the output grid.
    """

    # Define the dimensions of the output grid
    output_rows = 3
    output_cols = 3

    # Initialize the output grid
    output_grid = [[0 for _ in range(output_cols)] for _ in range(output_rows)]

    # Define the fixed mapping from output indices to input indices
    # (excluding the central element which is handled conditionally)
    row_map = {0: 0, 1: 1, 2: 4}
    col_map = {0: 0, 1: 5, 2: 6}

    # Iterate through each cell of the output grid
    for r_out in range(output_rows):
        for c_out in range(output_cols):
            # Check if the current cell is the central cell (1, 1)
            if r_out == 1 and c_out == 1:
                # Apply conditional logic for the central cell
                primary_value = input_grid[1][5] # Value at Input[1, 5]
                if primary_value != 0:
                    # If Input[1, 5] is non-zero, use its value
                    value = primary_value
                else:
                    # Otherwise, use the value from Input[3, 5]
                    value = input_grid[3][5]
            else:
                # Apply fixed mapping for all other cells
                r_in = row_map[r_out]
                c_in = col_map[c_out]
                value = input_grid[r_in][c_in]

            # Assign the determined value to the output grid cell
            output_grid[r_out][c_out] = value

    # Return the populated output grid
    return output_grid
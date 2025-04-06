"""
Transforms a 3x6 input grid into a 3x3 output grid.
The value of each cell in the output grid at position (r, c) is determined
by checking the values in the input grid at positions (r, c) and (r, c + 3).
If the value at input_grid[r][c] is 4 OR the value at input_grid[r][c + 3] is 3,
the output_grid[r][c] is set to 6. Otherwise, it is set to 0.
"""

import copy # Potentially useful if modifying structures in place, though not strictly needed here.

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to map the input grid to the output grid.

    Args:
        input_grid: A 3x6 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the transformed output grid.
    """

    # Get dimensions (assuming consistent input structure based on examples)
    input_rows = len(input_grid)
    # Input columns are assumed to be 6
    # Output rows will be the same as input rows
    output_rows = input_rows
    # Output columns will be half the input columns
    output_cols = 3 # Hardcoded based on observed pattern

    # Initialize output_grid with zeros
    # Using list comprehension for conciseness
    output_grid = [[0 for _ in range(output_cols)] for _ in range(output_rows)]

    # Iterate through each cell of the target output grid dimensions
    for r in range(output_rows):
        for c in range(output_cols):
            # Get the corresponding values from the input grid
            # left_value is from the same (r, c) position in the input
            left_value = input_grid[r][c]
            # right_value is from the (r, c + output_cols) position in the input
            right_value = input_grid[r][c + output_cols] # c + 3

            # Apply the transformation rule
            # If the left value is 4 OR the right value is 3, set output to 6
            if left_value == 4 or right_value == 3:
                output_grid[r][c] = 6
            # Otherwise, the output remains 0 (as initialized)
            # else:
            #     output_grid[r][c] = 0 # This line is redundant due to initialization

    # Return the completed output grid
    return output_grid

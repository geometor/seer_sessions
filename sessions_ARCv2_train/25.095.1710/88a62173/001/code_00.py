"""
Constructs a 2x2 output grid by selecting specific elements from a 5x5 input grid.
The output grid's elements are determined as follows:
- Output[0, 0] is taken from Input[1, 1].
- Output[0, 1] is taken from Input[0, 4].
- Output[1, 0] is taken from Input[4, 0].
- Output[1, 1] is taken from Input[4, 4].
This effectively extracts one value from each of the four 2x2 quadrants formed when ignoring the central row and column of the input grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 5x5 input grid into a 2x2 output grid by selecting
    specific corner elements from the input grid's implied quadrants.

    Args:
        input_grid: A 5x5 list of lists representing the input grid.

    Returns:
        A 2x2 list of lists representing the output grid.
    """
    # Initialize a 2x2 output grid (using lists for now, could use numpy if preferred)
    output_grid = [[0, 0], [0, 0]]

    # Perform transformations based on the identified pattern

    # Select value from input grid at (row 1, col 1) for output (row 0, col 0)
    # This corresponds to the bottom-right of the top-left quadrant
    output_grid[0][0] = input_grid[1][1]

    # Select value from input grid at (row 0, col 4) for output (row 0, col 1)
    # This corresponds to the top-right of the top-right quadrant
    output_grid[0][1] = input_grid[0][4]

    # Select value from input grid at (row 4, col 0) for output (row 1, col 0)
    # This corresponds to the bottom-left of the bottom-left quadrant
    output_grid[1][0] = input_grid[4][0]

    # Select value from input grid at (row 4, col 4) for output (row 1, col 1)
    # This corresponds to the bottom-right of the bottom-right quadrant
    output_grid[1][1] = input_grid[4][4]

    return output_grid

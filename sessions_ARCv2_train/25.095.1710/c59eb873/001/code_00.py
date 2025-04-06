import math
import numpy as np # Note: Using numpy could simplify grid operations, but sticking to basic lists as per examples
from typing import List, Tuple 

"""
Expands an input grid by doubling its dimensions. Each element in the
input grid becomes a 2x2 block of that same element in the output grid.
"""

# No external libraries beyond standard types are strictly necessary for this logic

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid by replacing each element with a 2x2 block 
    of that element, effectively doubling the grid's dimensions.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A new list of lists representing the expanded output grid.
    """
    # Handle edge case: empty input grid
    if not input_grid or not input_grid[0]:
        return []

    # Get dimensions of the input grid
    input_rows = len(input_grid)
    input_cols = len(input_grid[0]) # Assuming a rectangular grid

    # Calculate dimensions for the output grid
    output_rows = input_rows * 2
    output_cols = input_cols * 2

    # Initialize the output grid - can pre-allocate or build row by row.
    # Building row by row might be slightly more Pythonic for lists.
    output_grid = []

    # Iterate through each row of the input grid
    for r in range(input_rows):
        # For each input row, we will generate two output rows
        output_row_part1 = []
        output_row_part2 = []

        # Iterate through each column (element) in the current input row
        for c in range(input_cols):
            # Get the element value from the input grid
            element_value = input_grid[r][c]

            # Append the element twice to the first output row part
            output_row_part1.append(element_value)
            output_row_part1.append(element_value)

            # Append the element twice to the second output row part
            output_row_part2.append(element_value)
            output_row_part2.append(element_value)
            # This effectively creates the horizontal expansion [e, e] for the 2x2 block

        # Add the two newly constructed rows to the final output grid
        output_grid.append(output_row_part1)
        output_grid.append(output_row_part2)
        # Adding both rows achieves the vertical expansion for the 2x2 block

    return output_grid

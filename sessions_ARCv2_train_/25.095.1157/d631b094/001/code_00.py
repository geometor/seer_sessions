import math
import numpy as np

"""
Extracts all non-zero integer values from a 3x3 input grid and returns them as a flat list, 
maintaining the order they appear when scanning the grid row by row, left to right.
"""

def transform(input_grid: list[list[int]]) -> list[int]:
    """
    Transforms a 3x3 grid of integers into a list containing only the non-zero elements
    in their original scan order (row-major).

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A list of integers containing the non-zero elements from the input grid.
    """

    # Initialize an empty list to store the non-zero elements
    output_sequence = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Iterate through each element (cell) in the current row
        for cell_value in row:
            # Check if the cell value is not zero
            if cell_value != 0:
                # If the value is non-zero, append it to the output list
                output_sequence.append(cell_value)

    # Return the list containing all collected non-zero values
    return output_sequence

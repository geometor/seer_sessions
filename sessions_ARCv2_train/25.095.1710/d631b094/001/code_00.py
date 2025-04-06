"""
Extracts all non-zero integer values from a 3x3 input grid and returns them as a single list, preserving the order encountered during a row-major (top-to-bottom, left-to-right) traversal of the grid.
"""

import numpy as np  # Using numpy for easier grid handling, though not strictly necessary

def transform(input_grid: list[list[int]]) -> list[int]:
    """
    Transforms a 3x3 grid of integers into a list containing only the non-zero elements,
    ordered by their appearance in a row-major traversal of the input grid.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A list of integers containing the non-zero elements from the input grid
        in row-major order.
    """
    # Initialize an empty list to store the non-zero numbers
    output_sequence = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Iterate through each cell (number) in the current row
        for number in row:
            # Check if the number is not zero
            if number != 0:
                # If the number is not zero, append it to the output sequence
                output_sequence.append(number)

    # Return the final sequence containing all collected non-zero numbers
    return output_sequence

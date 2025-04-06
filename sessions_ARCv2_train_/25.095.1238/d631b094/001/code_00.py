import numpy as np

"""
Scans the input grid row by row, left to right, and collects all non-zero digits into a sequence, preserving the order of appearance. The final output is a space-separated string of these collected digits.
"""

def transform(input_grid: list[list[int]]) -> str:
    """
    Extracts non-zero digits from a grid and returns them as a space-separated string.

    Args:
        input_grid: A 3x3 list of lists of integers representing the input grid.

    Returns:
        A string containing the non-zero digits from the input grid,
        in row-major order, separated by spaces.
    """
    # Initialize an empty list to store the non-zero digits
    output_digits = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Iterate through each cell (digit) in the current row
        for digit in row:
            # Check if the digit is not zero
            if digit != 0:
                # If non-zero, convert it to a string and append to the list
                output_digits.append(str(digit))

    # Join the collected digits with spaces to form the final output string
    output_string = " ".join(output_digits)

    # Return the resulting string
    return output_string

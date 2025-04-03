"""
Iterate through the input 3x3 grid, row by row, then column by column.
Collect all non-zero digits encountered during the iteration.
Format the collected non-zero digits into a space-separated string.
"""

import numpy as np # Common library, might be useful for grid operations, although simple iteration is sufficient here

def transform(input_grid):
    """
    Transforms a 3x3 grid of digits by extracting non-zero digits and
    returning them as a space-separated string.

    Args:
        input_grid (list of list of int): A 3x3 grid representing the input.

    Returns:
        str: A string containing the non-zero digits from the input grid,
             separated by spaces, in reading order (left-to-right, top-to-bottom).
    """
    # Initialize an empty list to store the non-zero digits found
    output_digits = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Iterate through each cell (digit) in the current row
        for cell in row:
            # Check if the digit is non-zero
            if cell != 0:
                # If non-zero, convert the digit to a string and add it to the list
                output_digits.append(str(cell))

    # Join the collected digits with spaces to form the final output string
    output_string = " ".join(output_digits)

    # Return the formatted string
    return output_string

import math  # Include common math library, though not strictly needed for this task
import numpy as np # Include common science library, though not strictly needed for this task

"""
Identifies the background color from the top-left cell of the input grid.
Scans the grid row by row, then column by column.
Collects all cell values (digits) that are *not* the background color, preserving the scanning order.
Formats the collected digits into a list where each digit is in its own single-element list.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts foreground digits from a grid based on the background color
    (identified from the top-left cell) and returns them in scan order.

    Args:
        input_grid: A 2D list of integers representing the grid.

    Returns:
        A list of lists, where each inner list contains a single foreground digit
        encountered during a top-to-bottom, left-to-right scan.
    """
    # Initialize an empty list to store the foreground digits found
    output_digits = []

    # Check for an empty or invalid input grid
    if not input_grid or not input_grid[0]:
        # If the grid is empty, return an empty list
        return []

    # Step 1: Identify the background digit.
    # Assume the digit at the top-left corner (0, 0) is the background.
    background_digit = input_grid[0][0]

    # Step 2: Scan the grid row by row, then column by column.
    # Iterate through each row in the input grid
    for row_index in range(len(input_grid)):
        # Iterate through each cell (digit) in the current row
        for col_index in range(len(input_grid[row_index])):
            # Get the value of the current cell
            cell_value = input_grid[row_index][col_index]

            # Step 3: Check if the cell's digit is different from the background digit.
            if cell_value != background_digit:
                # Step 4: If it's a foreground digit, collect it.
                output_digits.append(cell_value)

    # Step 5: Format the collected digits into the required output structure.
    # The output should be a list of lists, where each inner list contains one digit.
    output_grid = [[digit] for digit in output_digits]

    # Return the formatted list of foreground digits
    return output_grid
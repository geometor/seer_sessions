"""
Extracts a specific 2x2 subgrid from a larger input grid based on the input grid's width.
The subgrid starts at row 0. The starting column is calculated based on the width (W)
of the input grid: if W is even, the start column is W // 2; if W is odd, the start
column is 0. The extracted subgrid always spans 2 rows and 2 columns.
"""

import math # Although not strictly needed for this logic, it's a common math library

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts a 2x2 subgrid from the input grid based on width parity.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the 2x2 extracted subgrid.
    """
    # Initialize output_grid
    output_grid = []

    # Ensure the input grid has at least 2 rows and enough columns
    if not input_grid or len(input_grid) < 2:
        # Handle error or return empty/default based on expected behavior for invalid input
        # For this task, based on examples, we assume valid input >= 2x2 dimensions needed for extraction
        return [] # Returning empty for invalid input

    # Determine the width (number of columns) of the input grid
    # Assuming a rectangular grid, width is the length of the first row
    width = len(input_grid[0]) if input_grid else 0

    if width < 2:
         # Handle error or return empty/default if width is insufficient
        return []

    # Calculate the starting column index (C) for the subgrid
    start_col = 0
    if width % 2 == 0:
        # If width is even, start column is width / 2
        start_col = width // 2
    else:
        # If width is odd, start column is 0
        start_col = 0

    # Check if the calculated start column allows for extracting 2 columns
    if start_col + 1 >= width:
         # Handle error or return empty/default if extraction goes out of bounds
         return []

    # Extract the 2x2 subgrid
    # Row 1 of the subgrid
    row1 = input_grid[0][start_col : start_col + 2]
    # Row 2 of the subgrid
    row2 = input_grid[1][start_col : start_col + 2]

    output_grid.append(row1)
    output_grid.append(row2)

    return output_grid

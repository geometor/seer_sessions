import math
import numpy as np
# Add other imports as needed, for example:
# import re

"""
1. Obtain the input grid and determine its number of rows (R) and columns (C).
2. Evaluate if both R and C are even numbers.
3. If R and C are both even, identify the 2x2 subgrid located at rows 0 and 1, and columns C-2 and C-1 (the top-right 2x2 corner).
4. If the condition in step 2 is false (i.e., R is odd or C is odd or both are odd), identify the 2x2 subgrid located at rows 0 and 1, and columns 0 and 1 (the top-left 2x2 corner).
5. Construct the output grid using the elements from the identified 2x2 subgrid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the parity of its dimensions.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A 2x2 list of lists representing the extracted subgrid.
    """

    # 1. Obtain the dimensions of the input grid
    rows = len(input_grid)
    # Handle potential empty input grid or rows
    if rows == 0:
        return [] # Or raise an error, depending on requirements
    cols = len(input_grid[0])
    if cols == 0:
         return [[] for _ in range(rows)] # Or raise error

    # 2. Check if both dimensions are even
    both_even = (rows % 2 == 0) and (cols % 2 == 0)

    # 3. Determine the starting column for the 2x2 subgrid
    if both_even:
        # Top-right corner (adjusting for 0-based index)
        start_col = cols - 2
    else:
        # 4. Top-left corner
        start_col = 0

    # Always take from the top rows (row 0 and 1)
    start_row = 0

    # 5. Extract the 2x2 subgrid
    # Initialize the output grid
    output_grid = []
    # Iterate through the 2 rows of the subgrid
    for r in range(start_row, start_row + 2):
        # Check if the row exists (important for input grids with < 2 rows)
        if r < rows:
            new_row = []
            # Iterate through the 2 columns of the subgrid
            for c in range(start_col, start_col + 2):
                 # Check if the column exists (important for input grids with < 2 cols)
                 if c < cols:
                     new_row.append(input_grid[r][c])
                 else:
                     # Handle cases where grid is too small - this might need refinement
                     # based on expected behavior for grids smaller than 2x2 in the target corner
                     pass # Or append a default value, or raise error
            output_grid.append(new_row)
        else:
            # Handle cases where grid is too small vertically
            pass # Or append default rows, or raise error

    # Ensure the output is strictly 2x2, even if the source wasn't large enough
    # This part might need adjustment based on how edge cases (input < 2x2) should be handled.
    # The current logic implicitly handles it by just extracting what's available.
    # If a guaranteed 2x2 output is needed even for smaller inputs, padding logic would be required here.

    return output_grid
"""
Extracts the 3x3 subgrid located in the top-right corner of the input 9x9 grid.
The top-right subgrid includes elements from rows 0, 1, and 2, and columns 6, 7, and 8
of the input grid (using 0-based indexing).
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts the top-right 3x3 subgrid from a 9x9 input grid.

    Args:
        input_grid: A 9x9 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the top-right subgrid.
    """
    # Convert input list of lists to a NumPy array for easier slicing
    input_array = np.array(input_grid)

    # Define the row and column indices for the top-right 3x3 subgrid
    start_row, end_row = 0, 3  # Rows 0, 1, 2 (end is exclusive)
    start_col, end_col = 6, 9  # Columns 6, 7, 8 (end is exclusive)

    # Extract the subgrid using NumPy slicing
    # Select rows from start_row up to (but not including) end_row
    # Select columns from start_col up to (but not including) end_col
    output_subgrid_array = input_array[start_row:end_row, start_col:end_col]

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_subgrid_array.tolist()

    return output_grid

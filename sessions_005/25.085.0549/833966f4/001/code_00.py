"""
Takes an input grid and swaps the contents of adjacent pairs of rows.
Iterates through the rows starting from the top (index 0) with a step of 2.
If a row `i` and the next row `i+1` both exist, their contents are swapped.
If the grid has an odd number of rows, the last row remains in its original position.
"""

import numpy as np

def transform(input_grid):
    """
    Swaps adjacent pairs of rows in the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A new 2D numpy array with adjacent rows swapped.
    """
    # Get the dimensions of the input grid
    num_rows, num_cols = input_grid.shape

    # Initialize output_grid as a copy of the input_grid
    # This ensures that any rows not involved in a swap (like the last row in an odd-height grid)
    # retain their original values.
    output_grid = np.copy(input_grid)

    # Iterate through the rows with a step of 2
    # The loop goes from row 0 up to num_rows - 1 (exclusive), stepping by 2.
    # This correctly handles both even and odd numbers of rows.
    for i in range(0, num_rows, 2):
        # Check if the next row (i + 1) exists within the grid boundaries
        if i + 1 < num_rows:
            # Swap the contents of row i and row i + 1 in the output grid
            # We use .copy() to ensure we are swapping the values, not just references,
            # although direct assignment works for row swapping in numpy.
            # Store row i temporarily
            temp_row = np.copy(output_grid[i, :])
            # Copy row i+1 to row i
            output_grid[i, :] = output_grid[i + 1, :]
            # Copy the original row i (stored in temp_row) to row i+1
            output_grid[i + 1, :] = temp_row

    # Return the modified grid
    return output_grid
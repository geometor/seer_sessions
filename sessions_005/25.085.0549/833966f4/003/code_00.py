"""
Transforms the input grid by swapping the first two rows and the last two rows.
1. Creates a copy of the input grid.
2. If the grid has 2 or more rows, swaps the row at index 0 with the row at index 1.
3. If the grid has 4 or more rows, swaps the row at index n-2 with the row at index n-1 (where n is the number of rows).
4. Rows between the first pair and the last pair remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Swaps the first two rows and the last two rows of the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A new 2D numpy array with the specified rows swapped.
    """
    # Get the number of rows
    num_rows = input_grid.shape[0]

    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Check if there are at least 2 rows to perform the first swap
    if num_rows >= 2:
        # Swap the first row (index 0) and the second row (index 1)
        # Store row 0 temporarily
        temp_row_0 = np.copy(output_grid[0, :])
        # Copy row 1 to row 0
        output_grid[0, :] = output_grid[1, :]
        # Copy the original row 0 (stored in temp_row_0) to row 1
        output_grid[1, :] = temp_row_0

    # Check if there are at least 4 rows to perform the second swap
    # The second swap involves the last two rows (n-2 and n-1)
    if num_rows >= 4:
        # Swap the second-to-last row (index n-2) and the last row (index n-1)
        # Store row n-2 temporarily
        temp_row_n_minus_2 = np.copy(output_grid[num_rows - 2, :])
        # Copy row n-1 to row n-2
        output_grid[num_rows - 2, :] = output_grid[num_rows - 1, :]
        # Copy the original row n-2 (stored in temp_row_n_minus_2) to row n-1
        output_grid[num_rows - 1, :] = temp_row_n_minus_2

    # Return the modified grid
    return output_grid
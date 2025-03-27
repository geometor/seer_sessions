"""
Extracts a subgrid from the input grid by removing the first row and the first column.
The output grid is the portion of the input grid starting from the second row (index 1) 
and the second column (index 1).
"""

import numpy as np

def transform(input_grid):
    """
    Removes the first row and first column from the input grid.

    Args:
        input_grid (list of list of int): A 2D list representing the input grid.

    Returns:
        list of list of int: A 2D list representing the output grid, which is 
                             the input grid with the first row and column removed.
    """
    # Convert the input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Check if the input grid has at least 2 rows and 2 columns
    if input_array.shape[0] < 1 or input_array.shape[1] < 1:
        # Handle edge case: If the grid is too small to remove a row/column, 
        # perhaps return an empty grid or handle as an error.
        # For this task, based on examples, inputs are larger.
        # If the input is 1xN or Nx1, removing a row AND column results in empty.
        # If it's exactly 1x1, it becomes 0x0.
        # Let's assume valid inputs based on the pattern (>= 2x2 for non-empty output)
        # If input is 1xN or Mx1, slicing [1:, 1:] might yield unexpected results or errors depending on numpy version.
        # A robust solution checks dimensions.
        if input_array.shape[0] <= 1 or input_array.shape[1] <= 1:
            return [] # Return an empty list for grids too small to produce the expected 6x6 output

    # Select the subgrid starting from the second row (index 1) and second column (index 1)
    # The slice `1:` means from index 1 to the end.
    output_array = input_array[1:, 1:]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

"""
Transforms a 5x5 input grid containing 0s and 5s into a 5x5 output grid.
The output grid is initially all zeros. A single '1' is placed in the first
row of the output grid. The column index of this '1' depends on the index
of the leftmost column in the input grid that contains at least one '5'.
If the leftmost column with a '5' is index 1, the '1' goes in output[0][1].
If the leftmost column with a '5' is index 2, the '1' goes in output[0][0].
"""

import numpy as np

def find_leftmost_col_with_value(grid, value):
    """
    Finds the index of the leftmost column containing the specified value.

    Args:
        grid (np.array): The input grid.
        value (int): The value to search for.

    Returns:
        int: The index of the leftmost column containing the value, or -1 if not found.
    """
    rows, cols = grid.shape
    for c in range(cols):
        if np.any(grid[:, c] == value):
            return c
    return -1 # Should not happen based on problem description, but good practice

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 5x5 grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed 5x5 grid as a list of lists.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid)
    rows, cols = input_np.shape

    # Initialize output_grid with zeros
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the index of the leftmost column containing a '5'
    leftmost_col_idx = find_leftmost_col_with_value(input_np, 5)

    # Place the '1' in the output grid based on the leftmost column index
    if leftmost_col_idx == 1:
        output_grid[0, 1] = 1
    elif leftmost_col_idx == 2:
        output_grid[0, 0] = 1
    # Add handling for other cases if necessary, though based on examples only 1 and 2 occur

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()

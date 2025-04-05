"""
Iterate through each cell of the input grid. If a cell's value is 6, set the corresponding cell in the output grid to 0. Otherwise, copy the input cell's value to the output cell.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all occurrences of the number 6 with 0.

    Args:
        input_grid (list of list of int): The input 2D grid.

    Returns:
        list of list of int: The transformed 2D grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Create a copy of the input array to modify as the output grid
    # This handles the case where values are copied if they are not 6
    output_array = input_array.copy()

    # Find the indices (rows and columns) where the value is 6
    rows, cols = np.where(input_array == 6)

    # Iterate through the found locations and set the corresponding value in the output array to 0
    # Although NumPy allows direct assignment like output_array[input_array == 6] = 0,
    # iterating explicitly matches the natural language program step-by-step for clarity here.
    # A more efficient NumPy way: output_array[input_array == 6] = 0
    for r, c in zip(rows, cols):
        # If the value at the input cell (r, c) is 6 (which it is, based on np.where),
        # set the corresponding output cell to 0.
        output_array[r, c] = 0

    # Convert the output NumPy array back to a list of lists format
    output_grid = output_array.tolist()

    return output_grid

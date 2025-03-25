"""
Iterate through each cell of the input grid. If the cell's value is '6' (magenta), replace it with '2' (red). Otherwise, keep the original value. Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all instances of the digit 6 with the digit 2.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list to a NumPy array for easier manipulation
    output_grid = np.array(input_grid)

    # Replace all occurrences of 6 with 2
    output_grid[output_grid == 6] = 2

    # Convert the NumPy array back to a list of lists
    return output_grid.tolist()
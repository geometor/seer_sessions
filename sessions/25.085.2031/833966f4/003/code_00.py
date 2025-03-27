"""
Transforms an input grid by swapping adjacent rows based on their index.
Specifically, it swaps rows i and i+1 if the index i is divisible by 3 (i % 3 == 0).
The grid dimensions remain unchanged.
"""

import numpy as np
import copy

def transform(input_grid):
    """
    Swaps adjacent rows i and i+1 in the input grid if i % 3 == 0.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A new list of lists representing the transformed grid.
    """
    # Convert input grid (list of lists) to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Create a copy of the input array to modify for the output
    # Using deepcopy might be safer if lists contain mutable elements, but np.copy is fine for arrays of ints.
    output_array = np.copy(input_array)

    # Get the number of rows (height) of the grid
    height = input_array.shape[0]

    # Iterate through the row indices, up to the second-to-last row
    # We stop at height - 2 because we are swapping pairs (i, i+1)
    for i in range(height - 1):
        # Check if the current row index i is divisible by 3
        if i % 3 == 0:
            # Swap the entire row i with row i+1 in the output array
            # NumPy allows direct swapping using fancy indexing
            output_array[[i, i+1]] = output_array[[i+1, i]]

    # Convert the NumPy array back to a list of lists for the expected output format
    output_grid = output_array.tolist()

    return output_grid

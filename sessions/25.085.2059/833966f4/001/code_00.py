"""
Rearrange elements in a 1D list by swapping adjacent pairs where the starting index of the pair is divisible by 3.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid (a 1D list/array) by swapping adjacent elements
    based on their starting index.

    Args:
        input_grid (np.ndarray): A numpy array representing the input grid.
                                 Expected to be 1D or effectively 1D (e.g., Nx1 or 1xN).

    Returns:
        np.ndarray: The transformed grid with elements swapped according to the rule.
    """
    # Ensure the input is treated as a 1D array for easier processing
    # Flatten the array if it's multi-dimensional but represents a single row or column
    if input_grid.ndim > 1:
        flat_list = input_grid.flatten().tolist()
    else:
        flat_list = input_grid.tolist()

    # Create a copy of the list to modify
    output_list = flat_list[:]
    n = len(output_list)

    # Iterate through the indices of the list
    # We stop at n-2 because we are looking at pairs (i, i+1)
    for i in range(n - 1):
        # Check if the current index i is divisible by 3
        if i % 3 == 0:
            # Swap the element at index i with the element at index i+1
            output_list[i], output_list[i+1] = output_list[i+1], output_list[i]

    # Convert the modified list back into a numpy array with the original orientation if possible
    # Assuming the output should have the same shape as the input if it was Nx1 or 1xN
    output_grid = np.array(output_list).reshape(input_grid.shape)

    return output_grid

"""
1. Flatten the input grid into a 1D array.
2. Sort the flattened array in descending order.
3. Reshape the sorted array into the dimensions of the original grid.
4. Sort each row of this intermediate reshaped grid in ascending order.
5. Reverse the order of rows.
"""

import numpy as np

def transform(input_grid):
    # Flatten the input grid into a 1D array.
    flattened_grid = input_grid.flatten()

    # Sort the flattened array in descending order.
    sorted_elements = np.sort(flattened_grid)[::-1]

    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Reshape the sorted elements back into the original grid dimensions.
    reshaped_grid = sorted_elements.reshape(rows, cols)

    # Sort each row of the reshaped grid in ascending order.
    for i in range(rows):
        reshaped_grid[i, :] = np.sort(reshaped_grid[i, :])

    # Reverse the order of the rows
    output_grid = reshaped_grid[::-1]
    return output_grid
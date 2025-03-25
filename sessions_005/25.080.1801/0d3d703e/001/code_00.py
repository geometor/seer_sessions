"""
Performs an element-wise substitution on a grid based on a predefined mapping.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by replacing each pixel's value with a
    corresponding value from a predefined mapping.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)

    # Define the mapping dictionary.
    mapping = {
        3: 4,
        1: 5,
        2: 6,
        8: 9,
        5: 1,
        9: 8,
        4: 3,
    }

    # Iterate through each pixel in the grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Replace the pixel's value with its mapped value.
            original_value = output_grid[i, j]
            output_grid[i, j] = mapping.get(original_value, original_value) # Use .get() to handle potential missing keys

    return output_grid
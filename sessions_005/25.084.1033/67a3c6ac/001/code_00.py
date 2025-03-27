"""
Transform the input grid by flipping it horizontally. The pixel value at input 
coordinate (row, column) is moved to the output coordinate (row, grid_width - 1 - column).
"""

import numpy as np

def transform(input_grid):
    """
    Flips the input grid horizontally.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the horizontally flipped output grid.
    """
    # Convert the input list of lists to a NumPy array for efficient manipulation
    input_array = np.array(input_grid, dtype=int)

    # Use NumPy's fliplr function to flip the array horizontally (left to right)
    # This achieves the transformation where output[r, c] = input[r, width - 1 - c]
    output_array = np.fliplr(input_array)

    # Convert the resulting NumPy array back to a list of lists format
    output_grid = output_array.tolist()

    # Return the transformed grid
    return output_grid

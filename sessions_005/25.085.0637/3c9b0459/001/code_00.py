"""
Rotates the input grid by 180 degrees to produce the output grid.
Each pixel at position (row, col) in the input grid is moved to the 
position (height - 1 - row, width - 1 - col) in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the 180-degree rotated grid.
    """
    # Convert the input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions of the grid
    height, width = input_array.shape

    # Create an output array of the same shape, initialized with zeros (or any placeholder)
    # Alternatively, we can directly calculate the rotated array using numpy functions
    
    # Perform a 180-degree rotation using numpy.rot90 twice
    # np.rot90 rotates 90 degrees counter-clockwise by default. k=2 means rotate 180 degrees.
    output_array = np.rot90(input_array, k=2)

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

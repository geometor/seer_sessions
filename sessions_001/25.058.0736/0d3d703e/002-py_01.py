"""
The transformation rule is to increment the value of each pixel in the input grid by 1 to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by incrementing each pixel's value by 1.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the output grid.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.array(input_grid)

    # Iterate over each pixel in the input grid and increment its value by 1.
    output_grid = output_grid + 1 # using numpy element-wise addition
    
    return output_grid.tolist()
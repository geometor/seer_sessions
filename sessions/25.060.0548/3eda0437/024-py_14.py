"""
The transformation rule is to replace the rightmost three columns of zeros in the input grid with magenta (color code 6) pixels, while keeping all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing the rightmost three columns of zeros with magenta pixels.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = [row[:] for row in input_grid]
    
    # Convert to numpy array for easier manipulation
    output_grid = np.array(output_grid)
    input_grid = np.array(input_grid)
    
    # Get the number of columns
    num_cols = output_grid.shape[1]

    # Replace the last three columns with 6 if they are all zeros
    if np.all(input_grid[:, num_cols-3:] == 0):
      output_grid[:, num_cols-3:] = 6


    return output_grid.tolist()
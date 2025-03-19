"""
Transforms the input grid by filling rows containing red pixels with red and clearing others.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid based on the presence of red pixels in each row.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Initialize output_grid with zeros (white), same dimensions as input_grid
    output_grid = np.zeros_like(input_grid)

    # Iterate through rows
    for i, row in enumerate(input_grid):
        # Check if the row contains any red (2) pixels
        if 2 in row:
            # Fill the entire row with red (2) in the output grid
            output_grid[i, :] = 2
        else:
            # set all other pixels to white, which they are
            # already initialized to
            pass
    
    return output_grid
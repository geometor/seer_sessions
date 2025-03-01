"""
Extracts the color value from the top-left corner of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top-left element of the input grid.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        int: The value at the top-left corner of the input grid.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Extract the top-left element (0,0)
    top_left_element = input_array[0, 0]
    
    # Create output grid, a 1x1 matrix with top_left_element
    output_grid = np.array([[top_left_element]])

    return output_grid.tolist()
"""
Counts the number of blue pixels (value 1) in the input grid and returns the count.
"""

import numpy as np

def transform(input_grid):
    """
    Counts the number of blue pixels (value 1) in the input grid.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        int: The total count of blue pixels.
    """
    # Count the number of pixels with value 1 (blue)
    count = np.count_nonzero(input_grid == 1)
    
    return count
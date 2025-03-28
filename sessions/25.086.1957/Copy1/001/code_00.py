"""
This module defines a function to transform an input grid by duplicating it 
horizontally. The output grid has the same height as the input grid but double 
the width, consisting of the original input grid concatenated with an identical 
copy of itself placed to the right.
"""

import numpy as np

def transform(input_grid):
    """
    Duplicates the input grid horizontally.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed grid, which is
                  the input grid concatenated horizontally with itself.
    """
    # Concatenate the input grid with itself along the horizontal axis (axis=1)
    # This effectively places a copy of the input grid to the right of the original.
    output_grid = np.concatenate((input_grid, input_grid), axis=1)
    
    return output_grid

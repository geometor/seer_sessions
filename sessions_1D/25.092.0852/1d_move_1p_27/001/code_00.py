"""
Shift the initial colored block one position to the right.
The input is treated as a single row (1xN grid).
A white pixel (0) is inserted at the beginning (index 0) of the row.
The elements from the input row, excluding the last one, are shifted one position to the right.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the content of a 1xN grid one position to the right, 
    inserting a white pixel (0) at the beginning and discarding the last element.

    Args:
        input_grid: A numpy array representing the 1xN input grid.

    Returns:
        A numpy array representing the transformed 1xN output grid.
    """
    # Ensure input is treated as a 2D array (even if 1 row)
    if input_grid.ndim == 1:
        input_grid = np.array([input_grid]) # Treat 1D array as a single row

    # Get the dimensions (height will be 1, width is the length)
    height, width = input_grid.shape

    # Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Check if the grid has any columns to shift
    if width > 0:
        # Select elements from the input grid's first row, excluding the last element
        elements_to_shift = input_grid[0, :-1]
        
        # Place these elements into the output grid's first row, starting from the second position (index 1)
        output_grid[0, 1:] = elements_to_shift

    # The first element (index 0) of the output grid remains 0 (white) as initialized

    return output_grid

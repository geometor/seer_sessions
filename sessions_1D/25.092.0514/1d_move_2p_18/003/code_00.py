"""
Transforms a 1D input grid by shifting its contents 2 positions to the right.
The first two positions of the output grid are filled with the background
color (0), and the content that would be shifted off the right edge is
discarded.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the content of the input grid 2 positions to the right.

    Args:
        input_grid: A 1D numpy array representing the input row.

    Returns:
        A 1D numpy array representing the transformed row.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Get the width (number of elements) of the 1D input grid
    width = input_grid.shape[0]

    # Define the amount by which to shift the content to the right
    shift_amount = 2

    # Initialize the output grid with the same shape as the input,
    # filled entirely with the background color (0)
    output_grid = np.zeros_like(input_grid)

    # Check if the grid is wide enough to perform the shift
    if width > shift_amount:
        # Determine the slice of the input grid to copy.
        # This slice includes elements from the start up to (but not including)
        # the last 'shift_amount' elements.
        # Example: width=17, shift=2 -> copy input_grid[0:15]
        input_slice = input_grid[:width - shift_amount]

        # Determine the target slice in the output grid.
        # This slice starts at index 'shift_amount' and goes to the end.
        # Example: width=17, shift=2 -> paste into output_grid[2:17]
        output_slice_start = shift_amount
        # The end index is implicitly the end of the array when using slicing like [start:]

        # Copy the selected part of the input grid to the shifted position
        # in the output grid.
        output_grid[output_slice_start:] = input_slice

    # The first 'shift_amount' elements of the output grid remain 0 (background)
    # due to the initialization with np.zeros_like.
    # Elements shifted beyond the original width are implicitly discarded
    # because we only copy 'width - shift_amount' elements.

    return output_grid
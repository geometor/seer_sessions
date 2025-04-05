"""
Transform the input grid by performing a circular left shift on the elements 
within its first (and only) row. The first element moves to the last position, 
and all other elements shift one position to the left.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a circular left shift to the first row of the input grid.

    Args:
        input_grid: A 2D NumPy array, expected to have at least one row. 
                      Based on examples, it usually has shape (1, N).

    Returns:
        A 2D NumPy array with the same shape as the input, where the first row's
        elements have been circularly shifted one position to the left.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
      # This case shouldn't happen with the framework but is good practice
      raise TypeError("Input must be a NumPy array.")

    # Check if the grid is empty
    if input_grid.size == 0:
        return np.copy(input_grid) # Return an empty grid of the same shape

    # Extract the first row
    # Assuming the relevant data is always in the first row based on examples
    first_row = input_grid[0]

    # Check if the row has enough elements to perform a shift
    if first_row.size < 2:
        # If only 0 or 1 element, the shift has no effect
        return np.copy(input_grid) # Return a copy of the original grid

    # Perform the circular left shift on the first row
    # np.roll(array, shift) shifts elements. A shift of -1 moves elements left.
    transformed_row = np.roll(first_row, -1)

    # Create the output grid
    # We need to ensure the output has the same dimensions as the input
    # If the input was guaranteed to be 1xN, we could just reshape
    # A safer approach is to copy the input and replace the first row
    output_grid = np.copy(input_grid)
    output_grid[0] = transformed_row

    return output_grid
"""
Transforms an input grid of shape (1, 12) containing digits by counting the 
non-zero elements in the row and setting the corresponding number of leading 
elements in the output grid's row to 1, with the rest being 0.
"""

import numpy as np

# Helper function (though np.count_nonzero is used directly below for simplicity)
# def count_non_zeros_in_row(row):
#   """Counts the number of non-zero elements in a 1D NumPy array (row)."""
#   return np.count_nonzero(row)

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A NumPy array of shape (1, 12) containing integers 0-9.

    Returns:
        A NumPy array of shape (1, 12) representing the transformed grid.
    """
    # Ensure the input has the expected shape (optional but good practice)
    if input_grid.shape != (1, 12):
        raise ValueError(f"Input grid must have shape (1, 12), but got {input_grid.shape}")

    # Extract the first (and only) row from the input grid
    input_row = input_grid[0]

    # Count the number of non-zero elements in the input row
    non_zero_count = np.count_nonzero(input_row)

    # Initialize the output_grid with zeros, matching the input grid's shape and type
    output_grid = np.zeros_like(input_grid)

    # Access the first (and only) row of the output grid
    # Set the first 'non_zero_count' elements of this row to 1 using slicing
    # This works correctly even if non_zero_count is 0 (empty slice)
    output_grid[0, :non_zero_count] = 1

    # The remaining elements are already initialized to 0

    return output_grid
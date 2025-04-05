"""
Transforms an input grid (1x12 NumPy array) by performing a circular right shift 
on the elements within its single row. The last element moves to the first 
position, and all other elements shift one position to the right.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a circular right shift along the columns of a 1x12 NumPy array.

    Args:
        input_grid (np.ndarray): A 2D NumPy array with shape (1, 12).

    Returns:
        np.ndarray: A new 2D NumPy array of shape (1, 12) with elements 
                    circularly shifted one position to the right along axis 1.
                    Returns the input grid unmodified if it's empty or not 2D.
    """
    # 1. Receive the input grid (assumed shape (1, 12)).
    # Basic validation: Check if it's a NumPy array and 2D.
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2:
        # Or raise an error depending on expected behavior for invalid input
        print(f"Warning: Input grid is not a 2D NumPy array. Received shape: {getattr(input_grid, 'shape', 'N/A')}")
        return input_grid # Return unmodified

    # Handle empty array case
    if input_grid.size == 0:
        return np.array([[]]) # Return an empty grid of correct dimensions

    # 2. Perform the circular right shift along the second axis (axis=1, columns).
    # A shift value of 1 moves elements one position to the right along that axis,
    # wrapping the last element to the first position within the row.
    output_grid = np.roll(input_grid, shift=1, axis=1)

    # 3. Return the resulting grid.
    return output_grid

"""
Transforms an input sequence (NumPy array) of 12 digits based on the count of non-zero digits.

The transformation rule is as follows:
1. Count the number of non-zero elements in the input array (let the count be N).
2. Create an output array of 12 integers, initialized to zeros.
3. The first N elements of the output array are set to 1.
4. The remaining (12 - N) elements remain 0.
"""

import numpy as np

# Helper function to count non-zero elements
def count_non_zeros_np(arr):
  """Counts the number of non-zero elements in a NumPy array."""
  return np.count_nonzero(arr)

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A NumPy array of shape (12,) containing integers.

    Returns:
        A NumPy array of shape (12,) representing the transformed sequence.
    """
    # Ensure input is a numpy array (optional, depends on execution environment)
    if not isinstance(input_grid, np.ndarray):
        # Handle potential non-array input if necessary, or raise error
        # For this problem context, assume input is already correct type
        pass 

    # Check expected shape (optional but good practice)
    if input_grid.shape != (12,):
         raise ValueError(f"Input grid must have shape (12,), but got {input_grid.shape}")

    # Count the number of non-zero elements in the input array
    non_zero_count = count_non_zeros_np(input_grid)

    # Initialize the output array with 12 zeros
    # Use the same dtype as input or specify int if needed
    output_grid = np.zeros(12, dtype=input_grid.dtype) 

    # Set the first 'non_zero_count' elements to 1
    # Slicing handles the case where non_zero_count is 0 correctly (empty slice)
    output_grid[:non_zero_count] = 1

    # Return the resulting output array
    return output_grid
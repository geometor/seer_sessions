```python
import numpy as np
import math # Not needed for this specific logic, but potentially useful for other tasks
import collections # Not needed for this specific logic, but potentially useful for other tasks

"""
Transforms a grid (NumPy array) of single-digit integers.
The transformation treats the grid as a 1D sequence (flattening if necessary).
It identifies the contiguous sub-sequence bounded by the first and last non-zero digits (inclusive).
This sub-sequence is then reversed in place.
Any leading and trailing zeros (relative to the 1D sequence) remain in their original positions.
If the sequence contains only zeros, it remains unchanged.
The final output grid is reshaped to match the original input grid's dimensions.
"""

def _find_first_non_zero_index(sequence_1d):
  """Finds the index of the first non-zero element in a 1D NumPy array."""
  # np.nonzero returns a tuple of arrays, one for each dimension.
  # For a 1D array, it returns a tuple with one array containing the indices.
  non_zero_indices = np.nonzero(sequence_1d)[0]
  if len(non_zero_indices) == 0:
    return -1 # Indicates no non-zero element found
  return non_zero_indices[0] # Return the first index

def _find_last_non_zero_index(sequence_1d):
  """Finds the index of the last non-zero element in a 1D NumPy array."""
  non_zero_indices = np.nonzero(sequence_1d)[0]
  if len(non_zero_indices) == 0:
    return -1 # Indicates no non-zero element found
  return non_zero_indices[-1] # Return the last index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described transformation to the input NumPy array.

    Args:
        input_grid: A NumPy array (potentially multi-dimensional) containing single-digit integers.

    Returns:
        A NumPy array containing the transformed sequence, reshaped to the original input dimensions.
    """
    # 1. Store the original shape of the input grid.
    original_shape = input_grid.shape

    # 2. Flatten the input grid into a 1D sequence for processing.
    # Using .ravel() is often slightly more efficient than .flatten() if a copy isn't strictly needed internally,
    # but flatten guarantees a copy, which can be safer depending on subsequent operations.
    # For this logic, either works fine. Let's use flatten for clarity of making a distinct 1D version.
    sequence_1d = input_grid.flatten()

    # 3. Find the index of the first non-zero digit in the 1D sequence.
    start_index = _find_first_non_zero_index(sequence_1d)

    # 4. Handle the case where the input contains only zeros.
    if start_index == -1:
      # If no non-zero element found, return the original grid unchanged (but ensure it's a copy).
      # Reshaping a copy of the flattened sequence handles this uniformly.
      output_grid = np.copy(sequence_1d).reshape(original_shape)
      return output_grid

    # 5. Find the index of the last non-zero digit in the 1D sequence.
    # We know at least one non-zero exists if start_index != -1.
    end_index = _find_last_non_zero_index(sequence_1d)

    # 6. Extract the three parts from the 1D sequence using slicing.
    # a. Leading part (before the first non-zero)
    leading_part = sequence_1d[:start_index]
    # b. Middle part (from first non-zero to last non-zero, inclusive)
    middle_part = sequence_1d[start_index : end_index + 1]
    # c. Trailing part (after the last non-zero)
    trailing_part = sequence_1d[end_index + 1:]

    # 7. Reverse the order of the elements within the middle part.
    reversed_middle_part = middle_part[::-1] # Efficient slicing for reversal

    # 8. Construct the transformed 1D sequence by concatenating the parts.
    # np.concatenate requires a tuple or list of arrays. Ensure parts are arrays.
    output_sequence_1d = np.concatenate((leading_part, reversed_middle_part, trailing_part))

    # 9. Reshape the transformed 1D sequence back into the original shape.
    output_grid = output_sequence_1d.reshape(original_shape)

    # 10. Return the reshaped grid.
    return output_grid
```
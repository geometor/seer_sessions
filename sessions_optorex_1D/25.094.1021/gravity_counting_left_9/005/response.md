```python
import numpy as np

"""
Transforms an input NumPy array of 12 integers (0-9) into an output NumPy array of 12 binary integers (0 or 1).
The transformation rule is as follows:
1. Count the number of 0 values in the input array. Let this be N.
2. The number of non-zero values (1-9) in the input array will be M = 12 - N.
3. The output array consists of N zero integers followed by M one integers.
"""

def count_zeros_in_array(arr: np.ndarray) -> int:
  """Counts the number of zero elements in a NumPy array."""
  # Use numpy's vectorized comparison and sum
  return (arr == 0).sum()

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A NumPy array of shape (12,) containing integers from 0 to 9.

    Returns:
        A NumPy array of shape (12,) containing N zeros followed by M ones,
        where N is the count of zeros and M is the count of non-zeros in the input.
    """
    # Ensure input is a NumPy array and has the expected size
    if not isinstance(input_grid, np.ndarray):
        raise TypeError("Input must be a NumPy array.")
    if input_grid.size != 12:
         raise ValueError(f"Input array must have size 12, but got {input_grid.size}")

    # Count the number of zeros in the input array
    zero_count = count_zeros_in_array(input_grid)

    # Calculate the number of non-zeros (total elements - zero count)
    total_elements = input_grid.size # Should be 12
    non_zero_count = total_elements - zero_count

    # Construct the output array using numpy operations
    # Create an array of N zeros
    output_zeros = np.zeros(zero_count, dtype=int)
    # Create an array of M ones
    output_ones = np.ones(non_zero_count, dtype=int)
    # Concatenate the two arrays to form the final output grid
    output_grid = np.concatenate((output_zeros, output_ones))

    # Reshape to ensure it's a 1D array of size 12, although concatenate should handle this
    # This step might be redundant if concatenate always produces the correct shape,
    # but added for robustness.
    output_grid = output_grid.reshape(12) 

    return output_grid
```
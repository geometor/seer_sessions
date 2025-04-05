```python
import numpy as np
import collections

"""
Transforms an input NumPy array of 12 integers (0, 1, or 2) by rearranging 
them such that all '2's appear first, followed by the necessary number of '0's
to maintain a total length of 12, and finally all '1's appear last. 
The counts of '1's and '2's from the input array are preserved in the output array.
"""

def count_elements(arr, element):
  """Helper function to count occurrences of a specific element in a NumPy array."""
  return np.count_nonzero(arr == element)

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A NumPy array of 12 integers (0, 1, or 2).

    Returns:
        A NumPy array of 12 integers representing the transformed sequence.
    """
    
    total_length = 12 # The required length of the sequence

    # Count the occurrences of '2' and '1' in the input array
    num_twos = count_elements(input_grid, 2)
    num_ones = count_elements(input_grid, 1)

    # Calculate the number of '0's needed for the output array
    # The total length must be maintained
    num_zeros = total_length - num_twos - num_ones
    
    # Ensure num_zeros is not negative (though unlikely given problem constraints)
    num_zeros = max(0, num_zeros) 

    # Construct the components of the output array
    twos_part = np.full(num_twos, 2, dtype=int)
    zeros_part = np.full(num_zeros, 0, dtype=int)
    ones_part = np.full(num_ones, 1, dtype=int)

    # Concatenate the parts to form the final output array
    output_grid = np.concatenate((twos_part, zeros_part, ones_part))

    return output_grid
```
```python
"""
Transforms an input sequence of integers (0, 1, 2), represented as a 1D NumPy array, 
by reordering its elements. The output sequence places all '2's first, followed 
by all '0's, and finally all '1's, while preserving the original counts of each integer.
"""

import numpy as np

def count_occurrences(array, value):
  """Counts the number of times a specific value appears in a NumPy array."""
  return np.count_nonzero(array == value)
  # Alternative: return np.sum(array == value)

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Reorders the integers in the input NumPy array according to the rule: 2s, then 0s, then 1s.

    Args:
        input_sequence: A 1D NumPy array containing integers (0, 1, 2).

    Returns:
        A 1D NumPy array containing the reordered integers.
    """

    # Count the occurrences of each relevant integer (2, 0, 1) in the input array
    count_2 = count_occurrences(input_sequence, 2)
    count_0 = count_occurrences(input_sequence, 0)
    count_1 = count_occurrences(input_sequence, 1)

    # Create arrays for each group of integers based on their counts
    twos = np.full(count_2, 2, dtype=int)
    zeros = np.full(count_0, 0, dtype=int)
    ones = np.full(count_1, 1, dtype=int)

    # Concatenate the arrays in the desired order (2s, then 0s, then 1s)
    output_sequence = np.concatenate((twos, zeros, ones))

    # Ensure the output array has the correct integer data type
    # (np.concatenate should handle this, but explicit casting is safe)
    output_sequence = output_sequence.astype(int)

    return output_sequence

```
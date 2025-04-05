"""
Sorts the elements of the input NumPy array based on the custom priority order 2 > 0 > 1.
The input is assumed to be a 1D NumPy array of length 12 containing only the digits 0, 1, and 2.
The output is a NumPy array of the same shape and dtype, with elements sorted according to the rule: all 2s first, then all 0s, then all 1s.
"""

import numpy as np
import collections

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Sorts the input NumPy array based on the custom order: 2 comes first, then 0, then 1.

    Args:
        input_grid: A 1D NumPy array of integers (0, 1, or 2).

    Returns:
        A 1D NumPy array with the elements sorted according to the custom order (2, 0, 1).
    """

    # Ensure the input is a NumPy array (although the type hint suggests it is)
    if not isinstance(input_grid, np.ndarray):
      # If it's a list or other iterable, convert it
      input_sequence = np.array(input_grid)
    else:
      input_sequence = input_grid # Use the input directly

    # Count the occurrences of each digit (0, 1, 2) using collections.Counter for simplicity
    # Alternatively, use np.count_nonzero(input_sequence == digit) for each digit
    counts = collections.Counter(input_sequence)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)
    count_2 = counts.get(2, 0)

    # Initialize an empty list to build the output sequence
    output_sequence_list = []

    # Append '2's to the output list based on their count
    output_sequence_list.extend([2] * count_2)

    # Append '0's to the output list based on their count
    output_sequence_list.extend([0] * count_0)

    # Append '1's to the output list based on their count
    output_sequence_list.extend([1] * count_1)

    # Convert the resulting list into a NumPy array with the same dtype as input if possible
    output_grid = np.array(output_sequence_list, dtype=input_sequence.dtype)

    return output_grid
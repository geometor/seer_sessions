"""
Accepts a NumPy array containing the digits 0, 1, and 2.
Rearranges the digits based on the priority order: 2s first, then 0s, then 1s.
Outputs the newly constructed and sorted NumPy array.
"""

import numpy as np
import collections

def count_digits(input_array: np.ndarray) -> collections.Counter:
    """Counts the occurrences of each digit in the input NumPy array."""
    return collections.Counter(input_array)

def construct_sorted_array(counts: collections.Counter) -> np.ndarray:
    """Constructs a sorted NumPy array based on digit counts and priority (2 > 0 > 1)."""
    count_2 = counts.get(2, 0)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)

    # Create arrays for each digit based on their counts
    twos = np.full(count_2, 2, dtype=int)
    zeros = np.full(count_0, 0, dtype=int)
    ones = np.full(count_1, 1, dtype=int)

    # Concatenate arrays in the desired order: 2s, then 0s, then 1s
    output_array = np.concatenate((twos, zeros, ones))
    return output_array

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Sorts the digits in the input NumPy array based on the priority 2 > 0 > 1.

    Args:
        input_grid: A NumPy array containing digits (0, 1, 2).

    Returns:
        A NumPy array with digits sorted according to the rule.
    """

    # Count the occurrences of each digit (0, 1, 2) in the input array
    digit_counts = count_digits(input_grid)

    # Construct the output array based on the counts and the sorting priority (2 > 0 > 1)
    output_grid = construct_sorted_array(digit_counts)

    # Ensure the output has the same dtype as input if necessary, though concatenation defaults should work
    output_grid = output_grid.astype(input_grid.dtype)

    return output_grid
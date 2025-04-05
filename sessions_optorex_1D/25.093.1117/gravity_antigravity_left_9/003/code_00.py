"""
Rearrange the elements of an input 1D NumPy array such that all '2's appear first, followed by all '0's, and finally all '1's. The counts of each number (0, 1, 2) remain the same between input and output.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms a 1D input NumPy array of numbers (0, 1, 2) by rearranging them
    according to the specific order: 2s first, then 0s, then 1s.

    Args:
        input_grid: A 1D NumPy array of integers (expected to contain 0, 1, and 2).

    Returns:
        A new 1D NumPy array of integers rearranged according to the rule.
    """

    # Count the occurrences of each number (2, 0, 1) in the input array
    # using NumPy's boolean comparison and sum.
    count_2 = np.sum(input_grid == 2)
    count_0 = np.sum(input_grid == 0)
    count_1 = np.sum(input_grid == 1)

    # Create arrays filled with the respective numbers based on their counts.
    # Using np.full is efficient for creating arrays with a constant value.
    twos_array = np.full(count_2, 2, dtype=input_grid.dtype)
    zeros_array = np.full(count_0, 0, dtype=input_grid.dtype)
    ones_array = np.full(count_1, 1, dtype=input_grid.dtype)

    # Concatenate the arrays in the desired order (2s, then 0s, then 1s).
    output_grid = np.concatenate((twos_array, zeros_array, ones_array))

    # Return the newly constructed and rearranged array.
    return output_grid
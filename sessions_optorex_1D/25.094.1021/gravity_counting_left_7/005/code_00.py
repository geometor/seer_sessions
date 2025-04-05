import numpy as np

"""
Transform an input sequence (represented as a NumPy array) of single-digit integers 
into a binary sequence (NumPy array) of the same total number of elements.
The output sequence consists of a block of zeros followed by a block of ones.
The number of zeros in the output sequence is equal to the total count of 
the integer 0 in the input sequence (considering all elements if multi-dimensional).
The remaining positions in the output sequence are filled with ones.
"""


def count_zeros_np(grid: np.ndarray) -> int:
    """
    Counts the total occurrences of the integer 0 in a NumPy array.

    Args:
        grid: The input NumPy array.

    Returns:
        The total count of zeros in the array.
    """
    return np.count_nonzero(grid == 0)

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms an input NumPy array of digits into a binary NumPy array based
    on the count of zeros.

    Args:
        input_grid: A NumPy array of single-digit integers.

    Returns:
        A NumPy array of binary digits (0 or 1) with the same total number
        of elements as the input_grid.
    """
    # Determine the total number of elements in the input grid
    total_length = input_grid.size

    # Count the total number of zeros in the input grid
    zero_count = count_zeros_np(input_grid)

    # Calculate the number of ones needed
    one_count = total_length - zero_count

    # Create an array of zeros
    zeros_part = np.zeros(zero_count, dtype=int)

    # Create an array of ones
    ones_part = np.ones(one_count, dtype=int)

    # Concatenate the zeros and ones parts to form the output grid
    # The output will always be a 1D array matching the total element count.
    output_grid = np.concatenate((zeros_part, ones_part))

    return output_grid

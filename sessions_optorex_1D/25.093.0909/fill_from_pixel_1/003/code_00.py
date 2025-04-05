import numpy as np

"""
Identifies the first and last non-zero digits in a sequence (list or NumPy array) of 12 digits.
Counts the number of leading zeros (before the first non-zero) and trailing zeros (after the last non-zero).
If the count of leading zeros is less than or equal to the count of trailing zeros, replace the leading zeros with the value of the first non-zero digit.
Otherwise, replace the trailing zeros with the value of the last non-zero digit.
If the sequence contains only zeros, return it unchanged.
"""

def find_first_non_zero(seq):
    """
    Finds the value and index of the first non-zero element in a sequence.

    Args:
        seq: A list or NumPy array of numbers.

    Returns:
        A tuple (value, index) of the first non-zero element.
        Returns (None, -1) if all elements are zero or the sequence is empty.
    """
    for i, val in enumerate(seq):
        if val != 0:
            return val, i
    return None, -1 # Return None and -1 if all zeros or empty

def find_last_non_zero(seq):
    """
    Finds the value and index of the last non-zero element in a sequence.

    Args:
        seq: A list or NumPy array of numbers.

    Returns:
        A tuple (value, index) of the last non-zero element.
        Returns (None, -1) if all elements are zero or the sequence is empty.
    """
    last_val = None
    last_idx = -1
    for i, val in enumerate(seq):
        if val != 0:
            last_val = val
            last_idx = i
    return last_val, last_idx

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_grid: A NumPy array representing the sequence of 12 digits.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Determine the length of the sequence
    n = len(input_grid)
    if n == 0:
        return input_grid # Handle empty input

    # Find the first non-zero digit and its index
    first_val, first_idx = find_first_non_zero(input_grid)

    # Handle the case where the input is all zeros
    if first_val is None:
        return input_grid # Return unchanged if all zeros

    # Find the last non-zero digit and its index
    # (We know there's at least one non-zero element if first_val is not None)
    last_val, last_idx = find_last_non_zero(input_grid)

    # Calculate the number of leading zeros
    num_left_zeros = first_idx

    # Calculate the number of trailing zeros
    # Ensure n-1 calculation is correct for indexing
    num_right_zeros = (n - 1) - last_idx

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Compare the number of leading and trailing zeros
    if num_left_zeros <= num_right_zeros:
        # Fill leading zeros with the first non-zero value
        # Loop from index 0 up to (but not including) first_idx
        for i in range(first_idx):
            output_grid[i] = first_val
    else:
        # Fill trailing zeros with the last non-zero value
        # Loop from index last_idx + 1 up to (but not including) n
        for i in range(last_idx + 1, n):
            output_grid[i] = last_val

    # Return the modified grid
    return output_grid
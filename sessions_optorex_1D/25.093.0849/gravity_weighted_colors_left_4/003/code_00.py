"""
Transforms an input sequence (list or array) of digits (0, 1, 2) by sorting the digits numerically in non-decreasing (ascending) order and returning the sorted digits as a space-separated string.
"""

import numpy as np # Import numpy as the error message indicated its use

def transform(input_data) -> str:
    """
    Sorts the digits in an input sequence and formats them as a space-separated string.

    Args:
        input_data: A list or NumPy array containing digits (0, 1, 2).

    Returns:
        A string containing the same digits as the input, sorted numerically
        in non-decreasing order and separated by spaces.
    """
    # 1. Ensure input is in a sortable format (list or numpy array).
    #    If it's a numpy array, sorting works directly. If it's a list, sorting works too.
    #    Let's convert to a numpy array for consistency if it's not already one,
    #    or simply work with the input if it's already array-like.
    #    Actually, Python's built-in sort() or sorted() works on lists, and np.sort() on arrays.
    #    Let's use sorted() for generality, as it returns a new sorted list.
    # Example input (assuming train_1): [0, 1, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0] or np.array([0, 1, ...])

    # 2. Sort the elements numerically in non-decreasing order.
    # Example: [0, 1, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0] -> [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2]
    sorted_digits = sorted(input_data)

    # 3. Convert each sorted number to its string representation.
    # Example: [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2] -> ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2']
    sorted_digits_str = [str(digit) for digit in sorted_digits]

    # 4. Join the string representations into a single string with space separators.
    # Example: ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2'] -> "0 0 0 0 0 0 0 0 1 2 2 2"
    output_str = ' '.join(sorted_digits_str)

    # 5. Return the resulting string.
    return output_str
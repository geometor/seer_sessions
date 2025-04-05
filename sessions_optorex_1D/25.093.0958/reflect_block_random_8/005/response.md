```python
import numpy as np
# No other specific math/science libraries are needed for this list manipulation task.

"""
Reverses the subsequence of digits located between the first and last non-zero digits (inclusive) in the input sequence. Leading and trailing zeros remain in their original positions. If no non-zero digits or only one non-zero digit exists, the sequence remains unchanged.
"""

def find_first_non_zero_index(digit_list):
    """
    Finds the index of the first non-zero digit in a list.

    Args:
        digit_list: A list of integers.

    Returns:
        The index of the first non-zero digit, or -1 if none are found.
    """
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    return -1 # Return -1 if no non-zero digit is found

def find_last_non_zero_index(digit_list):
    """
    Finds the index of the last non-zero digit in a list.

    Args:
        digit_list: A list of integers.

    Returns:
        The index of the last non-zero digit, or -1 if none are found.
    """
    last_index = -1
    # Iterate through the list and update last_index whenever a non-zero is found
    for i, digit in enumerate(digit_list):
        if digit != 0:
            last_index = i
    return last_index # Will return -1 if no non-zero digit is found

def transform(input_list):
    """
    Applies the subsequence reversal transformation based on non-zero boundaries.

    Args:
        input_list: A list (or numpy array) of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a standard Python list for consistent slicing/indexing
    # Handles potential numpy array input from a testing environment
    if isinstance(input_list, np.ndarray):
        input_digits = input_list.tolist()
    else:
        # Assume it's already list-like (e.g., a list)
        input_digits = list(input_list) # Make a copy to avoid modifying original if mutable

    # Find the index of the first non-zero digit.
    first_nz_index = find_first_non_zero_index(input_digits)

    # Find the index of the last non-zero digit.
    # This is only strictly necessary if a first non-zero digit was found,
    # but calling it anyway is safe and simplifies the edge case check.
    last_nz_index = find_last_non_zero_index(input_digits)

    # Handle edge cases:
    # 1. No non-zero digits (first_nz_index == -1)
    # 2. Only one non-zero digit (first_nz_index == last_nz_index)
    # In both these scenarios, the list remains unchanged.
    if first_nz_index == -1 or first_nz_index == last_nz_index:
        # Return the original (copied) list
        return input_digits

    # If we reach here, there are at least two non-zero digits,
    # and first_nz_index and last_nz_index define the boundaries.

    # Extract the prefix: elements before the first non-zero index.
    prefix = input_digits[:first_nz_index]

    # Extract the middle subsequence: elements from the first to the last
    # non-zero index (inclusive).
    middle = input_digits[first_nz_index : last_nz_index + 1]

    # Extract the suffix: elements after the last non-zero index.
    suffix = input_digits[last_nz_index + 1:]

    # Reverse the order of the digits within the middle subsequence.
    # Slicing with [::-1] creates a reversed copy of the list.
    reversed_middle = middle[::-1]

    # Construct the final output sequence by concatenating the parts.
    output_digits = prefix + reversed_middle + suffix

    # Return the constructed output sequence.
    return output_digits
```
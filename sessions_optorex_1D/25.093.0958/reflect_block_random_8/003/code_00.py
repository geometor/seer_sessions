import numpy as np
import math # Although math is imported, it's not used in this specific transformation

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
    for i, digit in enumerate(digit_list):
        if digit != 0:
            last_index = i
    return last_index # Will return -1 if no non-zero digit is found

def transform(input_list):
    """
    Applies the subsequence reversal transformation.

    Args:
        input_list: A list (or numpy array) of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a standard Python list for consistent slicing/indexing
    if isinstance(input_list, np.ndarray):
        input_digits = input_list.tolist()
    else:
        # Assume it's already list-like (e.g., a list)
        input_digits = list(input_list)

    # 2. Find the index of the first non-zero digit.
    first_nz_index = find_first_non_zero_index(input_digits)

    # 3. Find the index of the last non-zero digit.
    #    (Only needed if a first non-zero digit was found)
    if first_nz_index != -1:
        last_nz_index = find_last_non_zero_index(input_digits)
    else:
        last_nz_index = -1 # Ensures the edge case below is handled correctly

    # 4. Handle edge cases:
    #    - No non-zero digits (first_nz_index == -1)
    #    - Only one non-zero digit (first_nz_index == last_nz_index)
    #    In both cases, the list remains unchanged.
    if first_nz_index == -1 or first_nz_index == last_nz_index:
        return input_digits # Return the original list

    # 5. Identify the prefix: elements before the first non-zero index.
    prefix = input_digits[:first_nz_index]

    # 6. Identify the middle subsequence: elements from the first to the last
    #    non-zero index (inclusive).
    middle = input_digits[first_nz_index : last_nz_index + 1]

    # 7. Identify the suffix: elements after the last non-zero index.
    suffix = input_digits[last_nz_index + 1:]

    # 8. Reverse the order of the digits within the middle subsequence.
    reversed_middle = middle[::-1] # Pythonic way to reverse a list

    # 9. Construct the output sequence by concatenating the parts.
    output_digits = prefix + reversed_middle + suffix

    # 10. Return the constructed output sequence.
    return output_digits
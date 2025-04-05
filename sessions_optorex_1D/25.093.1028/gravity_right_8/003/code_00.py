import numpy as np
import collections  # Although not used in the final code, kept for potential future use if needed

"""
Rearranges digits in an input NumPy array of strings, placing all '0' strings at the beginning 
while preserving the relative order of non-zero digit strings. The output is a single 
space-separated string.
"""

def transform(input_array: np.ndarray) -> str:
    """
    Transforms a 1D NumPy array of digit strings by moving all '0's to the front,
    maintaining the relative order of other digits, and returning a space-separated string.

    Args:
        input_array: A 1-dimensional NumPy array containing string representations of digits.

    Returns:
        A string with digits rearranged according to the rule (zeros first, others follow in order).
    """

    # 1. Initialize lists to store zero and non-zero digit strings.
    zeros = []
    non_zeros = []

    # 2. Iterate through the input NumPy array.
    for digit_str in input_array:
        # 3. Check if the current element is '0'.
        if digit_str == '0':
            # 4. Append '0' strings to the zeros list.
            zeros.append(digit_str)
        else:
            # 5. Append non-zero strings to the non_zeros list.
            non_zeros.append(digit_str)

    # 6. Concatenate the list of zeros followed by the list of non-zeros.
    rearranged_digits = zeros + non_zeros

    # 7. Join the elements of the rearranged list with spaces.
    output_str = ' '.join(rearranged_digits)

    # 8. Return the final space-separated string.
    return output_str
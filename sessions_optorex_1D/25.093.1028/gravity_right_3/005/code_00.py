import numpy as np # numpy is available for array operations
import math # math is available
import collections # collections is available
import re # regular expressions is available

"""
Reorders the elements of an input integer NumPy array such that all zeros 
precede non-zeros, preserving the relative order of the non-zero elements, 
and formats the result as a space-separated string.
"""

def transform(input_arr: np.ndarray) -> str:
    """
    Transforms a NumPy array of integers by moving all zeros to the beginning 
    while maintaining the relative order of non-zero elements, and returns 
    the result as a space-separated string.

    Args:
        input_arr: A NumPy array containing integers (potentially multi-dimensional).

    Returns:
        A string containing the reordered space-separated integers.
    """

    # 1. Flatten the input NumPy array into a 1D sequence.
    # This handles potential multi-dimensional inputs consistently.
    flattened_sequence = input_arr.flatten()

    # 2. Create two new empty lists to store zero and non-zero elements.
    zeros_list = []
    non_zeros_list = []

    # 3. Iterate through each element in the flattened sequence.
    for element in flattened_sequence:
        # 4. Check if the element is zero.
        if element == 0:
            # If it is 0, append it to the zeros_list.
            zeros_list.append(element)
        else:
            # If it is not 0, append it to the non_zeros_list.
            # This preserves the relative order of non-zero elements from the flattened sequence.
            non_zeros_list.append(element)

    # 5. Concatenate the lists: zeros first, then non-zeros.
    # This creates the final ordered sequence of numbers.
    ordered_list = zeros_list + non_zeros_list

    # 6. Convert each integer in the ordered list to its string representation.
    # We use a list comprehension for conciseness.
    string_list = [str(num) for num in ordered_list]

    # 7. Join the string representations with a single space.
    # This formats the output according to the required specification.
    output_str = " ".join(string_list)

    # 8. Return the resulting space-separated string.
    return output_str
import math
import numpy as np
# from skimage import measure # example - can uncomment if needed

"""
Transforms a 1D NumPy array of integers (0, 1, 2) by sorting its elements in descending numerical order (2 > 1 > 0) and then formatting the sorted sequence into a space-separated string.
"""

def transform(input_array: np.ndarray) -> str:
    """
    Sorts a 1D NumPy array of integers (0, 1, 2) in descending order and
    returns the result as a space-separated string.

    Args:
        input_array: A 1D NumPy array containing integers (0, 1, or 2).

    Returns:
        A string containing the sorted integers, separated by spaces.
    """

    # 1. Sort the elements of the NumPy array in descending numerical order.
    #    np.sort sorts in ascending order by default.
    #    We can reverse the sorted array using slicing [::-1].
    sorted_digits_asc = np.sort(input_array)
    sorted_digits_desc = sorted_digits_asc[::-1]

    # 2. Convert each integer in the sorted array to its string representation.
    #    A list comprehension is suitable for this conversion.
    sorted_digit_strings = [str(digit) for digit in sorted_digits_desc]

    # 3. Join these string representations together, separated by single spaces.
    #    The ' '.join() method concatenates the strings in the list with a space.
    output_str = ' '.join(sorted_digit_strings)

    # 4. Output the resulting space-separated string.
    return output_str

import math
import numpy as np
# from skimage import measure # example - can uncomment if needed

"""
Receives a 1D NumPy array of integers (0, 1, 2), sorts these integers in descending numerical order (2 > 1 > 0), and formats the sorted sequence into a space-separated string.
"""

def transform(input_array: np.ndarray) -> str:
    """
    Transforms a 1D NumPy array of integers by sorting them in descending order
    and formatting the result as a space-separated string.

    Args:
        input_array: A 1D NumPy array containing integers (0, 1, or 2).

    Returns:
        A string containing the same integers sorted in descending order,
        separated by spaces.
    """

    # 1. Sort the elements of the NumPy array in descending numerical order.
    # Use np.sort to get an ascending sort, then reverse it.
    # Alternatively, convert to list and sort in place:
    # digits = input_array.tolist()
    # digits.sort(reverse=True)
    # sorted_digits = np.array(digits) # if needed as array, but list is fine here

    # Using np.sort and slicing for reversal is efficient for numpy arrays
    sorted_digits_asc = np.sort(input_array)
    sorted_digits_desc = sorted_digits_asc[::-1] # Reverse the sorted array

    # 2. Convert each integer in the sorted array to its string representation.
    sorted_digit_strings = [str(d) for d in sorted_digits_desc]

    # 3. Join these string representations together, separated by single spaces.
    output_str = ' '.join(sorted_digit_strings)

    # 4. Output the resulting string.
    return output_str

"""
Transforms an input NumPy array of 12 digits by performing a circular left shift of 8 positions and returns the result as a space-separated string.
"""

import numpy as np

def transform(input_array: np.ndarray) -> str:
    """
    Applies a circular left shift of 8 positions to a 1D NumPy array of 12 digits.

    Args:
        input_array: A NumPy array of shape (12,) containing integers.

    Returns:
        A string representing the transformed sequence, with digits space-separated.
    """
    # 1. Ensure the input is a NumPy array (already guaranteed by type hint, but good practice).
    # input_array is expected to be a 1D numpy array like [6 6 6 6 6 0 0 0 0 0 6 6]

    # 2. Perform a circular left shift on the array by 8 positions.
    # np.roll provides an efficient way to do circular shifts (negative shift means left).
    shifted_array = np.roll(input_array, shift=-8)
    # Alternative using slicing and concatenation:
    # shift = 8
    # shifted_array = np.concatenate((input_array[shift:], input_array[:shift]))


    # 3. Convert the elements of the resulting NumPy array into strings.
    string_elements = [str(x) for x in shifted_array]

    # 4. Join these string elements with a single space separator.
    output_string = " ".join(string_elements)

    # 5. Return the formatted string.
    return output_string
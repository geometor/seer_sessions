"""
Sorts the elements of an input 1D NumPy array of integers in ascending numerical order and returns them as a space-separated string.
"""

import numpy as np

def transform(input_array: np.ndarray) -> str:
    """
    Takes a 1D NumPy array of integers, sorts them numerically
    in ascending order, and returns the sorted sequence as a
    space-separated string.

    Args:
        input_array: A 1D NumPy array containing integers (e.g., 0, 1, 2).

    Returns:
        A string containing the sorted integers, space-separated.
    """

    # Sort the input NumPy array in ascending order.
    # np.sort returns a new sorted array, leaving the original unchanged.
    sorted_array = np.sort(input_array)

    # Convert each integer in the sorted array to its string representation.
    # We can use a list comprehension for this.
    string_elements = [str(num) for num in sorted_array]

    # Join the list of string elements into a single string,
    # using a space (" ") as the separator between elements.
    output_str = " ".join(string_elements)

    # Return the final formatted string.
    return output_str

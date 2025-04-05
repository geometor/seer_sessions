import numpy as np

"""
Accept the input sequence of digits (as a 1D NumPy array), sort the elements of the array in descending numerical order (from 2 down to 0), and return the sorted NumPy array.
"""

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Sorts a 1D NumPy array of integers in descending order.

    Args:
        input_array: A 1D NumPy array containing integers (expected 0, 1, or 2).

    Returns:
        A new 1D NumPy array with the elements of the input array sorted
        in descending order.
    """

    # Use Python's built-in sorted() function which directly supports descending order.
    # This function works on iterables like NumPy arrays and returns a list.
    # Example: [2, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 2] -> [2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    sorted_list = sorted(input_array, reverse=True)

    # Convert the sorted list back into a NumPy array.
    output_array = np.array(sorted_list, dtype=input_array.dtype)

    # Return the resulting sorted array.
    return output_array
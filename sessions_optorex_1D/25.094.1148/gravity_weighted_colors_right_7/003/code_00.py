import numpy as np

"""
Accept the input NumPy array of digits, sort the elements of the array in descending numerical order (from 2 down to 0), and return the sorted NumPy array.
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
    # Sort the input array in ascending order using np.sort
    # Example: [2, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 2] -> [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2] (Note: np.sort sorts in place)
    # Then reverse the sorted array using slicing [::-1] to get descending order
    # Example: [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2][::-1] -> [2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    output_array = np.sort(input_array)[::-1]

    # Return the resulting sorted array
    return output_array
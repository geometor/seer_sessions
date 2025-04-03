"""
Transforms an input NumPy array of integers by moving the first two elements 
to the end of the array, preserving the relative order of the remaining elements.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Moves the first two elements of the input NumPy array to the end.

    Args:
        input_array: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the first two elements moved to the end.
    """

    # Get the length of the input array
    n = len(input_array)

    # Handle edge cases where the array has fewer than 2 elements
    if n < 2:
        # If fewer than 2 elements, return the array unchanged as the operation is not fully applicable.
        return input_array.copy() # Return a copy to avoid modifying the original input

    # Extract the first element (at index 0)
    first_element = input_array[0]

    # Extract the second element (at index 1)
    second_element = input_array[1]

    # Extract the remaining elements (from index 2 onwards)
    remaining_elements = input_array[2:]

    # Construct the output array by concatenating the parts
    # Note: np.concatenate expects tuples of arrays. Single elements need to be put in arrays/lists.
    output_array = np.concatenate((remaining_elements, np.array([first_element]), np.array([second_element])))

    return output_array

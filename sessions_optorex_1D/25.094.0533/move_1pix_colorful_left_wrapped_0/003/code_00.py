import numpy as np

"""
Performs a cyclic left shift on a 1D NumPy array of integers. 
The first element of the input array is moved to the last position, 
and all other elements shift one position to the left.
"""

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Applies a cyclic left shift by one position to a 1D NumPy array.

    Args:
        input_array: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array representing the cyclically shifted input.
    """

    # Get the size of the input array
    n = input_array.size

    # Handle edge cases: empty or single-element array
    # If the array has 0 or 1 element, the shift doesn't change it.
    if n <= 1:
        return input_array.copy() # Return a copy to avoid modifying the original

    # Extract the first element. Need [0:1] to keep it as a 1-element array for concatenation.
    first_element = input_array[0:1]

    # Extract the remaining elements (from the second element onwards)
    remaining_elements = input_array[1:]

    # Concatenate the remaining elements with the first element appended at the end
    output_array = np.concatenate((remaining_elements, first_element))

    return output_array
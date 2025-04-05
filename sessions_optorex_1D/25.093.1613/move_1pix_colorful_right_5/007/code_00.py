"""
Shift a sequence of integers one position to the right, inserting a zero at the beginning and discarding the last element.
"""

import numpy as np

def transform(input_arr: np.ndarray) -> np.ndarray:
    """
    Transforms a 1D NumPy array by shifting elements one position to the right,
    inserting a 0 at the beginning, and discarding the last element.

    Args:
        input_arr: A 1-dimensional NumPy array of integers.

    Returns:
        A new 1-dimensional NumPy array with the transformation applied.
    """
    # Get the length of the input array
    n = len(input_arr)

    # Create a new output array of the same size and data type as the input, 
    # initialized with zeros. This handles setting the first element (index 0) to 0.
    output_arr = np.zeros_like(input_arr)

    # Check if the array has elements to avoid errors with empty arrays
    if n > 0:
        # Copy elements from the input array, starting from the first element (index 0) 
        # up to, but not including, the last element (index n-1), 
        # into the output array, starting from the second position (index 1).
        # Input slice: input_arr[0] through input_arr[n-2]
        # Output slice: output_arr[1] through output_arr[n-1]
        # The number of elements copied is n-1.
        output_arr[1:n] = input_arr[0:n-1] 
        # Note: Slicing input_arr[0:n-1] extracts elements at indices 0, 1, ..., n-2.
        # Slicing output_arr[1:n] assigns to indices 1, 2, ..., n-1.

    # Return the newly created and populated output array
    return output_arr

"""
Shift the elements of an integer NumPy array one position to the right, 
inserting a zero at the beginning and discarding the last element.
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
    
    # Create a new output array of the same size and data type, initialized with zeros.
    # This automatically handles setting the first element to 0.
    output_arr = np.zeros_like(input_arr)
    
    # Copy elements from the input array (excluding the last one)
    # into the output array, starting from the second position.
    # input_arr[0] goes to output_arr[1], input_arr[1] to output_arr[2], ..., input_arr[n-2] to output_arr[n-1]
    output_arr[1:n] = input_arr[0:n-1]
    
    return output_arr

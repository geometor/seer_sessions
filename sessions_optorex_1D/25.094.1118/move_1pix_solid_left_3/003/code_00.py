"""
Performs a left circular shift on a 1D NumPy array by one position, 
replacing the element shifted out from the end with a zero.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Shifts a 1D NumPy array one position to the left, discarding the first 
    element and appending a zero at the end.

    Args:
        input_array: A 1-dimensional NumPy array of integers.

    Returns:
        A new 1-dimensional NumPy array representing the transformed sequence.
    """
    
    # 1. Create a new array by slicing the input array, starting from the 
    #    element at index 1 and including all subsequent elements up to the end.
    #    This effectively removes the first element.
    shifted_array_partial = input_array[1:]
    
    # 2. Append a single integer element with the value 0 to the end of the 
    #    sliced array. np.append creates and returns a new array.
    output_array = np.append(shifted_array_partial, 0)
    
    # 3. Return the resulting array.
    return output_array

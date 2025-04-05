"""
Performs a left cyclic shift on a 1D NumPy array of digits. The first element 
is moved to the end of the array.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Applies a left cyclic shift to the input NumPy array.

    Args:
        input_array: A 1-dimensional NumPy array of integers.

    Returns:
        A new 1-dimensional NumPy array with the first element moved to the end.
    """
    # 1. Receive the input NumPy array. (Implicit in function argument)

    # 2. If the array has 1 or fewer elements, return it unchanged.
    if input_array.size <= 1:
        return input_array.copy() # Return a copy to avoid modifying the original if it's mutable

    # 3. Extract the first element (at index 0).
    first_element = input_array[0]

    # 4. Create a new array containing all elements from the second position (index 1) 
    #    to the end of the input array.
    remaining_elements = input_array[1:]

    # 5. Append the extracted first element to the end of this new array.
    #    np.concatenate requires tuples of arrays, so wrap the single element in a list or array.
    output_array = np.concatenate((remaining_elements, [first_element]))

    # 6. Return the resulting array.
    return output_array
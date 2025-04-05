"""
Performs a left cyclic shift by one position on a 1D NumPy array representing a sequence of digits. The first element is moved to the end of the array.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a left cyclic shift to the input 1D NumPy array.

    Args:
        input_grid: A 1-dimensional NumPy array of integers.

    Returns:
        A new 1-dimensional NumPy array with the first element moved to the end.
    """
    # 1. Receive the input sequence (NumPy array).

    # Handle edge cases where no shift is possible or needed.
    if input_grid.size <= 1:
        # Return a copy to maintain immutability if the input was mutable.
        return input_grid.copy() 

    # 2. Identify and temporarily store the digit located at the first position (index 0).
    first_element = input_grid[0]

    # 3. Create a new sequence containing all digits from the second position (index 1) 
    #    through the last position of the original input sequence.
    #    Slicing creates a view, but subsequent concatenation makes a new array.
    remaining_elements = input_grid[1:]

    # 4. Append the digit stored in step 2 to the end of the new sequence 
    #    created in step 3. We need to wrap the scalar `first_element` in a list 
    #    or array for concatenation.
    output_grid = np.concatenate((remaining_elements, [first_element]))

    # 5. Return the resulting sequence (array).
    return output_grid
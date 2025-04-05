"""
Transforms an input NumPy array by taking all elements except the last one, 
and inserting the integer '0' at the beginning of the array. 
The length of the output array remains the same as the input array.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid (np.ndarray): A 1D NumPy array of integers.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """
    
    # 1. Select all elements from the input array except the last one.
    # Slicing `[:-1]` achieves this.
    elements_to_keep = input_grid[:-1]
    
    # 2. Insert the integer 0 at the beginning (index 0) of the selected elements.
    # np.insert(array, index, value)
    output_grid = np.insert(elements_to_keep, 0, 0)
    
    # 3. Return the resulting array.
    return output_grid

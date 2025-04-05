```python
"""
Performs a cyclic left shift by 3 positions on the input 1-dimensional NumPy array. 
The first 3 elements are moved to the end of the array, and the remaining elements 
shift 3 positions to the left.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a cyclic left shift of 3 positions to the input NumPy array.

    Args:
        input_grid: A 1-dimensional NumPy array of integers.

    Returns:
        A new 1-dimensional NumPy array representing the input array after 
        a cyclic left shift by 3 positions.
    """
    
    # Define the amount to shift (left shift is negative for np.roll)
    shift_amount = -3 
    
    # Use numpy.roll to perform the cyclic shift efficiently
    # np.roll shifts elements along the specified axis (implicitly the first axis for 1D arrays)
    # A negative shift value shifts elements to the left.
    output_grid = np.roll(input_grid, shift_amount)

    # Return the resulting shifted array
    return output_grid

```
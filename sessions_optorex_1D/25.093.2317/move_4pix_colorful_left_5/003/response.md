```python
"""
Performs a cyclic left shift (rotation) on the input 1D NumPy array by 4 positions.
The first 4 elements are moved to the end of the array.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input 1D NumPy array 4 positions to the left.

    Args:
        input_grid: A 1D NumPy array of shape (12,) containing integers.

    Returns:
        A 1D NumPy array representing the rotated sequence.
    """
    # Define the amount by which to rotate left.
    shift_amount = 4

    # Perform the cyclic left shift using numpy.roll.
    # A negative shift value in np.roll indicates a left shift.
    output_grid = np.roll(input_grid, -shift_amount)

    # Alternatively, using slicing and concatenation:
    # elements_after_shift = input_grid[shift_amount:]
    # elements_before_shift = input_grid[:shift_amount]
    # output_grid = np.concatenate((elements_after_shift, elements_before_shift))

    return output_grid

```
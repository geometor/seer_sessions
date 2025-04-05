```python
"""
Applies a single left circular shift (rotation) to the input 1D NumPy array. 
It moves the first element to the end of the array, shifting all other 
elements one position to the left.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Performs a single left rotation on the input 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the input array after moving the first 
        element to the end.
    """

    # Use numpy.roll to perform a circular shift.
    # A shift of -1 moves elements to the left, wrapping the first element 
    # around to the last position. This directly implements the required
    # left rotation.
    output_grid = np.roll(input_grid, -1)

    # Return the rotated array
    return output_grid
```
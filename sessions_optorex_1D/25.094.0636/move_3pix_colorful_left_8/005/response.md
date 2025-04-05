```python
"""
Transforms an input sequence of 12 digits by performing a cyclic left shift by 3 positions. 
The first 3 digits are moved to the end of the sequence, and the remaining 9 digits are shifted to the beginning.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a cyclic left shift of 3 positions to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of shape (12,) containing integer digits.

    Returns:
        A 1D NumPy array of shape (12,) representing the sequence after 
        the cyclic left shift.
    """
    
    # Define the amount to shift cyclically to the left
    shift_amount = 3

    # Perform the cyclic left shift using numpy.roll
    # A negative shift value indicates a left shift.
    output_grid = np.roll(input_grid, -shift_amount)

    return output_grid
```
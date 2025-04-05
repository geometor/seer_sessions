```python
"""
Performs a cyclic left shift on a 1D NumPy input array of 12 digits by 3 positions.
The elements from index 3 onwards are moved to the beginning, followed by the 
elements from index 0 to 2.
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

    # Ensure the input is a NumPy array (though the type hint suggests it is)
    # If it's not, conversion might be needed depending on the actual runtime environment.
    # For this implementation, we assume it's already a NumPy array based on error analysis.
    
    # Perform the cyclic left shift using NumPy slicing and concatenation
    
    # Get the part of the array from the shift_amount index to the end
    shifted_part = input_grid[shift_amount:]
    
    # Get the part of the array from the beginning up to the shift_amount index
    wrapped_part = input_grid[:shift_amount]
    
    # Concatenate the shifted part followed by the wrapped part
    output_grid = np.concatenate((shifted_part, wrapped_part))

    return output_grid

```
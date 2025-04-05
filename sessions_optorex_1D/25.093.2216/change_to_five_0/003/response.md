```python
"""
Transforms a 1D NumPy array of digits by replacing each non-zero digit with 5 and leaving 0 digits unchanged.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1-dimensional NumPy array containing integers (0-9).

    Returns:
        A 1-dimensional NumPy array of the same shape where non-zero elements
        are replaced by 5 and zero elements remain 0.
    """
    # Ensure the input is treated as an integer array
    input_array = np.array(input_grid, dtype=int)

    # Create an output array of the same shape, initialized with zeros
    # This handles the case where input is 0, output should be 0
    output_grid = np.zeros_like(input_array, dtype=int)

    # Create a boolean mask for elements that are not equal to 0
    non_zero_mask = (input_array != 0)

    # Use the mask to set the corresponding elements in the output grid to 5
    output_grid[non_zero_mask] = 5

    # Return the transformed grid
    return output_grid

```
```python
import numpy as np

"""
Transforms a 1D NumPy array of integers based on the following element-wise rule:
- If an element is 0, it remains 0.
- If an element is 5, it remains 5.
- All other integer elements (1, 2, 3, 4, 6, 7, 8, 9) are changed to 5.
The function returns a new NumPy array of the same shape with the transformed elements.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies an element-wise transformation to a 1D NumPy array of integers.

    Args:
        input_grid: A 1D NumPy array containing integer digits.

    Returns:
        A new 1D NumPy array with transformed elements according to the rule:
        0 -> 0, 5 -> 5, others -> 5.
    """
    # Create a copy of the input array to modify. This ensures the original
    # input is not changed and the output has the correct shape and dtype.
    output_grid = np.copy(input_grid)

    # Create a boolean mask to identify elements that need to be changed to 5.
    # These are elements that are NOT equal to 0 AND NOT equal to 5.
    mask_to_change = (output_grid != 0) & (output_grid != 5)

    # Apply the transformation: set elements identified by the mask to 5.
    output_grid[mask_to_change] = 5

    # Return the modified array.
    return output_grid
```
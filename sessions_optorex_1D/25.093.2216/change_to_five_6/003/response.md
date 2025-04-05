```python
import numpy as np

"""
Transforms a 1D NumPy array of integers by replacing every non-zero integer 
with the integer 5, while keeping all 0 integers unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array containing integers (e.g., np.array([0, 0, 7, 8, 0, 3, 0, 0, 8, 1, 7, 0])).

    Returns:
        A new 1D NumPy array of the same shape with non-zero integers replaced by 5, preserving zeros.
    """
    
    # Create a copy of the input array to avoid modifying the original input.
    # This will serve as the basis for our output grid.
    output_grid = input_grid.copy()
    
    # Create a boolean mask. This mask will be True for elements in the input_grid
    # that are not equal to 0, and False for elements that are equal to 0.
    non_zero_mask = input_grid != 0
    
    # Use the boolean mask to selectively update elements in the output_grid.
    # Where the mask is True (i.e., the original element was not 0),
    # assign the value 5 to the corresponding element in the output_grid.
    # Elements where the mask is False (original element was 0) remain unchanged
    # because we started with a copy of the input_grid.
    output_grid[non_zero_mask] = 5
    
    # Return the modified array.
    return output_grid
```
```python
"""
Iterate through each element in the input NumPy array. If the element is 0, keep it as 0 in the output array. If the element is non-zero (1-9), replace it with 5 in the output array. The output array should have the same shape as the input array.
"""

import numpy as np
# No other specific math/science libraries are needed for this rule.

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms a NumPy array of digits according to the rule:
    0 maps to 0, non-zero digits map to 5.

    Args:
        input_grid: A 1-dimensional NumPy array of single-digit integers.

    Returns:
        A 1-dimensional NumPy array of single-digit integers (0 or 5) 
        after applying the transformation rule element-wise.
    """
    
    # Use np.where for efficient element-wise conditional assignment.
    # The condition is `input_grid != 0`.
    # If the condition is True (element is non-zero), the output value is 5.
    # If the condition is False (element is 0), the output value is 0.
    output_grid = np.where(input_grid != 0, 5, 0)
    
    # Return the resulting array
    return output_grid

```
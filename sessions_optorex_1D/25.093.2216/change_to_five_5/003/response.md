```python
"""
Transforms a 1D NumPy array of integers by replacing any non-zero integer with 5, while keeping zeros as 0.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a transformation to a NumPy array: maps 0 to 0 and non-zero values to 5.

    Args:
        input_grid: A 1-dimensional NumPy array of integers.

    Returns:
        A new 1-dimensional NumPy array with the transformation applied.
    """

    # 1. Receive the input NumPy array. (Implicit in function argument)

    # 2. Create a new NumPy array based on the condition.
    # Use np.where for efficient vectorized conditional assignment.
    # Condition: input_grid == 0
    # If True (element is 0), the output element is 0.
    # If False (element is not 0), the output element is 5.
    output_grid = np.where(input_grid == 0, 0, 5)

    # 3. Ensure the output dtype is integer if needed (np.where might infer float if mixing types, though 0 and 5 are both ints).
    # In this case, since both replacement values (0 and 5) are integers,
    # the output dtype will likely be inferred correctly as integer.
    # output_grid = output_grid.astype(input_grid.dtype) # Optional: Force same dtype as input

    # 4. Return the resulting new NumPy array.
    return output_grid
```
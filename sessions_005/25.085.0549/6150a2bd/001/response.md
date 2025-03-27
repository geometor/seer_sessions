```python
"""
Rotate the entire input grid by 180 degrees around its center to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the grid rotated 180 degrees.
    """
    # Convert the input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Rotate the numpy array by 180 degrees (equivalent to two 90-degree rotations)
    # The axes parameter is not needed for 2D rotation with k=2.
    rotated_array = np.rot90(input_array, k=2)

    # Convert the rotated numpy array back to a list of lists
    output_grid = rotated_array.tolist()

    return output_grid

```
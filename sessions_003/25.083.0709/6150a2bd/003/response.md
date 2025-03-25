```python
"""
The output grid is the input grid rotated 90 degrees counter-clockwise. More precisely, the i-th row of the input grid becomes the (N-1-i)-th column of the output grid, where N is the number of rows in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid, rotated 90 degrees
        counter-clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array, k=1) # k=1 for 90-degree CCW rotation

    # Convert the rotated array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

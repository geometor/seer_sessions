```python
"""
The transformation rule is a 90-degree clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The rotated grid.
    """
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)  # k=-1 for clockwise rotation

    # Convert the rotated array back to a list of lists
    output_grid = rotated_array.tolist()

    return output_grid
```
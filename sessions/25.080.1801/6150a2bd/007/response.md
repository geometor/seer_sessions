```python
"""
Rotate the input grid 90 degrees clockwise and then flip it horizontally (reverse the order of the columns).
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise and then flips it horizontally.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Flip the array horizontally (reverse the order of columns)
    flipped_array = np.fliplr(rotated_array)

    # Convert the NumPy array back to a list of lists
    output_grid = flipped_array.tolist()

    return output_grid
```

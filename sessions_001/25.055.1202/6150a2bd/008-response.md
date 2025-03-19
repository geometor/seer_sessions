# 6150a2bd • 008 • example_2 • investigate_coder

---
```python
"""
The input grid is rotated 90 degrees counter-clockwise, maintaining the original colors.
Alternatively, the entire input is diagonally mirrored across the axis going from top left to bottom right.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise or mirrors diagonally.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    # output_array = np.rot90(input_array)

    # Mirror the array diagonally
    output_array = np.transpose(input_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

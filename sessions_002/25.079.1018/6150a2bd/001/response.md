```python
"""
The transformation is a 90-degree clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    rotated_array = np.rot90(input_array, k=-1)

    # Convert the rotated array back to a list of lists.
    output_grid = rotated_array.tolist()

    return output_grid
```
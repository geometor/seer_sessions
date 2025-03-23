```python
"""
The input grid is rotated 90 degrees counter-clockwise.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise (k=1 for counter-clockwise).
    output_array = np.rot90(input_array, k=1)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```
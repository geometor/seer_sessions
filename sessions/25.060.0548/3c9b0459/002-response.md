# 3c9b0459 • 002 • example_4 • investigate_coder

---
```python
"""
The input grid is rotated 90 degrees clockwise.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise using np.rot90.
    # The second argument (-1) specifies the direction of rotation (clockwise).
    output_array = np.rot90(input_array, -1)

    # Convert the rotated NumPy array back to a list.
    output_grid = output_array.tolist()

    return output_grid
```

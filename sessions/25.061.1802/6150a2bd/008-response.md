# 6150a2bd • 008 • example_1 • investigate_coder

---
```python
"""
The input grid is rotated 90 degrees counter-clockwise to produce the output grid.  All elements maintain their original values, only their positions within the grid change according to the rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

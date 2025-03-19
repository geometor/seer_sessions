# 6150a2bd • 002 • example_1 • investigate_coder

---
```python
"""
The input grid is rotated 90 degrees counter-clockwise to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.
    """
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise
    output_array = np.rot90(input_array)

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```

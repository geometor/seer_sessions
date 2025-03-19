# 6150a2bd • 006 • refine_coder

---
```python
"""
The input grid is rotated 90 degrees counter-clockwise. This involves swapping the rows and columns and reversing the order of elements within each new row. The dimensions of the grid change accordingly: a grid of size *m* x *n* becomes a grid of size *n* x *m*.
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


# 6150a2bd • 012 • refine_coder

---
```python
"""
The input grid is rotated 90 degrees counter-clockwise. All colors and shapes are preserved during the rotation.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array)

    # Convert the rotated array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

# 6150a2bd • 002 • example_1 • investigate_coder

---
```python
"""
The transformation is a 180-degree rotation of the grid around its center point.  Each cell's value is moved to the position diametrically opposite the center. The central value is unchanged with this transformation.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array by 180 degrees using numpy's rot90 function (twice 90 = 180)
    output_array = np.rot90(input_array, 2)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    return output_grid
```

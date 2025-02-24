# 6150a2bd • 002 • example_1 • investigate_coder

---
```python
"""
The input is a 3x3 grid of colored pixels, where each pixel is represented by a single-digit integer.
The entire grid is rotated 90 degrees counter-clockwise.
The colors of the pixels are preserved during the rotation; only their positions change.
The rotated grid becomes the output.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.
    """
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise
    output_array = np.rot90(input_array, k=1)  # k=1 for 90-degree rotation

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```

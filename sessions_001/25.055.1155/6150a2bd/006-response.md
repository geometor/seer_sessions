# 6150a2bd • 006 • refine_coder

---
```python
"""
The transformation rule is a 90-degree counter-clockwise rotation of the input grid. The input is a 3x3 grid, and the output is the rotated 3x3 grid. The colors of the pixels remain the same, but their positions change according to the rotation.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise
    output_array = np.rot90(input_array, k=1)  # k=1 for 90-degree rotation

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```


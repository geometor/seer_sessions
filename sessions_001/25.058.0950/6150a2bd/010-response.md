# 6150a2bd • 010 • refine_coder

---
```python
"""
The transformation rule is a 90-degree counter-clockwise rotation of the input grid. Each element (pixel) in the input grid is moved to its new position in the output grid according to this rotation. The color/value of each pixel remains constant; only its position changes. The rotation is applied regardless of the original dimensions of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array, k=1)

    # Convert the result back to a list.
    return output_array.tolist()
```


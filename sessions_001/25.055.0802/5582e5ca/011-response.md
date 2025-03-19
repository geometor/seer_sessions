# 5582e5ca • 011 • refine_coder

---
```python
"""
1. Preserve Shape: The output grid will have the exact same dimensions (height and width) as the input grid.
2. Universal Replacement: Every pixel in the input grid, regardless of its original color, is replaced with the color maroon (value 9).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same shape as the input grid.
    output_grid = np.full(input_grid.shape, 9)  # Use np.full for efficiency

    # The shape is already correct, and all pixels are set to 9 (maroon).

    return output_grid
```


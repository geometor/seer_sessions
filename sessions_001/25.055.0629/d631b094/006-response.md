# d631b094 • 006 • refine_coder

---
```python
"""
If the input grid contains at least one blue pixel (1), the output is a 1x1 grid containing a single blue pixel (1).
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Check if any pixel is blue (1).
    if np.any(input_array == 1):
        # Create a 1x1 output grid filled with blue (1).
        output_grid = np.array([[1]])
    else:
        # should not happen based on the current examples
        output_grid = np.array([[0]])

    return output_grid.tolist()
```


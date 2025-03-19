# d9fac9be • 014 • refine_coder

---
```python
"""
The transformation rule determines if the input grid contains any blue pixels. If blue is present anywhere in the input grid, the output is a 1x1 grid containing the value 1. If blue is not present, the output is a 1x1 grid containing the value 0.
"""

import numpy as np

def transform(input_grid):
    """
    Checks for the presence of blue pixels in the input grid.
    Returns 1 if blue is present, 0 otherwise.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    grid = np.array(input_grid)

    # Check if any pixel is blue (1)
    if np.any(grid == 1):
        output_grid = np.array([[1]])  # Output 1 if blue is present
    else:
        output_grid = np.array([[0]])  # Output 0 if blue is not present

    return output_grid
```


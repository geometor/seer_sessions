# 77fdfe62 • 011 • refine_coder

---
```python
"""
Transforms the input grid by extracting the corner pixel values and
creating a 2x2 output grid with those values, mapping each input corner
to the corresponding output corner.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Initialize the output grid as a 2x2 numpy array
    output_grid = np.zeros((2, 2), dtype=int)

    # Extract the corner values from the input grid and populate the output grid
    output_grid[0, 0] = input_grid[0, 0]  # Top-left
    output_grid[0, 1] = input_grid[0, cols - 1]  # Top-right
    output_grid[1, 0] = input_grid[rows - 1, 0]  # Bottom-left
    output_grid[1, 1] = input_grid[rows - 1, cols - 1]  # Bottom-right

    return output_grid
```


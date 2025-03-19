# cce03e0d • 010 • example_2 • investigate_coder

---
```python
"""
Replicates a 3x3 input grid into a 9x9 output grid at the top-right, bottom-left, and bottom-right corners. The rest of the output grid is filled with zeros.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 9x9 output grid with zeros.
    output_grid = np.zeros((9, 9), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Copy the input grid to the top-right corner of the output grid.
    output_grid[0:input_height, 6:6+input_width] = input_grid

    # Copy the input grid to the bottom-left corner of the output grid.
    output_grid[6:6+input_height, 0:input_width] = input_grid

    # Copy the input grid to the bottom-right corner of the output grid.
    output_grid[6:6+input_height, 6:6+input_width] = input_grid

    return output_grid
```

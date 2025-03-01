# 137eaa0f • 012 • refine_coder

---
```python
"""
Copies non-zero pixels from the last row of the 4x4 input grid to the first row of the 3x3 output grid, preserving color and relative horizontal position.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Get the last row of the input grid.
    last_row = input_grid[-1, :]

    # Find non-zero pixels in the last row and their indices.
    non_zero_indices = np.nonzero(last_row)[0]
    non_zero_values = last_row[non_zero_indices]

    # Copy the non-zero pixels to the first row of the output grid.
    output_grid[0, :len(non_zero_values)] = non_zero_values
    
    return output_grid
```

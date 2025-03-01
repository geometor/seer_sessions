# cdecee7f • 005 • refine_coder

---
```python
"""
The transformation identifies the first non-zero pixel in the input grid.
It creates a 3x3 output grid filled with zeros.
The color of the identified non-zero pixel is placed in the top-left corner (0,0) of the output grid.
"""

import numpy as np

def find_first_non_zero(grid):
    """Finds the first non-zero element in a grid."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return grid[r, c]
    return 0  # Return 0 if no non-zero element is found

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find First Non-Zero:
    first_non_zero_color = find_first_non_zero(input_grid)

    # Place Color:
    if first_non_zero_color != 0:
        output_grid[0, 0] = first_non_zero_color
    
    # Return Output Grid
    return output_grid
```

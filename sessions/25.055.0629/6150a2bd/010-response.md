# 6150a2bd • 010 • refine_coder

---
```python
"""
1. Rotate the Grid: Rotate the entire input grid by 180 degrees clockwise.

2. Color Swap: Apply the following color substitutions based on the *rotated* grid:
    *   Blue (1) becomes Grey (5).
    *   Red (2) becomes Blue (1).
    *   Grey (5) becomes Red (2).
    *   Yellow (4) becomes Azure (8).
    *   Azure (8) becomes Yellow (4).
    *   White (0) remains White (0).
    *   Maroon (9) remains Maroon(9)
"""

import numpy as np

def rotate_grid(grid):
    """Rotates a grid 180 degrees clockwise."""
    return np.rot90(grid, 2)

def color_swap(val):
    """Performs the complete color swap."""
    if val == 1:
        return 5
    elif val == 2:
        return 1
    elif val == 5:
        return 2
    elif val == 4:
        return 8
    elif val == 8:
        return 4
    elif val == 0:
        return 0
    elif val == 9:
        return 9
    else:
        return val # Should not happen, but good practice

def transform(input_grid):
    # initialize output_grid
    output_grid = np.array(input_grid)
    
    # Rotate the grid 180 degrees
    output_grid = rotate_grid(output_grid)

    # Apply color swap
    it = np.nditer(output_grid, flags=['multi_index'], op_flags=['readwrite'])
    for x in it:
      output_grid[it.multi_index] = color_swap(int(x))

    return output_grid.tolist()
```

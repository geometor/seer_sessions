# bc1d5164 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation extracts a subgrid containing only the yellow
pixels and their immediate white neighbors, discarding the rest. The minimal
subgrid containing the target values and immediate neighbor is the output.
"""

import numpy as np

def get_target_pixels(grid, target_value):
    """Finds coordinates of all pixels with the target value."""
    return np.argwhere(grid == target_value)

def transform(input_grid):
    """Transforms the input grid to the output grid."""
    input_grid = np.array(input_grid)
    target_value = 4

    # 1. Identify Target Pixels
    target_pixels = get_target_pixels(input_grid, target_value)

    # 2. Determine Output Grid Dimensions and Extract Subgrid
    if target_pixels.size > 0:
        min_row = np.min(target_pixels[:, 0])
        max_row = np.max(target_pixels[:, 0])
        min_col = np.min(target_pixels[:, 1])
        max_col = np.max(target_pixels[:, 1])

        output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    else:  # Handle the case with no target pixels (empty output)
        output_grid = np.array([])
        
    return output_grid.tolist()
```

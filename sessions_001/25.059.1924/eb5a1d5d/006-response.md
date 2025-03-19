# eb5a1d5d • 006 • refine_coder

---
```python
"""
The transformation identifies the bottom-right non-background (azure) pixel in the input grid and places it at the bottom-right corner (4, 4) of a 5x5 output grid filled with the background color (azure).
"""

import numpy as np

def find_bottom_right_non_background(grid):
    """Finds the coordinates of the bottom-right non-background pixel."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] != 8:
                return r, c
    return None  # Should never happen in this task, but good practice

def transform(input_grid):
    # Create a 5x5 output grid filled with the background color (8).
    output_grid = np.full((5, 5), 8, dtype=int)

    # Find the coordinates of the bottom-right non-background pixel.
    target_coords = find_bottom_right_non_background(input_grid)

    # If a target pixel was found (it always should be in this specific task),
    # place its color at the bottom-right corner of the output grid.
    if target_coords:
        target_row, target_col = target_coords
        output_grid[4, 4] = input_grid[target_row, target_col]

    return output_grid
```


# d631b094 • 010 • refine_coder

---
```python
"""
Examines the input grid for a 3x1 block of red cells. If found, creates a 1x3 output grid filled with red; otherwise, creates a 1x3 output grid filled with zeros.
"""

import numpy as np

def _find_red_3x1_block(grid):
    """
    Helper function to check for a 3x1 block of red cells.
    """
    grid = np.array(grid)
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols):
            if grid[r, c] == 2 and grid[r+1, c] == 2 and grid[r+2, c] == 2:
                return True
    return False

def transform(input_grid):
    """
    Transforms the input grid to output.
    """
    # Initialize output_grid as a 1x3 numpy array filled with zeros.
    output_grid = np.zeros((1, 3), dtype=int)

    # Check if a 3x1 red block exists.
    red_block_exists = _find_red_3x1_block(input_grid)

    # If a 3x1 red block exists, fill the output grid with red (2).
    if red_block_exists:
        output_grid[:] = 2

    return output_grid.tolist()
```


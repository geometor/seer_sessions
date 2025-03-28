# 2dc579da • 002 • example_1 • investigate_coder

---
```python
"""
Extracts a 2x2 subgrid from the bottom-left corner of the input grid,
starting at the first non-azure(8) pixel.
"""

import numpy as np

def find_bottom_left_non_8(grid):
    """Finds the row index of the bottom-most, left-most non-8 pixel."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols):
            if grid[r, c] != 8:
                return r, c
    return None  # Should not happen in these tasks, as there's always a non-8 pixel

def transform(input_grid):
    """Extracts a 2x2 subgrid based on color change in bottom left."""
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the bottom-left non-8 pixel
    start_row, start_col = find_bottom_left_non_8(input_grid)

    # Extract the 2x2 subgrid
    output_grid = input_grid[start_row-1:start_row+1, start_col:start_col+2]
    
    return output_grid.tolist()
```

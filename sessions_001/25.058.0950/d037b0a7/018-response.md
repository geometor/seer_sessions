# d037b0a7 • 018 • refine_coder

---
```python
"""
Copies the non-zero pixel in the input grid to the cell directly below it, unless it's in the bottom row.
"""

import numpy as np

def transform(input_grid):
    """
    Copies the non-zero pixel to the cell below.
    """
    output_grid = np.copy(input_grid)  # Create a copy to avoid modifying the original
    rows, cols = input_grid.shape

    # Find the non-zero pixel
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                # Copy the value to the cell below if not in the last row
                if r < rows - 1:
                    output_grid[r + 1, c] = input_grid[r, c]
                return output_grid  # Only one non-zero pixel is copied
    return output_grid # return if no non-zero pixel
```


# 6d0160f0 • 017 • refine_coder

---
```python
"""
1. Identify all rows, and pixels within the rows.
2. Identify gray (color 5) rows, and preserve them.
3. Identify single colored pixels (not color 0 or 5), and preserve them.
4. Transform every other pixel to black (color 0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid.
    for r in range(rows):
        for c in range(cols):
            # Preserve gray pixels (5).
            if input_grid[r, c] == 5:
                continue  # Gray pixels are already copied
            
            # Check if the current row contains only 0, 5, or one other color
            row_colors = np.unique(input_grid[r])
            non_zero_non_gray_colors = row_colors[(row_colors != 0) & (row_colors != 5)]

            if len(non_zero_non_gray_colors) == 1 and input_grid[r,c] != 0 and input_grid[r,c] != 5:
                # Preserve single colored pixels
                output_grid[r,c] = input_grid[r,c]
            elif input_grid[r,c] != 5:
                # Transform other non-gray pixels to black (0)
                output_grid[r,c] = 0
                
    return output_grid
```

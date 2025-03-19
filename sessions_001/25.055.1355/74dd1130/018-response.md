# 74dd1130 • 018 • refine_coder

---
```python
"""
The transformation involves swapping the values of two adjacent cells colored azure (8) and gray (5). The swap occurs in the bottom-most row where such an adjacent pair exists. The left cell takes the value of the right cell, and vice-versa. If no such pair exists, the grid remains unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through rows from bottom to top
    for r in range(rows - 1, -1, -1):
        # Iterate through columns to find adjacent pairs
        for c in range(cols - 1):
            if (output_grid[r, c] == 8 and output_grid[r, c+1] == 5) or \
               (output_grid[r, c] == 5 and output_grid[r, c+1] == 8):
                # Swap the values
                temp = output_grid[r, c]
                output_grid[r, c] = output_grid[r, c+1]
                output_grid[r, c+1] = temp
                return output_grid  # Return after the first swap

    return output_grid  # Return unchanged if no swap is found
```


# 1b2d62fb • 006 • refine_coder

---
```python
"""
1. **Identify Blue Column:** Find the column(s) in the input grid that contain blue pixels (value 1).
2. **Extract Bottom Two:** Within the identified blue column, locate the bottom two blue pixels.
3. **Create output grid:** 5x3 filled with color=0
4. **Transform and Place:** Create two azure pixels adjacent to each other in row 3 (zero indexed) of the output grid. The placement of the azure pixels starts in a column that is calculated by using the modulus operator `%` on the blue column index.
 The formula `output_grid[3, stripe_col % 3] = 8` combined with `output_grid[3, (stripe_col+1) % 3 ] = 8`, captures the placement.
"""

import numpy as np

def find_blue_stripe(grid):
    # Find the column index where the blue stripe (color 1) exists. Assumes one continuous stripe.
    rows, cols = grid.shape
    for j in range(cols):
        if np.any(grid[:, j] == 1):
            return j
    return -1  # No blue stripe found

def transform(input_grid):
    # Initialize output_grid as 5x3, filled with white (0)
    output_grid = np.zeros((5, 3), dtype=int)

    # Find the central blue stripe column
    stripe_col = find_blue_stripe(input_grid)

    # If a blue stripe is found...
    if stripe_col != -1:
        # Find the indices of blue pixels in the stripe column
        blue_indices = np.where(input_grid[:, stripe_col] == 1)[0]

        # Check if we have at least two blue pixels
        if len(blue_indices) >= 2:
            # Get the bottom two blue pixels
            output_grid[3, stripe_col % 3] = 8
            output_grid[3, (stripe_col+1) % 3 ] = 8

    return output_grid
```

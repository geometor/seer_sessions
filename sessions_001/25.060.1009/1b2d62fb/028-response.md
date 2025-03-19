# 1b2d62fb • 028 • example_5 • investigate_coder

---
```python
"""
1.  **Locate:** Find the vertical column of blue (1) pixels in the input grid.
2.  **Crop:** Create a 5x3 output grid. The x index of the center column of this grid corresponds to the center column of the 1's in the input grid. The y range goes from 0 to 4.
3. **Color Mapping:** Find the positions with respect to the input grid that should be copied over.
4.  **Transform:** Fill the output grid. All positions that have color 1 in the input grid get color 8. Every other pixel gets color 0.
"""

import numpy as np

def find_vertical_stripe(grid, color):
    # Find the column index where the stripe of the given color exists.
    for j in range(grid.shape[1]):
        if all(grid[:, j] == color):
            return j
    return -1

def transform(input_grid):
    # Find the column index of the blue stripe (color 1).
    stripe_col = find_vertical_stripe(input_grid, 1)

    # Initialize the output grid with all zeros (white).
    output_grid = np.zeros((5, 3), dtype=int)
    
    # Calculate starting column of the stripe.
    start_col = stripe_col -1

    # Iterate through the input grid's relevant section and map colors.
    for i in range(5):
        for j in range(3):
          if input_grid[i,start_col + j] == 1:
            output_grid[i,j] = 8
          else:
            output_grid[i,j] = 0


    return output_grid
```

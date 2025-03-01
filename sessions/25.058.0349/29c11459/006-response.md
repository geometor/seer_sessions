# 29c11459 • 006 • refine_coder

---
```python
"""
1. Iterate through each row of the input grid.
2. For each row:
   - Find the positions of all blue (1) and red (2) pixels.
   - If both blue and red pixels are present:
     - Calculate the midpoint between the last blue pixel and the first red pixel.
     - Fill all pixels from the beginning of the row up to (but not including) the midpoint with blue (1).
     - Fill all pixels from the midpoint + 1 to the end of the row with red (2).
     - Place a gray pixel (5) at the calculated midpoint.
   - If only blue or red pixels exist, leave as is
3. Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows = input_grid.shape[0]

    for r_idx in range(rows):
      row = input_grid[r_idx]
      
      # Find blue and red pixel indices
      blue_pixels = np.where(row == 1)[0]
      red_pixels = np.where(row == 2)[0]

      # if both exists
      if blue_pixels.size > 0 and red_pixels.size > 0:
        # use last blue and first red
        midpoint = (blue_pixels[-1] + red_pixels[0]) // 2
        
        # Fill from start to midpoint with blue
        output_grid[r_idx, :midpoint] = 1
        
        # insert gray
        output_grid[r_idx, midpoint] = 5
        
        # fill from midpoint + 1 with red
        output_grid[r_idx, midpoint + 1:] = 2
    return output_grid
```

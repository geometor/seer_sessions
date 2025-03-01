# aedd82e4 • 020 • refine_coder

---
```python
"""
1.  **Identify the Target Pixel:** Find the single red (value 2) pixel in the input grid.
2.  **Change Color:** Change the color of this pixel to blue (value 1).
3. **Return Output:** output is the same as input, except for the single pixel that was changed.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # find all red pixels
    red_pixels = np.argwhere(input_grid == 2)
    
    # Check if there is exactly one red pixel
    if len(red_pixels) == 1:
      # get row and column index, and change that pixel to blue.
      row_index, col_index = red_pixels[0]
      output_grid[row_index, col_index] = 1

    return output_grid
```

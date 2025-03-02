# d9fac9be • 004 • example_1 • investigate_coder

---
```python
"""
1. Identify colored regions: Examine the input grid and identify contiguous regions of the same color. Consider white (0) as background.
2. Count instances of Red Regions: Count the number of discontinguous single pixels with color red (2)
3. Output: Create an output grid containing single pixel with the color red(2).
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid to extract the color red (2)
    """
    # initialize output_grid as a single pixel
    output_grid = np.array([[0]])
    
    # Find red pixels
    red_pixels = []
    for row_idx, row in enumerate(input_grid):
       for col_idx, pixel in enumerate(row):
          if pixel == 2:
             red_pixels.append((row_idx, col_idx))

    # if red pixels are present set output grid to red
    if (len(red_pixels) > 0):
       output_grid[0,0] = 2

    return output_grid
```

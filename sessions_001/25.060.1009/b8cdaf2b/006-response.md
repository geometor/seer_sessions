# b8cdaf2b • 006 • example_1 • investigate_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Identify:** Focus on the 3x3 grid of pixels.
2.  **Locate:** Specifically target the top row of the grid.
3.  **Conditional Replacement:** If a pixel in the top row has the color value 0 (white), replace it with the color value 4 (yellow).
4. **Preservation:** All other pixels, including those not in the top row or those in the top row that doesn't equal to 0, retain their original color values.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through the pixels of the top row (row index 0).
    for x in range(output_grid.shape[1]):
      # Check if the pixel's color is white (0).
      if output_grid[0, x] == 0:
        # replace the pixel with yellow (4)
        output_grid[0,x] = 4
    
    #return the modified grid
    return output_grid
```


# 25d8a9c8 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation involves a simple color mapping. Iterate through each pixel in the input grid.
1.  If a pixel is red, change it to white (0).
2.  If a pixel is yellow, change it to gray (5).
3. If a pixel is maroon, change it to gray (5).
4.  Maintain the grid's original 3x3 structure. Other colors are not present in input, thus no explicit rule needed.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy to modify
    output_grid = input_grid.copy()

    # change output pixels based on color mapping
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 2:  # Red
                output_grid[i, j] = 0  # White
            elif output_grid[i, j] == 4:  # Yellow
                output_grid[i, j] = 5  # Gray
            elif output_grid[i, j] == 9:  # Maroon
                output_grid[i, j] = 5  # Gray
    return output_grid
```

# 25ff71a9 • 026 • example_4 • investigate_coder

---
```python
"""
The transformation rule appears to either rotate the red pixels 90 degrees clockwise, OR it reflects the grid along the horizontal axis (x-axis).

1.  **Identify** the contiguous block of red (2) pixels within the input grid.
2.  **Rotate** the set of red pixels 90 degrees clockwise within the 3x3 grid. OR
3.  **Reflect** the position of the red pixels across the x-axis

"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    input_grid_shape = input_grid.shape
    # Find the coordinates of red pixels
    red_pixels = np.argwhere(input_grid == 2)

    # Apply 90-degree clockwise rotation OR reflection across x-axis
    for r, c in red_pixels:
      # new_r = c
      #  new_c = input_grid_shape[0] -1 - r
        new_r = input_grid_shape[0] - 1 - r
        new_c = c
        output_grid[r,c] = 0 #clear old position
        output_grid[new_r, new_c] = 2 #set the color

    return output_grid
```
